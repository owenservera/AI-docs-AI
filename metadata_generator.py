"""
Metadata Generator for AI-Friendly Documentation

This module generates rich metadata for documentation pages including
taxonomy tags, content type classification, and JSON-LD schema markup
for better AI consumption and semantic understanding.
"""

import re
import json
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import datetime


class MetadataGenerator:
    """Generates rich metadata for documentation pages"""

    def __init__(self):
        # Content type patterns
        self.content_patterns = {
            "api_reference": [
                r"api\s+reference",
                r"api\s+docs",
                r"api\s+documentation",
                r"endpoint",
                r"method",
                r"parameter",
                r"response",
                r"authentication",
                r"authorization",
            ],
            "tutorial": [
                r"tutorial",
                r"getting\s+started",
                r"guide",
                r"walkthrough",
                r"learn",
                r"beginner",
                r"introduction",
                r"quick\s+start",
            ],
            "faq": [
                r"faq",
                r"frequently\s+asked",
                r"questions?",
                r"troubleshoot",
                r"common\s+issues",
                r"help",
                r"support",
            ],
            "how_to": [
                r"how\s+to",
                r"install",
                r"setup",
                r"configure",
                r"deploy",
                r"build",
                r"run",
                r"create",
                r"implement",
            ],
            "reference": [
                r"reference",
                r"glossary",
                r"terminology",
                r"dictionary",
                r"syntax",
                r"specification",
                r"standard",
            ],
            "conceptual": [
                r"concepts?",
                r"overview",
                r"architecture",
                r"design",
                r"understanding",
                r"background",
                r"theory",
            ],
            "troubleshooting": [
                r"troubleshoot",
                r"debug",
                r"error",
                r"fix",
                r"problem",
                r"issue",
                r"solution",
                r"resolve",
            ],
        }

        # Taxonomy tags
        self.taxonomy_keywords = {
            "framework": [
                "react",
                "vue",
                "angular",
                "django",
                "flask",
                "fastapi",
                "express",
            ],
            "language": [
                "python",
                "javascript",
                "typescript",
                "java",
                "go",
                "rust",
                "c++",
                "php",
            ],
            "database": ["postgresql", "mysql", "mongodb", "redis", "sqlite", "oracle"],
            "cloud": ["aws", "azure", "gcp", "heroku", "vercel", "netlify", "docker"],
            "tool": ["git", "npm", "yarn", "webpack", "babel", "eslint", "prettier"],
            "platform": ["linux", "macos", "windows", "ios", "android", "web"],
        }

    def generate_page_metadata(
        self, url: str, content: str, soup: BeautifulSoup
    ) -> Dict[str, Any]:
        """Generate comprehensive metadata for a documentation page"""

        title = self._extract_title(soup)
        description = self._extract_description(soup)

        return {
            "url": url,
            "title": title,
            "description": description,
            "content_type": self._classify_content_type(content, title, description),
            "taxonomies": self._extract_taxonomies(content, title, url),
            "entities": self._extract_entities(content),
            "version": self._extract_version(content, soup),
            "last_updated": self._extract_last_updated(soup),
            "word_count": len(content.split()),
            "code_blocks_count": len(soup.find_all(["pre", "code"])),
            "heading_count": len(soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])),
            "link_count": len(soup.find_all("a", href=True)),
            "image_count": len(soup.find_all("img")),
            "keywords": self._extract_keywords(content),
            "reading_time": self._estimate_reading_time(content),
            "complexity_score": self._calculate_complexity_score(content, soup),
            "metadata_generated": datetime.now().isoformat(),
        }

    def generate_jsonld_schema(
        self, metadata: Dict[str, Any], soup: BeautifulSoup
    ) -> Dict[str, Any]:
        """Generate JSON-LD structured data for the page"""

        schema = {
            "@context": "https://schema.org",
            "@type": self._get_schema_type(metadata["content_type"]),
            "url": metadata["url"],
            "name": metadata["title"],
            "description": metadata["description"],
        }

        # Add content-specific schema properties
        if metadata["content_type"] == "faq":
            schema.update(self._generate_faq_schema(soup))
        elif metadata["content_type"] == "how_to":
            schema.update(self._generate_howto_schema(soup))
        elif metadata["content_type"] == "api_reference":
            schema.update(self._generate_api_schema(soup))

        # Add common properties
        if metadata.get("last_updated"):
            schema["dateModified"] = metadata["last_updated"]
        if metadata.get("version"):
            schema["version"] = metadata["version"]

        # Add keywords as tags
        if metadata.get("keywords"):
            schema["keywords"] = metadata["keywords"][:10]  # Limit to top 10

        return schema

    def generate_taxonomy_summary(
        self, pages_metadata: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate taxonomy summary for entire documentation set"""

        summary = {
            "total_pages": len(pages_metadata),
            "content_type_distribution": {},
            "taxonomy_distribution": {},
            "entity_distribution": {},
            "version_distribution": {},
            "generated_at": datetime.now().isoformat(),
        }

        # Aggregate distributions
        for page in pages_metadata:
            # Content types
            ct = page.get("content_type", "unknown")
            summary["content_type_distribution"][ct] = (
                summary["content_type_distribution"].get(ct, 0) + 1
            )

            # Taxonomies
            for tax_type, tax_values in page.get("taxonomies", {}).items():
                if tax_type not in summary["taxonomy_distribution"]:
                    summary["taxonomy_distribution"][tax_type] = {}
                for value in tax_values:
                    summary["taxonomy_distribution"][tax_type][value] = (
                        summary["taxonomy_distribution"][tax_type].get(value, 0) + 1
                    )

            # Entities
            for entity_type, entities in page.get("entities", {}).items():
                if entity_type not in summary["entity_distribution"]:
                    summary["entity_distribution"][entity_type] = {}
                for entity in entities:
                    summary["entity_distribution"][entity_type][entity] = (
                        summary["entity_distribution"][entity_type].get(entity, 0) + 1
                    )

            # Versions
            version = page.get("version", "unknown")
            summary["version_distribution"][version] = (
                summary["version_distribution"].get(version, 0) + 1
            )

        return summary

    def _classify_content_type(self, content: str, title: str, description: str) -> str:
        """Classify the content type based on text analysis"""

        # Combine all text for analysis
        text = f"{title} {description} {content}".lower()

        # Score each content type
        scores = {}
        for content_type, patterns in self.content_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            scores[content_type] = score

        # Return highest scoring type, or "general" if no clear match
        max_score = max(scores.values()) if scores else 0
        if max_score >= 2:  # Require at least 2 matches
            return max(scores, key=scores.get)

        return "general"

    def _extract_taxonomies(
        self, content: str, title: str, url: str
    ) -> Dict[str, List[str]]:
        """Extract taxonomy tags from content"""

        text = f"{title} {content}".lower()
        taxonomies = {}

        for tax_type, keywords in self.taxonomy_keywords.items():
            matches = []
            for keyword in keywords:
                if keyword.lower() in text:
                    matches.append(keyword)
            if matches:
                taxonomies[tax_type] = matches

        # Extract version numbers
        version_pattern = r"\b(v?\d+\.\d+(\.\d+)?)\b"
        versions = re.findall(version_pattern, url + " " + title)
        if versions:
            taxonomies["version"] = [v[0] for v in versions]

        return taxonomies

    def _extract_entities(self, content: str) -> Dict[str, List[str]]:
        """Extract named entities and technical concepts"""

        entities = {
            "code_references": [],
            "api_endpoints": [],
            "file_extensions": [],
            "command_names": [],
        }

        # Extract code references (function names, classes, etc.)
        code_patterns = [
            r"\b([a-zA-Z_][a-zA-Z0-9_]*)\([^)]*\)",  # function calls
            r"\bclass\s+([a-zA-Z_][a-zA-Z0-9_]*)",  # class definitions
            r"\bdef\s+([a-zA-Z_][a-zA-Z0-9_]*)",  # function definitions
            r"\bconst\s+([a-zA-Z_$][a-zA-Z0-9_$]*)",  # JS constants
            r"\blet\s+([a-zA-Z_$][a-zA-Z0-9_$]*)",  # JS variables
        ]

        for pattern in code_patterns:
            matches = re.findall(pattern, content)
            entities["code_references"].extend(matches[:10])  # Limit to avoid spam

        # Extract API endpoints
        api_patterns = [
            r"/api/[a-zA-Z0-9_/{}?-]+",  # REST API paths
            r"POST\s+(/[a-zA-Z0-9_/{}?-]+)",  # HTTP methods
            r"GET\s+(/[a-zA-Z0-9_/{}?-]+)",
            r"PUT\s+(/[a-zA-Z0-9_/{}?-]+)",
            r"DELETE\s+(/[a-zA-Z0-9_/{}?-]+)",
        ]

        for pattern in api_patterns:
            matches = re.findall(pattern, content)
            entities["api_endpoints"].extend(matches[:10])

        # Extract file extensions
        ext_pattern = r"\.([a-zA-Z0-9]{2,4})\b"
        extensions = re.findall(ext_pattern, content)
        entities["file_extensions"] = list(set(extensions))[:10]

        # Extract command names
        cmd_pattern = (
            r"\b([a-zA-Z][a-zA-Z0-9_-]*)\s+(--?[a-zA-Z][a-zA-Z0-9_-]*(?:\s+[^-\n]+)?)"
        )
        commands = re.findall(cmd_pattern, content)
        entities["command_names"] = [f"{cmd[0]} {cmd[1]}" for cmd in commands[:5]]

        # Remove duplicates and empty values
        for key in entities:
            entities[key] = list(set([e.strip() for e in entities[key] if e.strip()]))

        return entities

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title with fallback logic"""

        # Try title tag
        title_tag = soup.find("title")
        if title_tag and title_tag.get_text(strip=True):
            return title_tag.get_text(strip=True)

        # Try h1
        h1 = soup.find("h1")
        if h1 and h1.get_text(strip=True):
            return h1.get_text(strip=True)

        # Try og:title
        og_title = soup.find("meta", attrs={"property": "og:title"})
        if og_title and og_title.get("content"):
            return og_title["content"]

        return "Untitled Page"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description"""

        # Try meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc and meta_desc.get("content"):
            return meta_desc["content"]

        # Try og:description
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if og_desc and og_desc.get("content"):
            return og_desc["content"]

        # Try first substantial paragraph
        paragraphs = soup.find_all("p")
        for p in paragraphs:
            text = p.get_text(strip=True)
            if len(text) > 50:  # Substantial content
                return text[:200] + "..." if len(text) > 200 else text

        return ""

    def _extract_version(self, content: str, soup: BeautifulSoup) -> Optional[str]:
        """Extract version information"""

        # Try common version patterns
        version_patterns = [
            r"\b(version|v)\s*[:=]?\s*(\d+\.\d+(\.\d+)?)",
            r"\b(\d+\.\d+(\.\d+)?)\s+(release|version)",
            r"v(\d+\.\d+(\.\d+)?)",
        ]

        for pattern in version_patterns:
            match = re.search(pattern, content, re.IGNORECASE)
            if match:
                return match.group(1) if match.group(1) else match.group(2)

        # Try URL path for version
        url = soup.find("meta", attrs={"property": "og:url"})
        if url:
            url_path = url.get("content", "")
            version_match = re.search(r"/v?(\d+\.\d+)/", url_path)
            if version_match:
                return version_match.group(1)

        return None

    def _extract_last_updated(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract last updated/modified date"""

        # Try common date meta tags
        date_selectors = [
            ("meta", {"name": "last-modified"}),
            ("meta", {"property": "article:modified_time"}),
            ("meta", {"name": "revised"}),
            ("time", {"datetime": True}),
            ("time", {}),
        ]

        for selector in date_selectors:
            tag = soup.find(*selector)
            if tag:
                date_str = tag.get("content") or tag.get("datetime") or tag.get_text()
                if date_str:
                    # Try to parse various date formats
                    try:
                        # ISO format
                        if "T" in date_str:
                            return date_str
                        # Other formats - just return as-is for now
                        return date_str
                    except:
                        continue

        return None

    def _extract_keywords(self, content: str) -> List[str]:
        """Extract important keywords using TF-IDF style scoring"""

        # Simple keyword extraction (in a real implementation, use proper NLP)
        words = re.findall(r"\b[a-zA-Z]{4,}\b", content.lower())

        # Remove common stop words
        stop_words = {
            "the",
            "and",
            "for",
            "are",
            "but",
            "not",
            "you",
            "all",
            "can",
            "had",
            "her",
            "was",
            "one",
            "our",
            "out",
            "day",
            "get",
            "has",
            "him",
            "his",
            "how",
            "its",
            "may",
            "new",
            "now",
            "old",
            "see",
            "two",
            "way",
            "who",
            "boy",
            "did",
            "her",
            "his",
            "let",
            "put",
            "say",
            "she",
            "too",
            "use",
            "that",
            "with",
            "have",
            "this",
            "will",
            "your",
            "from",
            "they",
            "know",
            "want",
            "been",
            "good",
            "much",
            "some",
            "time",
            "very",
            "when",
            "come",
            "here",
            "just",
            "like",
            "long",
            "make",
            "many",
            "over",
            "such",
            "take",
            "than",
            "them",
            "well",
            "were",
        }

        keywords = [word for word in words if word not in stop_words]

        # Count frequency and return top keywords
        from collections import Counter

        keyword_counts = Counter(keywords)
        return [word for word, count in keyword_counts.most_common(20)]

    def _estimate_reading_time(self, content: str) -> int:
        """Estimate reading time in minutes"""

        words_per_minute = 200  # Average reading speed
        word_count = len(content.split())
        return max(1, round(word_count / words_per_minute))

    def _calculate_complexity_score(self, content: str, soup: BeautifulSoup) -> float:
        """Calculate content complexity score (0-10)"""

        score = 0

        # Code density
        code_blocks = soup.find_all(["pre", "code"])
        code_chars = sum(len(block.get_text()) for block in code_blocks)
        code_ratio = code_chars / len(content) if content else 0
        score += code_ratio * 5  # Up to 5 points for code density

        # Technical terms (simple heuristic)
        technical_indicators = [
            "function",
            "class",
            "method",
            "api",
            "endpoint",
            "parameter",
            "config",
        ]
        tech_count = sum(content.lower().count(term) for term in technical_indicators)
        tech_score = min(3, tech_count / 10)  # Up to 3 points for technical terms
        score += tech_score

        # Heading complexity
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])
        heading_score = min(2, len(headings) / 5)  # Up to 2 points for structure
        score += heading_score

        return round(min(10, score), 1)

    def _get_schema_type(self, content_type: str) -> str:
        """Map content type to JSON-LD schema type"""

        schema_mapping = {
            "faq": "FAQPage",
            "how_to": "HowTo",
            "api_reference": "APIReference",
            "tutorial": "TechArticle",
            "reference": "TechArticle",
            "troubleshooting": "TechArticle",
            "conceptual": "Article",
        }

        return schema_mapping.get(content_type, "Article")

    def _generate_faq_schema(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Generate FAQ schema from page content"""

        faqs = []

        # Look for common FAQ patterns
        questions = soup.find_all(["h2", "h3", "h4"])
        answers = soup.find_all("p")

        # Simple heuristic: question headings followed by answer paragraphs
        for i, q in enumerate(questions):
            question_text = q.get_text(strip=True)
            if any(
                word in question_text.lower()
                for word in ["what", "how", "why", "when", "where", "can", "do"]
            ):
                # Find next paragraph as answer
                answer_elem = q.find_next(["p", "div"])
                if answer_elem:
                    answer_text = answer_elem.get_text(strip=True)
                    if len(answer_text) > 20:
                        faqs.append(
                            {
                                "@type": "Question",
                                "name": question_text,
                                "acceptedAnswer": {
                                    "@type": "Answer",
                                    "text": answer_text,
                                },
                            }
                        )

        return {"mainEntity": faqs} if faqs else {}

    def _generate_howto_schema(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Generate HowTo schema from page content"""

        steps = []

        # Look for ordered lists or step indicators
        ol = soup.find("ol")
        if ol:
            for i, li in enumerate(ol.find_all("li")):
                steps.append(
                    {
                        "@type": "HowToStep",
                        "position": i + 1,
                        "text": li.get_text(strip=True),
                    }
                )

        return {"step": steps} if steps else {}

    def _generate_api_schema(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Generate API reference schema"""

        # This would be more complex in a real implementation
        # For now, just mark it as a technical article
        return {"@type": "TechArticle", "genre": "API Documentation"}
