"""
AI Sitemap Generator for Documentation

This module generates AI-friendly sitemaps (llms.txt, .ai-sitemap) that help
LLMs and AI agents discover and prioritize documentation content.
"""

import json
from typing import List, Dict, Any, Optional
from datetime import datetime


class AISitemapGenerator:
    """Generates AI-friendly sitemaps and indexes"""

    def __init__(self):
        self.templates = {
            "llms_txt": """# {site_name} Documentation

This is a machine-readable sitemap for AI agents and LLMs to efficiently discover and navigate the documentation.

## Site Information
- **Base URL**: {base_url}
- **Total Pages**: {total_pages}
- **Last Updated**: {last_updated}
- **Generated**: {generated_at}

## Content Types
{type_summary}

## Priority Pages
{priority_pages}

## All Pages
{page_list}

## API Endpoints
{api_endpoints}

## Search Tips
- Use the priority pages for high-level understanding
- Reference pages are good for specific features
- API documentation is best for technical implementation
- Tutorial pages provide step-by-step guidance

---

*This sitemap was generated for AI agents. Last updated: {generated_at}*
""",
            "ai_sitemap_json": {
                "@context": "https://schema.org",
                "@type": "SiteNavigationElement",
                "name": "{site_name} AI Sitemap",
                "description": "Machine-readable sitemap for AI agents and LLMs",
                "url": "{base_url}",
                "dateCreated": "{generated_at}",
                "mainEntity": [],
            },
        }

    def generate_llms_txt(
        self,
        pages_metadata: List[Dict[str, Any]],
        site_name: str = "Documentation",
        base_url: str = "",
    ) -> str:
        """Generate llms.txt format sitemap"""

        # Sort pages by priority
        sorted_pages = self._sort_pages_by_priority(pages_metadata)

        # Generate content sections
        type_summary = self._generate_type_summary(pages_metadata)
        priority_pages = self._generate_priority_list(sorted_pages[:10])
        page_list = self._generate_page_list(sorted_pages)
        api_endpoints = self._generate_api_endpoints(pages_metadata)

        # Fill template
        content = self.templates["llms_txt"].format(
            site_name=site_name,
            base_url=base_url,
            total_pages=len(pages_metadata),
            last_updated=self._get_latest_update(pages_metadata),
            generated_at=datetime.now().isoformat(),
            type_summary=type_summary,
            priority_pages=priority_pages,
            page_list=page_list,
            api_endpoints=api_endpoints,
        )

        return content

    def generate_ai_sitemap_json(
        self,
        pages_metadata: List[Dict[str, Any]],
        site_name: str = "Documentation",
        base_url: str = "",
    ) -> Dict[str, Any]:
        """Generate JSON format AI sitemap"""

        sitemap = self.templates["ai_sitemap_json"].copy()
        sitemap["name"] = sitemap["name"].format(site_name=site_name)
        sitemap["description"] = sitemap["description"].format(site_name=site_name)
        sitemap["url"] = base_url or sitemap["url"]
        sitemap["dateCreated"] = sitemap["dateCreated"].format(
            generated_at=datetime.now().isoformat()
        )

        # Add pages as main entities
        for page in pages_metadata:
            page_entity = {
                "@type": "WebPage",
                "name": page.get("title", "Untitled"),
                "url": page.get("url", ""),
                "description": page.get("description", ""),
                "keywords": page.get("keywords", [])[:5],  # Limit keywords
                "dateModified": page.get("last_updated"),
                "additionalProperty": [
                    {
                        "@type": "PropertyValue",
                        "name": "contentType",
                        "value": page.get("content_type", "unknown"),
                    },
                    {
                        "@type": "PropertyValue",
                        "name": "wordCount",
                        "value": page.get("word_count", 0),
                    },
                    {
                        "@type": "PropertyValue",
                        "name": "readingTime",
                        "value": page.get("reading_time", 0),
                    },
                ],
            }

            # Add priority score
            priority = self._calculate_page_priority(page)
            page_entity["additionalProperty"].append(
                {"@type": "PropertyValue", "name": "aiPriority", "value": priority}
            )

            sitemap["mainEntity"].append(page_entity)

        return sitemap

    def generate_navigation_index(
        self, pages_metadata: List[Dict[str, Any]], base_url: str = ""
    ) -> str:
        """Generate human and AI-readable navigation index"""

        # Group pages by content type
        grouped_pages = {}
        for page in pages_metadata:
            content_type = page.get("content_type", "general")
            if content_type not in grouped_pages:
                grouped_pages[content_type] = []
            grouped_pages[content_type].append(page)

        # Generate HTML index
        html_parts = []

        html_parts.append(f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI-Friendly Documentation Index</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f8f9fa;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            text-align: center;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .content-type {{
            background: white;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .content-type-header {{
            background: #007acc;
            color: white;
            padding: 15px 20px;
            margin: 0;
            font-size: 1.2em;
        }}
        .page-list {{
            padding: 0;
            margin: 0;
            list-style: none;
        }}
        .page-item {{
            border-bottom: 1px solid #eee;
            transition: background 0.2s;
        }}
        .page-item:hover {{
            background: #f8f9fa;
        }}
        .page-link {{
            display: block;
            padding: 15px 20px;
            text-decoration: none;
            color: #333;
        }}
        .page-title {{
            font-weight: 600;
            margin-bottom: 5px;
        }}
        .page-meta {{
            font-size: 0.9em;
            color: #666;
        }}
        .ai-priority {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 500;
        }}
        .priority-high {{ background: #d4edda; color: #155724; }}
        .priority-medium {{ background: #fff3cd; color: #856404; }}
        .priority-low {{ background: #f8d7da; color: #721c24; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🤖 AI-Friendly Documentation Index</h1>
        <p>This index is optimized for AI agents and LLMs to efficiently navigate the documentation.</p>
        <p><strong>Site:</strong> {base_url or "Documentation"}</p>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>

    <div class="stats">
        <div class="stat-card">
            <h3>{len(pages_metadata)}</h3>
            <p>Total Pages</p>
        </div>
        <div class="stat-card">
            <h3>{len(grouped_pages)}</h3>
            <p>Content Types</p>
        </div>
        <div class="stat-card">
            <h3>{sum(p.get("word_count", 0) for p in pages_metadata):,}</h3>
            <p>Total Words</p>
        </div>
        <div class="stat-card">
            <h3>{self._get_latest_update(pages_metadata) or "Unknown"}</h3>
            <p>Last Updated</p>
        </div>
    </div>
""")

        # Add content type sections
        for content_type, pages in grouped_pages.items():
            # Sort pages by priority
            pages_sorted = sorted(
                pages, key=self._calculate_page_priority, reverse=True
            )

            html_parts.append(f"""
    <div class="content-type">
        <h2 class="content-type-header">{content_type.replace("_", " ").title()} ({len(pages)} pages)</h2>
        <ul class="page-list">""")

            for page in pages_sorted:
                priority_class = self._get_priority_class(
                    self._calculate_page_priority(page)
                )
                reading_time = page.get("reading_time", 0)
                word_count = page.get("word_count", 0)

                html_parts.append(f"""
            <li class="page-item">
                <a href="{page.get("url", "#")}" class="page-link">
                    <div class="page-title">{page.get("title", "Untitled")}</div>
                    <div class="page-meta">
                        <span class="ai-priority {priority_class}">Priority: {self._calculate_page_priority(page)}</span>
                        • {reading_time} min read • {word_count:,} words
                    </div>
                    {f'<div class="page-description">{page.get("description", "")[:150]}...</div>' if page.get("description") else ""}
                </a>
            </li>""")

            html_parts.append("""
        </ul>
    </div>
""")

        html_parts.append("""
</body>
</html>""")

        return "\n".join(html_parts)

    def generate_summary_report(
        self, pages_metadata: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Generate summary statistics for the documentation set"""

        total_words = sum(p.get("word_count", 0) for p in pages_metadata)
        total_reading_time = sum(p.get("reading_time", 0) for p in pages_metadata)
        content_types = {}

        for page in pages_metadata:
            ct = page.get("content_type", "unknown")
            if ct not in content_types:
                content_types[ct] = {
                    "count": 0,
                    "total_words": 0,
                    "avg_reading_time": 0,
                }
            content_types[ct]["count"] += 1
            content_types[ct]["total_words"] += page.get("word_count", 0)

        # Calculate averages
        for ct_data in content_types.values():
            if ct_data["count"] > 0:
                ct_data["avg_reading_time"] = total_reading_time / len(pages_metadata)

        return {
            "total_pages": len(pages_metadata),
            "total_words": total_words,
            "total_reading_time_minutes": total_reading_time,
            "content_type_breakdown": content_types,
            "average_page_words": total_words // len(pages_metadata)
            if pages_metadata
            else 0,
            "average_reading_time": total_reading_time / len(pages_metadata)
            if pages_metadata
            else 0,
            "last_updated": self._get_latest_update(pages_metadata),
            "generated_at": datetime.now().isoformat(),
        }

    def _sort_pages_by_priority(
        self, pages_metadata: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Sort pages by AI priority score"""

        return sorted(pages_metadata, key=self._calculate_page_priority, reverse=True)

    def _calculate_page_priority(self, page: Dict[str, Any]) -> float:
        """Calculate AI priority score for a page"""

        score = 0.0

        # Content type priority
        content_type_weights = {
            "api_reference": 1.0,
            "how_to": 0.9,
            "tutorial": 0.8,
            "reference": 0.7,
            "faq": 0.6,
            "troubleshooting": 0.6,
            "conceptual": 0.5,
            "general": 0.3,
        }

        ct = page.get("content_type", "general")
        score += content_type_weights.get(ct, 0.3)

        # Title quality (shorter, more descriptive titles score higher)
        title = page.get("title", "")
        if title:
            title_length = len(title.split())
            if 3 <= title_length <= 10:
                score += 0.2
            elif title_length > 15:
                score -= 0.1

        # Description quality
        description = page.get("description", "")
        if len(description) > 50:
            score += 0.1

        # Code content (higher for technical docs)
        code_blocks = page.get("code_blocks_count", 0)
        if code_blocks > 0:
            score += min(0.2, code_blocks * 0.05)

        # Freshness (recently updated pages score higher)
        last_updated = page.get("last_updated")
        if last_updated:
            try:
                # Simple heuristic: if it has a date, give slight boost
                score += 0.05
            except:
                pass

        return min(1.0, score)  # Cap at 1.0

    def _generate_type_summary(self, pages_metadata: List[Dict[str, Any]]) -> str:
        """Generate content type summary for llms.txt"""

        content_types = {}
        for page in pages_metadata:
            ct = page.get("content_type", "unknown")
            content_types[ct] = content_types.get(ct, 0) + 1

        summary_lines = []
        for ct, count in sorted(
            content_types.items(), key=lambda x: x[1], reverse=True
        ):
            summary_lines.append(f"- **{ct.replace('_', ' ').title()}**: {count} pages")

        return "\n".join(summary_lines)

    def _generate_priority_list(self, priority_pages: List[Dict[str, Any]]) -> str:
        """Generate priority pages list for llms.txt"""

        lines = []
        for i, page in enumerate(priority_pages[:10], 1):
            title = page.get("title", "Untitled")
            url = page.get("url", "")
            ct = page.get("content_type", "unknown")
            lines.append(f"{i}. **{title}** ({ct.replace('_', ' ')}) - {url}")

        return "\n".join(lines)

    def _generate_page_list(self, sorted_pages: List[Dict[str, Any]]) -> str:
        """Generate complete page list for llms.txt"""

        lines = []
        for page in sorted_pages:
            title = page.get("title", "Untitled")
            url = page.get("url", "")
            ct = page.get("content_type", "unknown")
            lines.append(f"- [{title}]({url}) - {ct.replace('_', ' ')}")

        return "\n".join(lines)

    def _generate_api_endpoints(self, pages_metadata: List[Dict[str, Any]]) -> str:
        """Extract and list API endpoints for llms.txt"""

        api_pages = [
            p for p in pages_metadata if p.get("content_type") == "api_reference"
        ]

        if not api_pages:
            return "No dedicated API documentation pages found."

        endpoints = []
        for page in api_pages:
            title = page.get("title", "")
            url = page.get("url", "")
            entities = page.get("entities", {}).get("api_endpoints", [])
            if entities:
                endpoints.append(f"- **{title}**: {url}")
                for endpoint in entities[:5]:  # Limit to 5 per page
                    endpoints.append(f"  - `{endpoint}`")

        return (
            "\n".join(endpoints)
            if endpoints
            else "API endpoints found in documentation pages."
        )

    def _get_latest_update(self, pages_metadata: List[Dict[str, Any]]) -> Optional[str]:
        """Get the latest update date from all pages"""

        dates = []
        for page in pages_metadata:
            date_str = page.get("last_updated")
            if date_str:
                try:
                    # Try to parse date (assuming ISO format)
                    dates.append(date_str)
                except:
                    continue

        return max(dates) if dates else None

    def _get_priority_class(self, priority: float) -> str:
        """Get CSS class for priority display"""

        if priority >= 0.8:
            return "priority-high"
        elif priority >= 0.6:
            return "priority-medium"
        else:
            return "priority-low"
