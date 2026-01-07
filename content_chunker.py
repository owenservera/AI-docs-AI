"""
Content Chunker for AI-Friendly Documentation

This module splits documentation content into optimal chunks for AI/LLM
consumption, with configurable overlap and semantic boundary detection.
"""

import re
import hashlib
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup


class ContentChunker:
    """Chunks documentation content for AI consumption"""

    def __init__(self, chunk_size: int = 400, overlap: float = 0.15):
        self.chunk_size = chunk_size  # Target tokens per chunk
        self.overlap = overlap  # Overlap between chunks as fraction

    def chunk_by_sections(
        self, sections: List[Dict[str, Any]], base_url: str = ""
    ) -> List[Dict[str, Any]]:
        """Chunk content by document sections (semantic chunking)"""

        chunks = []

        for section in sections:
            # If section is small enough, keep it as one chunk
            section_text = section.get("content", "")
            section_title = section.get("title", "")
            combined_text = f"{section_title}\n\n{section_text}"

            if self._estimate_tokens(combined_text) <= self.chunk_size:
                chunks.append(
                    {
                        "id": self._generate_chunk_id(combined_text),
                        "content": combined_text,
                        "metadata": {
                            "source_section": section_title,
                            "level": section.get("level", 1),
                            "url": base_url,
                            "chunk_type": "section",
                            "token_count": self._estimate_tokens(combined_text),
                        },
                    }
                )
            else:
                # Split large sections into smaller chunks
                section_chunks = self._chunk_text_by_paragraphs(
                    combined_text, section_title, base_url
                )
                chunks.extend(section_chunks)

            # Recursively process subsections
            if section.get("subsections"):
                subsection_chunks = self.chunk_by_sections(
                    section["subsections"], base_url
                )
                chunks.extend(subsection_chunks)

        return chunks

    def chunk_by_tokens(
        self, content: str, title: str = "", url: str = ""
    ) -> List[Dict[str, Any]]:
        """Chunk content by token count with overlap"""

        chunks = []

        # Simple word-based token estimation (in practice, use proper tokenizer)
        words = content.split()
        if not words:
            return chunks

        overlap_words = int(self.chunk_size * self.overlap)
        step_size = self.chunk_size - overlap_words

        for i in range(0, len(words), step_size):
            chunk_words = words[i : i + self.chunk_size]
            chunk_text = " ".join(chunk_words)

            # Skip very short chunks at the end
            if len(chunk_words) < 50 and i > 0:
                continue

            chunk_metadata = {
                "id": self._generate_chunk_id(chunk_text),
                "content": chunk_text,
                "metadata": {
                    "title": title,
                    "url": url,
                    "chunk_type": "token_based",
                    "chunk_index": len(chunks),
                    "start_word": i,
                    "end_word": min(i + self.chunk_size, len(words)),
                    "token_count": len(chunk_words),
                    "overlap_words": overlap_words if i > 0 else 0,
                },
            }

            chunks.append(chunk_metadata)

        return chunks

    def chunk_markdown_file(
        self, markdown_content: str, url: str = ""
    ) -> List[Dict[str, Any]]:
        """Chunk markdown content by headers and sections"""

        chunks = []

        # Split by headers
        sections = self._split_markdown_by_headers(markdown_content)

        for section in sections:
            section_text = section["content"]
            token_count = self._estimate_tokens(section_text)

            if token_count <= self.chunk_size:
                # Keep section as one chunk
                chunks.append(
                    {
                        "id": self._generate_chunk_id(section_text),
                        "content": section_text,
                        "metadata": {
                            "header": section["header"],
                            "level": section["level"],
                            "url": url,
                            "chunk_type": "markdown_section",
                            "token_count": token_count,
                        },
                    }
                )
            else:
                # Split large sections
                section_chunks = self._chunk_text_by_paragraphs(
                    section_text, section["header"], url
                )
                chunks.extend(section_chunks)

        return chunks

    def create_chunk_index(self, chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create an index of all chunks for easy lookup"""

        index = {
            "total_chunks": len(chunks),
            "total_tokens": sum(chunk["metadata"]["token_count"] for chunk in chunks),
            "chunk_types": {},
            "chunks_by_type": {},
            "chunk_ids": [],
            "generated_at": self._get_timestamp(),
        }

        for chunk in chunks:
            chunk_id = chunk["id"]
            chunk_type = chunk["metadata"]["chunk_type"]
            token_count = chunk["metadata"]["token_count"]

            index["chunk_ids"].append(chunk_id)

            # Track by type
            if chunk_type not in index["chunk_types"]:
                index["chunk_types"][chunk_type] = {"count": 0, "total_tokens": 0}
            index["chunk_types"][chunk_type]["count"] += 1
            index["chunk_types"][chunk_type]["total_tokens"] += token_count

            if chunk_type not in index["chunks_by_type"]:
                index["chunks_by_type"][chunk_type] = []
            index["chunks_by_type"][chunk_type].append(chunk_id)

        return index

    def search_chunks(
        self, chunks: List[Dict[str, Any]], query: str, limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Simple semantic search over chunks"""

        query_lower = query.lower()
        results = []

        for chunk in chunks:
            content = chunk["content"].lower()
            score = 0

            # Simple scoring: count query terms
            query_terms = query_lower.split()
            for term in query_terms:
                score += content.count(term)

            if score > 0:
                results.append(
                    {
                        "chunk_id": chunk["id"],
                        "score": score,
                        "content_preview": chunk["content"][:200] + "...",
                        "metadata": chunk["metadata"],
                    }
                )

        # Sort by score and return top results
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:limit]

    def _chunk_text_by_paragraphs(
        self, text: str, context: str = "", url: str = ""
    ) -> List[Dict[str, Any]]:
        """Split text by paragraphs when sections are too large"""

        # Split by double newlines (paragraphs)
        paragraphs = re.split(r"\n\s*\n", text.strip())
        chunks = []

        current_chunk = ""
        current_tokens = 0

        for para in paragraphs:
            para_tokens = self._estimate_tokens(para)

            # If adding this paragraph would exceed chunk size
            if current_tokens + para_tokens > self.chunk_size and current_chunk:
                # Save current chunk
                chunks.append(
                    {
                        "id": self._generate_chunk_id(current_chunk),
                        "content": current_chunk.strip(),
                        "metadata": {
                            "context": context,
                            "url": url,
                            "chunk_type": "paragraph_group",
                            "token_count": current_tokens,
                        },
                    }
                )

                # Start new chunk with overlap
                overlap_text = self._get_overlap_text(current_chunk, paragraphs)
                current_chunk = overlap_text + "\n\n" + para if overlap_text else para
                current_tokens = self._estimate_tokens(current_chunk)
            else:
                # Add paragraph to current chunk
                if current_chunk:
                    current_chunk += "\n\n" + para
                else:
                    current_chunk = para
                current_tokens += para_tokens

        # Add final chunk
        if current_chunk.strip():
            chunks.append(
                {
                    "id": self._generate_chunk_id(current_chunk),
                    "content": current_chunk.strip(),
                    "metadata": {
                        "context": context,
                        "url": url,
                        "chunk_type": "paragraph_group",
                        "token_count": current_tokens,
                    },
                }
            )

        return chunks

    def _split_markdown_by_headers(self, markdown: str) -> List[Dict[str, Any]]:
        """Split markdown content by headers"""

        sections = []
        lines = markdown.split("\n")
        current_section = {"header": "", "level": 0, "content": ""}

        for line in lines:
            # Check if line is a header
            header_match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
            if header_match:
                # Save previous section if it has content
                if current_section["content"].strip():
                    sections.append(current_section)

                # Start new section
                level = len(header_match.group(1))
                header = header_match.group(2)
                current_section = {
                    "header": header,
                    "level": level,
                    "content": line + "\n",
                }
            else:
                # Add line to current section
                current_section["content"] += line + "\n"

        # Add final section
        if current_section["content"].strip():
            sections.append(current_section)

        return sections

    def _estimate_tokens(self, text: str) -> int:
        """Rough token estimation (words + punctuation)"""

        # Simple estimation: ~4/5 characters per token
        char_count = len(text)
        return max(1, char_count // 4)

    def _generate_chunk_id(self, content: str) -> str:
        """Generate unique chunk ID"""

        # Use first 50 chars + hash for uniqueness
        prefix = content[:50].replace("\n", " ").strip()
        hash_suffix = hashlib.md5(content.encode()).hexdigest()[:8]
        return f"chunk_{hash_suffix}"

    def _get_overlap_text(self, text: str, paragraphs: List[str]) -> str:
        """Get overlap text from end of current chunk"""

        if not text or self.overlap == 0:
            return ""

        # Get last few sentences/paragraphs for overlap
        overlap_chars = int(len(text) * self.overlap)
        overlap_text = text[-overlap_chars:]

        # Try to start at a sentence boundary
        sentences = re.split(r"[.!?]+\s+", overlap_text)
        if len(sentences) > 1:
            # Keep last 2-3 sentences
            overlap_text = " ".join(sentences[-min(3, len(sentences)) :])

        return overlap_text.strip()

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime

        return datetime.now().isoformat()

    def set_chunk_parameters(self, chunk_size: int = None, overlap: float = None):
        """Update chunking parameters"""

        if chunk_size is not None:
            self.chunk_size = chunk_size
        if overlap is not None:
            self.overlap = overlap
