"""
Content Extractor for AI-Friendly Documentation Formats

This module extracts clean, AI-friendly content from HTML pages,
removing navigation, scripts, styles, and other UI elements that
are not useful for LLM consumption.
"""

import re
import json
from typing import Dict, List, Optional, Any
from bs4 import BeautifulSoup, NavigableString, Tag
import html2text
from urllib.parse import urljoin, urlparse


class ContentExtractor:
    """Extracts clean content from HTML pages for AI consumption"""

    def __init__(self):
        # Initialize HTML to Markdown converter
        self.html2md = html2text.HTML2Text()
        self.html2md.ignore_links = False
        self.html2md.ignore_images = True  # Skip images for AI mode
        self.html2md.ignore_tables = False
        self.html2md.ignore_emphasis = False
        self.html2md.body_width = 0  # Don't wrap lines
        self.html2md.unicode_snob = True
        self.html2md.skip_internal_links = False

        # Elements to remove completely
        self.elements_to_remove = {
            "nav",
            "header",
            "footer",
            "aside",
            "script",
            "style",
            "noscript",
            "iframe",
            "form",
            "button",
            "input",
            "meta",
            'link[rel="stylesheet"]',
            'link[rel="canonical"]',
            'link[rel="alternate"]',
            'link[rel="icon"]',
            'link[rel="shortcut icon"]',
            "svg",
            "canvas",
            "video",
            "audio",
            "embed",
            "object",
            "ads",
            "advertisement",
            "banner",
            "popup",
            "modal",
            "social",
            "share",
            "comment",
            "disqus",
            "facebook",
            "twitter",
            "linkedin",
            "instagram",
            "youtube",
        }

        # Attributes to remove from elements
        self.attributes_to_remove = [
            "class",
            "id",
            "style",
            "onclick",
            "onload",
            "onmouseover",
            "data-*",
            "aria-*",
            "role",
            "tabindex",
            "hidden",
            "disabled",
        ]

    def extract_clean_html(self, soup: BeautifulSoup, base_url: str = "") -> str:
        """Extract clean HTML content, removing navigation and UI elements"""

        # Create a copy to avoid modifying original
        soup_copy = BeautifulSoup(str(soup), "html.parser")

        # Remove unwanted elements
        self._remove_unwanted_elements(soup_copy)

        # Clean remaining elements
        self._clean_elements(soup_copy)

        # Fix relative links to absolute
        if base_url:
            self._fix_links(soup_copy, base_url)

        # Extract main content area
        main_content = self._extract_main_content(soup_copy)

        return str(main_content)

    def extract_markdown(self, soup: BeautifulSoup, base_url: str = "") -> str:
        """Convert HTML to clean Markdown for AI consumption"""

        # Get clean HTML first
        clean_html = self.extract_clean_html(soup, base_url)

        # Convert to markdown
        markdown = self.html2md.handle(clean_html)

        # Post-process markdown
        markdown = self._clean_markdown(markdown)

        return markdown

    def extract_structured_json(
        self, soup: BeautifulSoup, url: str = ""
    ) -> Dict[str, Any]:
        """Extract structured JSON representation of the page"""

        title = self._extract_title(soup)
        description = self._extract_description(soup)
        sections = self._extract_sections(soup)
        code_blocks = self.extract_code_blocks(soup)
        links = self._extract_links(soup, url)

        return {
            "url": url,
            "title": title,
            "description": description,
            "sections": sections,
            "code_blocks": code_blocks,
            "internal_links": links["internal"],
            "external_links": links["external"],
            "last_extracted": self._get_timestamp(),
        }

    def extract_code_blocks(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract all code blocks with language and context information"""

        code_blocks = []

        # Find all <pre><code> blocks
        for pre in soup.find_all("pre"):
            code_tag = pre.find("code")
            if code_tag:
                # Extract language from class (e.g., "language-python")
                language = ""
                classes = code_tag.get("class", [])
                for cls in classes:
                    if cls.startswith("language-"):
                        language = cls.replace("language-", "")
                        break

                # Get code content
                code_content = code_tag.get_text(strip=True)

                # Get context (surrounding heading or paragraph)
                context = self._get_code_context(pre)

                code_blocks.append(
                    {
                        "language": language,
                        "code": code_content,
                        "context": context,
                        "line_count": len(code_content.split("\n")),
                        "character_count": len(code_content),
                    }
                )

        # Also look for inline code snippets
        for code in soup.find_all("code"):
            if not code.parent.name == "pre":  # Skip already processed
                code_content = code.get_text(strip=True)
                if len(code_content) > 10:  # Only meaningful snippets
                    context = self._get_code_context(code)
                    code_blocks.append(
                        {
                            "language": "text",  # Inline code
                            "code": code_content,
                            "context": context,
                            "line_count": 1,
                            "character_count": len(code_content),
                        }
                    )

        return code_blocks

    def _remove_unwanted_elements(self, soup: BeautifulSoup):
        """Remove navigation, scripts, styles, and other UI elements"""

        # Remove by tag name
        for tag_name in self.elements_to_remove:
            if tag_name.startswith("link["):
                # Handle CSS selector syntax
                rel_type = tag_name.split('rel="')[1].rstrip('"]')
                for link in soup.find_all("link", rel=rel_type):
                    link.decompose()
            else:
                for element in soup.find_all(tag_name):
                    element.decompose()

        # Remove elements with specific classes/IDs that indicate UI elements
        ui_indicators = [
            "nav",
            "navigation",
            "menu",
            "sidebar",
            "footer",
            "header",
            "banner",
            "advertisement",
            "ads",
            "social",
            "share",
            "comment",
            "disqus",
            "modal",
            "popup",
            "overlay",
        ]

        for element in soup.find_all(attrs={"class": True}):
            classes = element.get("class", [])
            for cls in classes:
                if any(indicator in cls.lower() for indicator in ui_indicators):
                    element.decompose()
                    break

        for element in soup.find_all(attrs={"id": True}):
            element_id = element.get("id", "").lower()
            if any(indicator in element_id for indicator in ui_indicators):
                element.decompose()

    def _clean_elements(self, soup: BeautifulSoup):
        """Clean remaining elements by removing unwanted attributes"""

        for element in soup.find_all():
            # Remove unwanted attributes
            for attr in self.attributes_to_remove:
                if attr.endswith("-*"):  # Wildcard attributes like data-*
                    prefix = attr[:-2]
                    attrs_to_remove = [
                        a for a in element.attrs.keys() if a.startswith(prefix)
                    ]
                    for a in attrs_to_remove:
                        del element.attrs[a]
                elif attr in element.attrs:
                    del element.attrs[attr]

    def _fix_links(self, soup: BeautifulSoup, base_url: str):
        """Convert relative links to absolute links"""

        for a in soup.find_all("a", href=True):
            href = a["href"]
            if not href.startswith(("http://", "https://", "mailto:", "#")):
                absolute_url = urljoin(base_url, href)
                a["href"] = absolute_url

    def _extract_main_content(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Extract the main content area from the page"""

        # Try common content selectors
        content_selectors = [
            "main",
            '[role="main"]',
            ".main-content",
            ".content",
            ".documentation",
            ".docs-content",
            ".article-content",
            ".post-content",
            "article",
            ".entry-content",
        ]

        for selector in content_selectors:
            try:
                if selector.startswith("."):
                    elements = soup.select(selector)
                else:
                    elements = soup.find_all(selector)

                if elements:
                    # Return the first matching element
                    return elements[0]
            except:
                continue

        # If no main content found, return body or entire soup
        body = soup.find("body")
        return body if body else soup

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract page title"""

        # Try title tag
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text(strip=True)

        # Try h1
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)

        # Try meta title
        meta_title = soup.find("meta", attrs={"property": "og:title"})
        if meta_title:
            return meta_title.get("content", "")

        return "Untitled Page"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract page description"""

        # Try meta description
        meta_desc = soup.find("meta", attrs={"name": "description"})
        if meta_desc:
            return meta_desc.get("content", "")

        # Try og:description
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        if og_desc:
            return og_desc.get("content", "")

        # Try first paragraph
        first_p = soup.find("p")
        if first_p:
            text = first_p.get_text(strip=True)
            if len(text) > 50:  # Only if substantial
                return text[:200] + "..." if len(text) > 200 else text

        return ""

    def _extract_sections(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extract hierarchical sections with headings"""

        sections = []
        current_section = None

        # Find all headings and their content
        headings = soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

        for heading in headings:
            level = int(heading.name[1])  # h1 -> 1, h2 -> 2, etc.
            title = heading.get_text(strip=True)

            # Skip if empty
            if not title:
                continue

            # Find content until next heading of same or higher level
            content = self._extract_section_content(heading, headings)

            section = {
                "level": level,
                "title": title,
                "content": content,
                "id": heading.get("id", ""),
                "subsections": [],
            }

            # Build hierarchy
            if level == 1:
                sections.append(section)
                current_section = section
            elif level == 2 and sections:
                sections[-1]["subsections"].append(section)
                current_section = section
            elif level > 2 and current_section:
                current_section["subsections"].append(section)

        return sections

    def _extract_section_content(self, heading: Tag, all_headings: List[Tag]) -> str:
        """Extract content for a section until the next heading"""

        content_parts = []
        current = heading.next_sibling

        # Get index of current heading
        try:
            current_index = all_headings.index(heading)
            next_heading = (
                all_headings[current_index + 1]
                if current_index + 1 < len(all_headings)
                else None
            )
        except ValueError:
            next_heading = None

        while current:
            if current == next_heading:
                break

            if isinstance(current, NavigableString):
                text = str(current).strip()
                if text:
                    content_parts.append(text)
            elif isinstance(current, Tag):
                if current.name in ["p", "div", "section", "article"]:
                    text = current.get_text(strip=True)
                    if text:
                        content_parts.append(text)
                elif current.name == "ul":
                    items = [li.get_text(strip=True) for li in current.find_all("li")]
                    if items:
                        content_parts.append("• " + "\n• ".join(items))
                elif current.name == "ol":
                    items = [li.get_text(strip=True) for li in current.find_all("li")]
                    if items:
                        content_parts.append("1. " + "\n2. ".join(items))

            current = current.next_sibling

        return "\n\n".join(content_parts)

    def _extract_links(
        self, soup: BeautifulSoup, base_url: str
    ) -> Dict[str, List[str]]:
        """Extract internal and external links"""

        internal_links = []
        external_links = []

        base_domain = urlparse(base_url).netloc if base_url else ""

        for a in soup.find_all("a", href=True):
            href = a["href"]

            # Skip anchors and mailto
            if href.startswith(("#", "mailto:")):
                continue

            # Normalize URL
            if not href.startswith(("http://", "https://")):
                full_url = urljoin(base_url, href)
            else:
                full_url = href

            link_domain = urlparse(full_url).netloc

            if link_domain == base_domain or not link_domain:
                internal_links.append(full_url)
            else:
                external_links.append(full_url)

        return {
            "internal": list(set(internal_links)),  # Remove duplicates
            "external": list(set(external_links)),
        }

    def _get_code_context(self, code_element: Tag) -> str:
        """Get contextual information around a code block"""

        context_parts = []

        # Look for preceding heading
        heading = None
        current = code_element.previous_sibling or code_element.parent
        for _ in range(5):  # Look up to 5 elements back
            if not current:
                break
            if isinstance(current, Tag) and current.name in [
                "h1",
                "h2",
                "h3",
                "h4",
                "h5",
                "h6",
            ]:
                heading = current.get_text(strip=True)
                break
            current = current.previous_sibling or current.parent

        if heading:
            context_parts.append(f"Section: {heading}")

        # Look for preceding paragraph
        paragraph = None
        current = code_element.previous_sibling or code_element.parent
        for _ in range(5):
            if not current:
                break
            if isinstance(current, Tag) and current.name == "p":
                text = current.get_text(strip=True)
                if len(text) > 20:  # Substantial paragraph
                    paragraph = text[:100] + "..." if len(text) > 100 else text
                    break
            current = current.previous_sibling or current.parent

        if paragraph:
            context_parts.append(f"Context: {paragraph}")

        return " | ".join(context_parts) if context_parts else "No context available"

    def _clean_markdown(self, markdown: str) -> str:
        """Clean and optimize markdown for AI consumption"""

        # Remove excessive empty lines
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

        # Fix code block language detection
        markdown = re.sub(
            r"```\n(.*?)\n```", self._fix_code_block, markdown, flags=re.DOTALL
        )

        # Remove HTML comments
        markdown = re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)

        # Clean up links
        markdown = re.sub(
            r"\[([^\]]+)\]\(([^\)]+)\)",
            lambda m: f"[{m.group(1)}]({m.group(2)})",
            markdown,
        )

        # Remove empty sections
        lines = markdown.split("\n")
        cleaned_lines = []
        for line in lines:
            if line.strip() or cleaned_lines:  # Keep empty lines only if content exists
                cleaned_lines.append(line)

        return "\n".join(cleaned_lines).strip()

    def _fix_code_block(self, match):
        """Fix code block formatting"""
        code = match.group(1)

        # Try to detect language from content
        language = ""
        if any(
            keyword in code.lower()
            for keyword in ["def ", "import ", "from ", "class "]
        ):
            language = "python"
        elif any(
            keyword in code.lower()
            for keyword in ["function", "const ", "let ", "var "]
        ):
            language = "javascript"
        elif any(keyword in code for keyword in ["<html", "<div", "<span"]):
            language = "html"
        elif any(keyword in code for keyword in ["SELECT", "FROM", "WHERE"]):
            language = "sql"

        return f"```{language}\n{code}\n```"

    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format"""
        from datetime import datetime

        return datetime.now().isoformat()
