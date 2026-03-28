from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import time
from pathlib import Path
from typing import Callable, Optional

from langchain_core.documents import Document


class MemoryStore:
    def __init__(
        self,
        memory_dir: Path,
        *,
        stopwords: set[str],
        official_source_hints: tuple[str, ...],
        low_trust_source_hints: tuple[str, ...],
    ) -> None:
        self.memory_dir = memory_dir
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.db_path = self.memory_dir / "memory.db"
        self.stopwords = set(stopwords)
        self.official_source_hints = tuple(official_source_hints)
        self.low_trust_source_hints = tuple(low_trust_source_hints)
        self.conn = sqlite3.connect(str(self.db_path))
        self.conn.row_factory = sqlite3.Row
        self.ensure_schema()

    def close(self) -> None:
        self.conn.close()

    def ensure_schema(self) -> None:
        self.conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS sources (
                source TEXT PRIMARY KEY,
                source_signature TEXT NOT NULL,
                authority_score INTEGER NOT NULL,
                authority_label TEXT NOT NULL,
                law_refs TEXT NOT NULL,
                years TEXT NOT NULL,
                slopes TEXT NOT NULL,
                keywords TEXT NOT NULL,
                summary TEXT NOT NULL,
                top_snippets TEXT NOT NULL,
                updated_at REAL NOT NULL
            );

            CREATE TABLE IF NOT EXISTS snippets (
                snippet_hash TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                page INTEGER,
                snippet TEXT NOT NULL,
                term_index TEXT NOT NULL,
                law_refs TEXT NOT NULL,
                years TEXT NOT NULL,
                slopes TEXT NOT NULL,
                keywords TEXT NOT NULL,
                authority_score INTEGER NOT NULL,
                authority_label TEXT NOT NULL,
                updated_at REAL NOT NULL
            );

            CREATE INDEX IF NOT EXISTS idx_snippets_source ON snippets(source);
            CREATE INDEX IF NOT EXISTS idx_snippets_page ON snippets(source, page);

            CREATE TABLE IF NOT EXISTS topics (
                topic_key TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                source_signature TEXT NOT NULL,
                article_path TEXT,
                content TEXT NOT NULL,
                local_context TEXT,
                exact_evidence TEXT,
                target_items TEXT NOT NULL,
                used_sources TEXT NOT NULL,
                updated_at REAL NOT NULL
            );
            """
        )
        self.conn.commit()

    @staticmethod
    def normalize_source_path(value: object) -> Optional[str]:
        if not value:
            return None
        return str(Path(str(value)).resolve())

    @staticmethod
    def normalize_for_match(text: str) -> str:
        return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9:./ -]+", " ", text.lower())).strip()

    @staticmethod
    def normalize_slope(text: str) -> str:
        return re.sub(r"\s*[:/-]\s*", ":", text.strip())

    @staticmethod
    def unique_preserve_order(items: list[str]) -> list[str]:
        seen = set()
        result = []
        for item in items:
            if item and item not in seen:
                seen.add(item)
                result.append(item)
        return result

    def extract_law_refs(self, text: str) -> list[str]:
        matches = re.findall(r"\b(?:bp|pd|ra)\s*\d+\b", text.lower())
        return self.unique_preserve_order([re.sub(r"\s+", " ", match).strip() for match in matches])

    def extract_years(self, text: str) -> list[str]:
        return self.unique_preserve_order(re.findall(r"\b(?:19|20)\d{2}\b", text.lower()))

    def extract_slopes(self, text: str) -> list[str]:
        slopes = re.findall(r"\b\d+\s*[:/-]\s*\d+\b", text.lower())
        return self.unique_preserve_order([self.normalize_slope(slope) for slope in slopes])

    def extract_keywords(self, text: str, limit: int = 24) -> list[str]:
        tokens = re.findall(r"\b[a-z][a-z0-9.-]{2,}\b", text.lower())
        keywords = []
        for token in tokens:
            if token in self.stopwords:
                continue
            keywords.append(token)
        return self.unique_preserve_order(keywords)[:limit]

    def extract_query_terms(self, query: str) -> list[str]:
        terms = []
        terms.extend(self.extract_law_refs(query))
        terms.extend(self.extract_slopes(query))
        terms.extend(self.extract_years(query))
        terms.extend(self.extract_keywords(query, limit=16))
        return self.unique_preserve_order(terms)

    def source_authority_score(self, source_text: str, query_terms: Optional[list[str]] = None) -> tuple[int, str]:
        source_lower = self.normalize_for_match(source_text)
        score = 0

        for hint in self.official_source_hints:
            if hint in source_lower:
                score += 8

        for hint in self.low_trust_source_hints:
            if hint in source_lower:
                score -= 10

        for term in query_terms or []:
            if term in source_lower:
                score += 5

        if score >= 18:
            label = "PRIMARY OFFICIAL"
        elif score >= 8:
            label = "HIGH AUTHORITY"
        elif score >= 0:
            label = "MEDIUM AUTHORITY"
        else:
            label = "LOW AUTHORITY"

        return score, label

    def compute_source_signature(self, source: str) -> str:
        path = Path(source)
        if path.exists():
            stat = path.stat()
            raw = f"{path.resolve()}|{stat.st_size}|{stat.st_mtime_ns}"
        else:
            raw = source
        return hashlib.sha1(raw.encode("utf-8")).hexdigest()

    def compute_topic_key(self, title: str) -> str:
        return hashlib.sha1(title.strip().lower().encode("utf-8")).hexdigest()

    def build_source_summary(
        self,
        source: str,
        authority_label: str,
        law_refs: list[str],
        years: list[str],
        slopes: list[str],
        keywords: list[str],
        snippets: list[tuple[int | None, str, int]],
    ) -> tuple[str, list[str]]:
        ranked = sorted(snippets, key=lambda item: item[2], reverse=True)
        selected = []
        top_snippets = []
        seen_pages = set()

        for page, snippet, _score in ranked:
            page_key = page if page is not None else -1
            if page_key in seen_pages:
                continue
            seen_pages.add(page_key)
            selected.append((page, snippet))
            top_snippets.append(snippet[:320])
            if len(selected) >= 4:
                break

        lines = [
            f"Source: {Path(source).name}",
            f"Authority: {authority_label}",
            f"Law refs: {', '.join(law_refs) if law_refs else 'None detected'}",
            f"Years: {', '.join(years) if years else 'None detected'}",
            f"Slopes: {', '.join(slopes) if slopes else 'None detected'}",
            f"Keywords: {', '.join(keywords[:12]) if keywords else 'None detected'}",
        ]
        if selected:
            lines.append("Key excerpts:")
            for page, snippet in selected:
                page_label = f"page {page + 1}" if isinstance(page, int) else "page ?"
                lines.append(f"- {page_label}: {snippet[:280]}")

        return "\n".join(lines), top_snippets

    def refresh_from_vectorstore(
        self,
        vectorstore,
        *,
        batch_size: int = 5000,
        force: bool = False,
        progress_callback: Optional[Callable[[str], None]] = None,
    ) -> dict[str, int]:
        if vectorstore is None:
            return {"sources_seen": 0, "sources_refreshed": 0, "sources_skipped": 0, "snippets_written": 0}

        stats = {
            "sources_seen": 0,
            "sources_refreshed": 0,
            "sources_skipped": 0,
            "snippets_written": 0,
        }

        total_chunks = vectorstore._collection.count()
        offset = 0
        chunks_by_source: dict[str, list[tuple[int | None, str]]] = {}

        while offset < total_chunks:
            batch = vectorstore._collection.get(
                include=["documents", "metadatas"],
                limit=batch_size,
                offset=offset,
            )
            for snippet, metadata in zip(batch.get("documents") or [], batch.get("metadatas") or []):
                source = self.normalize_source_path((metadata or {}).get("source"))
                if not source or not snippet:
                    continue
                page = (metadata or {}).get("page")
                snippet_text = " ".join(str(snippet).split()).strip()
                if not snippet_text:
                    continue
                chunks_by_source.setdefault(source, []).append((page, snippet_text))
            offset += batch_size

        now = time.time()

        for source, entries in chunks_by_source.items():
            stats["sources_seen"] += 1
            source_signature = self.compute_source_signature(source)
            existing = self.conn.execute(
                "SELECT source_signature FROM sources WHERE source = ?",
                (source,),
            ).fetchone()

            if not force and existing and existing["source_signature"] == source_signature:
                stats["sources_skipped"] += 1
                continue

            self.conn.execute("DELETE FROM snippets WHERE source = ?", (source,))

            source_text = f"{source}\n" + "\n".join(snippet for _, snippet in entries[:24])
            law_refs = self.extract_law_refs(source_text)
            years = self.extract_years(source_text)
            slopes = self.extract_slopes(source_text)
            keywords = self.extract_keywords(source_text, limit=32)
            authority_score, authority_label = self.source_authority_score(source, law_refs + years + slopes)

            snippet_summaries = []
            for page, snippet in entries:
                law_refs_chunk = self.extract_law_refs(snippet)
                years_chunk = self.extract_years(snippet)
                slopes_chunk = self.extract_slopes(snippet)
                keywords_chunk = self.extract_keywords(snippet, limit=24)
                term_index = " ".join(self.unique_preserve_order(law_refs_chunk + years_chunk + slopes_chunk + keywords_chunk))
                signal = (
                    len(law_refs_chunk) * 6
                    + len(years_chunk) * 3
                    + len(slopes_chunk) * 5
                    + min(len(keywords_chunk), 8)
                )
                snippet_hash = hashlib.sha1(
                    f"{source}|{page}|{snippet}".encode("utf-8")
                ).hexdigest()
                self.conn.execute(
                    """
                    INSERT OR REPLACE INTO snippets (
                        snippet_hash, source, page, snippet, term_index, law_refs, years,
                        slopes, keywords, authority_score, authority_label, updated_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        snippet_hash,
                        source,
                        page if isinstance(page, int) else None,
                        snippet,
                        term_index,
                        json.dumps(law_refs_chunk),
                        json.dumps(years_chunk),
                        json.dumps(slopes_chunk),
                        json.dumps(keywords_chunk),
                        authority_score,
                        authority_label,
                        now,
                    ),
                )
                stats["snippets_written"] += 1
                snippet_summaries.append((page if isinstance(page, int) else None, snippet, signal))

            summary, top_snippets = self.build_source_summary(
                source,
                authority_label,
                law_refs,
                years,
                slopes,
                keywords,
                snippet_summaries,
            )

            self.conn.execute(
                """
                INSERT OR REPLACE INTO sources (
                    source, source_signature, authority_score, authority_label, law_refs,
                    years, slopes, keywords, summary, top_snippets, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    source,
                    source_signature,
                    authority_score,
                    authority_label,
                    json.dumps(law_refs),
                    json.dumps(years),
                    json.dumps(slopes),
                    json.dumps(keywords),
                    summary,
                    json.dumps(top_snippets),
                    now,
                ),
            )
            stats["sources_refreshed"] += 1

            if progress_callback and (stats["sources_refreshed"] % 25 == 0):
                progress_callback(
                    f"  [Memory] Refreshed {stats['sources_refreshed']}/{stats['sources_seen']} sources..."
                )

        self.conn.commit()
        return stats

    def search_snippets(self, query: str, limit: int = 8) -> list[Document]:
        query_terms = self.extract_query_terms(query)
        if not query_terms:
            return []

        clauses = []
        params = []
        for term in query_terms[:12]:
            clauses.append("term_index LIKE ?")
            params.append(f"%{term}%")

        sql = (
            "SELECT snippet_hash, source, page, snippet, term_index, authority_score, authority_label "
            "FROM snippets WHERE " + " OR ".join(clauses) + " LIMIT 400"
        )
        rows = self.conn.execute(sql, params).fetchall()

        ranked = []
        for row in rows:
            haystack = self.normalize_for_match(f"{row['source']} {row['snippet']} {row['term_index']}")
            score = int(row["authority_score"])
            for term in query_terms:
                if term in haystack:
                    score += 5
            if any(re.fullmatch(r"\d+:\d+", term) for term in query_terms):
                score += sum(3 for term in query_terms if re.fullmatch(r"\d+:\d+", term) and term in haystack)
            ranked.append((score, row))

        ranked.sort(key=lambda item: item[0], reverse=True)
        documents = []
        seen = set()
        for score, row in ranked:
            key = (row["source"], row["page"], row["snippet"][:120])
            if key in seen:
                continue
            seen.add(key)
            documents.append(
                Document(
                    page_content=row["snippet"],
                    metadata={
                        "source": row["source"],
                        "page": row["page"],
                        "_memory_kind": "exact_snippet",
                        "_authority_label": row["authority_label"],
                        "_authority_score": row["authority_score"],
                        "_relevance_score": score,
                    },
                )
            )
            if len(documents) >= limit:
                break

        return documents

    def search_source_summaries(self, query: str, limit: int = 4) -> list[Document]:
        query_terms = self.extract_query_terms(query)
        if not query_terms:
            return []

        clauses = []
        params = []
        for term in query_terms[:12]:
            clauses.append("summary LIKE ?")
            params.append(f"%{term}%")
            clauses.append("keywords LIKE ?")
            params.append(f"%{term}%")

        sql = (
            "SELECT source, summary, authority_score, authority_label, law_refs, years, slopes "
            "FROM sources WHERE " + " OR ".join(clauses) + " LIMIT 120"
        )
        rows = self.conn.execute(sql, params).fetchall()

        ranked = []
        for row in rows:
            haystack = self.normalize_for_match(f"{row['source']} {row['summary']}")
            score = int(row["authority_score"])
            for term in query_terms:
                if term in haystack:
                    score += 4
            ranked.append((score, row))

        ranked.sort(key=lambda item: item[0], reverse=True)
        documents = []
        seen_sources = set()
        for score, row in ranked:
            if row["source"] in seen_sources:
                continue
            seen_sources.add(row["source"])
            documents.append(
                Document(
                    page_content=row["summary"],
                    metadata={
                        "source": row["source"],
                        "_memory_kind": "source_summary",
                        "_authority_label": row["authority_label"],
                        "_authority_score": row["authority_score"],
                        "_relevance_score": score,
                    },
                )
            )
            if len(documents) >= limit:
                break
        return documents

    def build_topic_source_signature(self, documents: list[Document]) -> str:
        parts = []
        for doc in documents:
            source = self.normalize_source_path(doc.metadata.get("source"))
            if not source:
                continue
            row = self.conn.execute(
                "SELECT source_signature FROM sources WHERE source = ?",
                (source,),
            ).fetchone()
            source_signature = row["source_signature"] if row else self.compute_source_signature(source)
            page = doc.metadata.get("page")
            memory_kind = doc.metadata.get("_memory_kind", "")
            parts.append(f"{source_signature}|{page}|{memory_kind}")
        digest = hashlib.sha1("|".join(sorted(set(parts))).encode("utf-8")).hexdigest()
        return digest

    def get_topic_cache(self, title: str, source_signature: str) -> Optional[dict]:
        topic_key = self.compute_topic_key(title)
        row = self.conn.execute(
            """
            SELECT title, source_signature, article_path, content, local_context,
                   exact_evidence, target_items, used_sources, updated_at
            FROM topics WHERE topic_key = ?
            """,
            (topic_key,),
        ).fetchone()
        if row is None or row["source_signature"] != source_signature:
            return None

        return {
            "title": row["title"],
            "source_signature": row["source_signature"],
            "article_path": row["article_path"],
            "content": row["content"],
            "local_context": row["local_context"],
            "exact_evidence": row["exact_evidence"],
            "target_items": json.loads(row["target_items"]),
            "used_sources": json.loads(row["used_sources"]),
            "updated_at": row["updated_at"],
        }

    def set_topic_cache(
        self,
        *,
        title: str,
        source_signature: str,
        article_path: str,
        content: str,
        local_context: str,
        exact_evidence: str,
        target_items: list[str],
        used_sources: list[str],
    ) -> None:
        topic_key = self.compute_topic_key(title)
        self.conn.execute(
            """
            INSERT OR REPLACE INTO topics (
                topic_key, title, source_signature, article_path, content,
                local_context, exact_evidence, target_items, used_sources, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                topic_key,
                title,
                source_signature,
                article_path,
                content,
                local_context,
                exact_evidence,
                json.dumps(target_items),
                json.dumps(used_sources),
                time.time(),
            ),
        )
        self.conn.commit()
