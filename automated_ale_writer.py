#!/usr/bin/env python3
# ./venv/Scripts/python.exe automated_ale_writer.py

from __future__ import annotations

import argparse
import glob
import io
import logging
import os
import re
import warnings
from contextlib import redirect_stderr, redirect_stdout
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv
import pandas as pd
import pdfplumber
from ale_canonical_facts import DEFAULT_CANONICAL_FACT_REGISTRY
from ale_memory_store import MemoryStore
from langchain_chroma import Chroma
from langchain_classic.retrievers import EnsembleRetriever
from langchain_community.document_loaders import Docx2txtLoader, PyPDFLoader
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from langchain_tavily._utilities import TavilySearchAPIWrapper
from langchain_text_splitters import RecursiveCharacterTextSplitter


SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".pptx"}
PDF_TABLE_SETTINGS = {
    "vertical_strategy": "text",
    "horizontal_strategy": "text",
    "min_words_vertical": 3,
    "min_words_horizontal": 1,
}
OFFICIAL_WEB_DOMAINS = ["dpwh.gov.ph", "coa.gov.ph", "officialgazette.gov.ph"]

DATA_FOLDER = Path(os.getenv("ALE_DATA_FOLDER",
                   "./RAG - ALE ARCHITECTURE BOARD EXAM")).resolve()
OUTPUT_FOLDER = Path(os.getenv("ALE_OUTPUT_FOLDER",
                     "./ALE_Reviewer_Library")).resolve()
DB_DIR = Path(os.getenv("ALE_DB_DIR", "./chroma_db")).resolve()
MEMORY_DIR = Path(os.getenv("ALE_MEMORY_DIR", "./.ale_memory")).resolve()

EMBED_MODEL_NAME = os.getenv("ALE_EMBED_MODEL", "all-MiniLM-L6-v2")
OLLAMA_MODEL = os.getenv("ALE_OLLAMA_MODEL", "qwen2.5:14b-instruct")
LOCAL_REASONER_MODEL = "deepseek-r1:14b"
LOCAL_WRITER_MODEL = OLLAMA_MODEL
LOCAL_VERIFIER_MODEL = "deepseek-r1:14b"
REASONER_MODEL = os.getenv("ALE_REASONER_MODEL", LOCAL_REASONER_MODEL)
WRITER_MODEL = os.getenv("ALE_WRITER_MODEL", LOCAL_WRITER_MODEL)
VERIFIER_MODEL = os.getenv("ALE_VERIFIER_MODEL", LOCAL_VERIFIER_MODEL)
OLLAMA_NUM_CTX = int(os.getenv("ALE_OLLAMA_NUM_CTX", "16384"))
OLLAMA_TEMPERATURE = float(os.getenv("ALE_OLLAMA_TEMPERATURE", "0"))
REASONER_TEMPERATURE = float(os.getenv("ALE_REASONER_TEMPERATURE", "0"))
WRITER_TEMPERATURE = float(os.getenv("ALE_WRITER_TEMPERATURE", str(OLLAMA_TEMPERATURE)))
VERIFIER_TEMPERATURE = float(os.getenv("ALE_VERIFIER_TEMPERATURE", "0"))
OLLAMA_REPEAT_PENALTY = float(os.getenv("ALE_OLLAMA_REPEAT_PENALTY", "1.15"))
OLLAMA_TOP_P = float(os.getenv("ALE_OLLAMA_TOP_P", "0.05"))

CHUNK_SIZE = int(os.getenv("ALE_CHUNK_SIZE", "1000"))
CHUNK_OVERLAP = int(os.getenv("ALE_CHUNK_OVERLAP", "100"))
INDEX_BATCH_SIZE = int(os.getenv("ALE_INDEX_BATCH_SIZE", "500"))
CHROMA_FETCH_BATCH_SIZE = int(os.getenv("ALE_CHROMA_FETCH_BATCH", "5000"))

VECTOR_K = int(os.getenv("ALE_VECTOR_K", "20"))
BM25_K = int(os.getenv("ALE_BM25_K", "20"))
BM25_MAX_CHUNKS = int(os.getenv("ALE_BM25_MAX_CHUNKS", "15000"))
MAX_TABLE_PAGES_PER_FILE = int(os.getenv("ALE_MAX_TABLE_PAGES", "25"))
MAX_LOCAL_CONTEXT_CHARS = int(
    os.getenv("ALE_MAX_LOCAL_CONTEXT_CHARS", "90000"))
MAX_WEB_CONTEXT_CHARS = int(os.getenv("ALE_MAX_WEB_CONTEXT_CHARS", "12000"))
MAX_DOC_SNIPPET_CHARS = int(os.getenv("ALE_MAX_DOC_SNIPPET_CHARS", "3500"))
MAX_LOCAL_DOCS = int(os.getenv("ALE_MAX_LOCAL_DOCS", "12"))
MEMORY_SNIPPET_LIMIT = int(os.getenv("ALE_MEMORY_SNIPPET_LIMIT", "8"))
MEMORY_SUMMARY_LIMIT = int(os.getenv("ALE_MEMORY_SUMMARY_LIMIT", "4"))
MAX_OFFICIAL_SOURCE_RESULTS = int(os.getenv("ALE_MAX_OFFICIAL_SOURCE_RESULTS", "4"))
MIN_ARTICLE_CHARS = int(os.getenv("ALE_MIN_ARTICLE_CHARS", "500"))
THIN_FILE_BYTES = int(os.getenv("ALE_THIN_FILE_BYTES", "1500"))
MAX_GENERATION_ATTEMPTS = int(os.getenv("ALE_MAX_GENERATION_ATTEMPTS", "2"))

ENABLE_WEB_SEARCH = os.getenv("ALE_ENABLE_WEB_SEARCH", "1").lower() not in {
    "0", "false", "no"}

# Tavily: set TAVILY_API_KEY in the process environment, or in `.local.env` at
# the repo root (loaded at startup in main()).

STOPWORDS = {
    "the", "and", "for", "with", "from", "that", "this", "into", "over",
    "rule", "rules", "section", "code", "codes", "general", "minimum",
    "maximum", "standard", "standards", "requirements", "requirement",
    "application", "considerations", "factors", "design", "details",
}
OFFICIAL_SOURCE_HINTS = (
    "official gazette",
    "dpwh",
    "ncda",
    "official",
    "irr",
    "amended",
    "revised",
    "000_laws",
    "\\000_laws\\",
    "01 - ph codes and laws",
    "ph codes and laws critical",
)
LOW_TRUST_SOURCE_HINTS = (
    "blog",
    "slides",
    "reviewer",
    "reviewers",
    "test bank",
    "pedrosantosjr",
    "scribd",
    "studocu",
    "youtube",
    "atlas",
    "manilatimes",
    "summary",
    "fully illustrated",
)
REGULATORY_TOPIC_HINTS = (
    "bp ",
    "pd ",
    "ra ",
    "irr",
    "rule ",
    "code",
    "building code",
    "fire code",
    "department order",
    "ordinance",
)
PRIMARY_UPDATE_HINTS = (
    "irr",
    "implementing rules",
    "implementing rule",
    "amended",
    "revised",
    "memorandum",
    "circular",
    "department order",
    "official gazette",
    ".pdf",
)

TARGET_CONTENT = {
    "Accessibility Standards (BP 344 / RA 9442)": [
        "BP 344 (2024 IRR): Ramp Slope Tiers (1:20, 1:15, 1:12) and Maximum Run Lengths",
        "BP 344 (2024 IRR): Accessible Washrooms - Clearance, Grab Bars, and Fixture Heights",
        "BP 344 (2024 IRR): Tactile Warning Surfaces, Braille Signage, and Visual Alarms",
        "BP 344 (2024 IRR): Elevator Dimensions, Control Panels, and Wheelchair Turning Radii",
        "BP 344 vs PD 1096: Resolving Conflicting Ramp and Corridor Width Requirements",
        "RA 9442: Mandatory PWD Privileges, Incentives, and Design Integration",
        "Dimensions for Wheelchair Maneuvering, Parking Slots (4.00m min.), and Passing Spaces",
    ],
    "Anthropometrics & Human Dimensions": [
        "Anthropometrics: Standard Human Body Dimensions (Standing, Sitting, Reaching)",
        "Residential Clearances: Kitchen Work Triangles, Counter Heights, and Bedroom Layouts",
        "Commercial Clearances: Office Workstations, Retail Aisle Widths, and Dining Tables",
        "Human Dimensions for Institutional Design (Schools, Hospitals, and Libraries)",
        "Ergonomics in Furniture Design: Posture, Seat Heights, and Viewing Angles",
    ],
    "National Building Code Application (PD 1096)": [
        "PD 1096 Rule VII: Classification of Use/Occupancy and Types of Construction",
        "PD 1096 Rule VII: Calculating AMBF, PSO, ISA, USA, and MACA (The Area Metrics)",
        "PD 1096 Rule VII: Building Height Limits (BHL), FLAR, and GFA/TGFA Computations",
        "PD 1096 Rule VIII: Light and Ventilation (Minimum Window Sizes and Court Dimensions)",
        "PD 1096 Rule VIII: Setbacks, Easements, and Projections over Public Streets",
        "PD 1096 Rule XII: General Requirements for Egress, Corridors, and Occupant Loads",
        "Building Permit Process, Exemptions, Fines, and the Role of the Building Official",
        "Minimum Parking Requirements per Occupancy Classification",
    ],
    "Architecture of Africa, Australia & the Americas": [
        "Pre-Columbian Mesoamerica: Pyramids, Plazas, and Aztec Urbanism",
        "Inca Architecture: Ashlar Masonry, Terracing, and Engineering Marvels",
        "North American Indigenous Architecture: Pueblos, Longhouses, and Tipis",
        "African Vernacular: Earth Architecture, Mosques of Mali, and Great Zimbabwe",
        "Colonial Adaptations: European Architectural Influence in the Americas and Australia",
    ],
    "Global Modernism & Contemporary": [
        "The Bauhaus and the International Style: Form Follows Function",
        "Le Corbusier's Five Points of Architecture and the Machine for Living",
        "Mies van der Rohe: 'Less is More' and the Modern Glass Skyscraper",
        "Brutalism: Raw Concrete and Structural Expressionism",
        "Post-Modernism in Architecture: Venturi, Scott Brown, and the Return of Ornament",
        "21st Century Movements: Deconstructivism, High-Tech, and Parametricism",
    ],
    "Philippine Architecture": [
        "Pre-Colonial Vernacular: The Anatomy, Joinery, and Evolution of the Bahay Kubo",
        "Spanish Colonial Era: The Bahay na Bato Floor Plan and Earthquake Baroque Churches",
        "Spanish Colonial Era: The Laws of the Indies and the Plaza Complex",
        "American Colonial Era: Daniel Burnham's City Beautiful and the Pensionado Architects",
        "Masters of the Golden Age: Juan Nakpil, Pablo Antonio, Leandro Locsin, and Francisco Manosa",
        "The Search for Modern Filipino Identity: Tropical Regionalism and the New Vernacular",
    ],
    "Site Planning Considerations and Environmental Factors": [
        "Microclimate Analysis: Wind Paths (Amihan/Habagat) and Solar Orientation Strategies",
        "Topography and Slope Analysis: Cut-and-Fill Computations and Buildability Limits",
        "Geological Hazards: Identifying Fault Lines, Liquefaction Zones, and Soil Bearing Capacities",
        "Hydrology in Site Planning: Surface Drainage, Swales, and Stormwater Runoff",
        "Flora and Fauna in Site Development: Preserving Existing Trees and Natural Habitats",
    ],
}

SYSTEM_INSTRUCTIONS = r"""
You are an elite, strict Architectural Mentor and Examiner for the Philippine Architecture Licensure Exam (ALE). Your dual mandate is factual accuracy and highly effective instruction.

CRITICAL DIRECTIVES:
1. Context is absolute law. You may only extract facts, dimensions, and rules from the provided context.
2. If the answer is not in the context, say: "The provided context does not contain this information."
3. Philippine laws and IRRs override all other sources.
4. If the topic title includes a year or amendment state, prefer exact year-matching official sources and treat older conflicting sources as superseded unless the context explicitly says otherwise.
5. Do not merge unofficial summaries, reviewer notes, slides, or older rules into the current rule set without explicitly labeling them as older or secondary.
6. Use metric units first.
7. Every specific rule, dimension, or formula must have an inline citation in this format: [Source File, Rule/Section].
8. Any calculation must show the exact formula, the variables used, and the arithmetic steps.
9. Do not simplify a rule into "no maximum length," "-", or "unlimited" if the context actually provides a per-span limit, rise trigger, or landing interval. State the precise constraint.

WORKFLOW:
Step 1: Thinking phase
Use <thinking> tags to extract rules, dimensions, source references, conflicts, and missing data before writing.

Step 2: Article generation
Generate the article using exactly this Markdown structure.

# [Topic Title]
*An Immersive ALE Review Module*

## The Real-World Scenario (The Hook)
[Write a short scenario that makes the rule feel practical.]

## Core Concepts
[Define the key terms in clear bullet points.]

## The Hard Data (Cheat Sheet)
[Use a Markdown table for dimensions, clearances, slopes, or other quantitative rules.]

## Step-by-Step Computation (If Applicable)
[Show the formula and a clear worked example only when the topic involves math.]

## ALE Exam Traps and Common Mistakes
[Highlight likely board-exam mistakes and common confusions.]

## Active Recall Question
[Write one specific multiple-choice question based only on the provided context. Put the answer and explanation in a blockquote.]

## Verified Sources
[Numbered list of the source documents and sections actually used.]
"""

HUMAN_TEMPLATE = r"""
USER TOPIC: {question}

<MANDATORY_COVERAGE>
You must ensure the article covers all of these required points:
{target_description}
If any point is missing from the context, say so explicitly and do not invent it.
</MANDATORY_COVERAGE>

<CONTEXT_PROCESSING_INSTRUCTIONS>
The data below may come from raw PDF extraction and web search.
1. Table artifacts may appear as plain text. Reconstruct row and column meaning carefully.
2. Treat local sources as the primary authority.
3. Use web sources only to supplement missing context and never let them override Philippine laws or IRRs.
4. If a source block is labeled HIGH AUTHORITY or PRIMARY OFFICIAL, prefer it over MEDIUM or LOW authority blocks when there is a conflict.
5. If an EXACT_MEMORY_EVIDENCE block is present, treat it as the highest-priority grounding for dimensions, rule wording, and citations.
6. If an OFFICIAL_FACT_CARD block is present, treat it as binding unless another PRIMARY OFFICIAL source in the provided context clearly supersedes it.
7. If the LATEST_OFFICIAL_SOURCE_CHECK block reports a potential newer official source, do not present the topic as settled without reconciling that newer official source.
8. If a TOPIC_TITLE_GUARDRAIL block is present, explicitly address that title-overclaim or scope warning in the article.
</CONTEXT_PROCESSING_INSTRUCTIONS>

<OFFICIAL_FACT_CARD>
{official_fact_card}
</OFFICIAL_FACT_CARD>

<TOPIC_TITLE_GUARDRAIL>
{topic_title_guardrail}
</TOPIC_TITLE_GUARDRAIL>

<LATEST_OFFICIAL_SOURCE_CHECK>
{latest_official_source_check}
</LATEST_OFFICIAL_SOURCE_CHECK>

<LOCAL_DB_SOURCES>
{local_context}
</LOCAL_DB_SOURCES>

<WEB_SEARCH_SOURCES>
{internet_context}
</WEB_SEARCH_SOURCES>

<FACT_SHEET>
{fact_sheet}
</FACT_SHEET>

<VERIFIER_FEEDBACK>
{verifier_feedback}
</VERIFIER_FEEDBACK>

Execute the required workflow:
1. Use the FACT_SHEET as the primary source map before writing.
2. If VERIFIER_FEEDBACK is present, fix those issues and remove unsupported claims.
3. Open <thinking> tags and map out the facts before writing.
4. Output the final Markdown article exactly in the required structure.
"""

FACT_SYSTEM_INSTRUCTIONS = r"""
You are the evidence extraction member of an ALE AI council.

Your only job is to build a compact fact sheet from the provided context.
Do not write the final article.
Do not speculate.
If information is missing, say it is missing.
Prefer Philippine laws, IRRs, and PRIMARY OFFICIAL local sources over all others.
When sources conflict, name the conflict and identify which source is higher authority.
Do not collapse a span limit into "no maximum" or "-" when the context provides a more precise landing or interval rule.
If an OFFICIAL_FACT_CARD is present, treat it as binding unless another PRIMARY OFFICIAL source in the provided context clearly supersedes it.
If the LATEST_OFFICIAL_SOURCE_CHECK indicates a potential newer official source, state that clearly in the fact sheet and do not claim the older source is definitively current.
If a TOPIC_TITLE_GUARDRAIL block is present, explicitly state that limitation or overclaim in the fact sheet.

Output exactly these Markdown sections:

## Source Priority
- [source file and why it is trusted]

## Confirmed Facts
- [fact] [Source File, page/section]

## Conflicts and Supersession
- [conflict and resolution]

## Missing or Unconfirmed
- [missing point]

## Coverage Audit
- [target item]: covered / missing
"""

FACT_HUMAN_TEMPLATE = r"""
USER TOPIC: {question}

<MANDATORY_COVERAGE>
{target_description}
</MANDATORY_COVERAGE>

<OFFICIAL_FACT_CARD>
{official_fact_card}
</OFFICIAL_FACT_CARD>

<TOPIC_TITLE_GUARDRAIL>
{topic_title_guardrail}
</TOPIC_TITLE_GUARDRAIL>

<LATEST_OFFICIAL_SOURCE_CHECK>
{latest_official_source_check}
</LATEST_OFFICIAL_SOURCE_CHECK>

<LOCAL_DB_SOURCES>
{local_context}
</LOCAL_DB_SOURCES>

<WEB_SEARCH_SOURCES>
{internet_context}
</WEB_SEARCH_SOURCES>

Build the fact sheet now.
"""

VERIFIER_SYSTEM_INSTRUCTIONS = r"""
You are the verifier member of an ALE AI council.

You do not rewrite the article.
You only judge whether it is safe to save.
Reject any unsupported dimension, rule, citation, or conflict resolution.
Prefer the FACT_SHEET and PRIMARY OFFICIAL sources when judging.
Fail the draft if it oversimplifies a qualified rule into "no maximum length," "-", or "unlimited" when the context contains a more precise span, rise, or landing constraint.
If an OFFICIAL_FACT_CARD is present, fail the draft when it contradicts or omits that card without a stronger PRIMARY OFFICIAL basis in the provided context.
If the LATEST_OFFICIAL_SOURCE_CHECK reports a potential newer official source, fail the draft unless it reconciles that newer official result or clearly states that a newer official source may supersede the local source.
If a TOPIC_TITLE_GUARDRAIL block is present, fail the draft unless it explicitly acknowledges that title-overclaim or scope warning.

Return exactly this structure:
VERDICT: PASS or FAIL
MISSING_ATOMIC_ITEMS:
- ...
UNSUPPORTED_CLAIMS:
- ...
CITATION_ISSUES:
- ...
CONFLICT_ISSUES:
- ...
REVISION_INSTRUCTIONS:
- ...
"""

VERIFIER_HUMAN_TEMPLATE = r"""
USER TOPIC: {question}

<MANDATORY_COVERAGE>
{target_description}
</MANDATORY_COVERAGE>

<OFFICIAL_FACT_CARD>
{official_fact_card}
</OFFICIAL_FACT_CARD>

<TOPIC_TITLE_GUARDRAIL>
{topic_title_guardrail}
</TOPIC_TITLE_GUARDRAIL>

<LATEST_OFFICIAL_SOURCE_CHECK>
{latest_official_source_check}
</LATEST_OFFICIAL_SOURCE_CHECK>

<FACT_SHEET>
{fact_sheet}
</FACT_SHEET>

<ARTICLE_DRAFT>
{article_draft}
</ARTICLE_DRAFT>

<LOCAL_DB_SOURCES>
{local_context}
</LOCAL_DB_SOURCES>

<WEB_SEARCH_SOURCES>
{internet_context}
</WEB_SEARCH_SOURCES>

Judge the article now.
"""


def configure_logging() -> None:
    os.environ.setdefault("HF_HUB_DISABLE_PROGRESS_BARS", "1")
    os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
    os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

    for logger_name in ("pdfminer", "pdfminer.pdfinterp", "pdfminer.psparser"):
        logging.getLogger(logger_name).setLevel(logging.ERROR)
    for logger_name in (
        "pypdf",
        "pypdf._reader",
        "pypdf.generic._data_structures",
        "sentence_transformers",
        "transformers",
        "huggingface_hub",
    ):
        logging.getLogger(logger_name).setLevel(logging.ERROR)

    warnings.filterwarnings(
        "ignore",
        message=r".*You are sending unauthenticated requests to the HF Hub.*",
    )

    try:
        from transformers.utils import logging as transformers_logging

        transformers_logging.set_verbosity_error()
    except Exception:
        pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate ALE reviewer modules from local source memory."
    )
    parser.set_defaults(
        force_regenerate=True,
        rebuild_memory=True,
    )
    parser.add_argument(
        "--topic",
        action="append",
        default=[],
        help="Only process titles or subtopics containing this text. Repeat to target multiple topics.",
    )
    parser.add_argument(
        "--force-regenerate",
        dest="force_regenerate",
        action="store_true",
        help="Ignore existing article files and cached topic outputs. This is now the default behavior.",
    )
    parser.add_argument(
        "--reuse-existing",
        dest="force_regenerate",
        action="store_false",
        help="Reuse existing article files and cached topic outputs when possible.",
    )
    parser.add_argument(
        "--rebuild-memory",
        dest="rebuild_memory",
        action="store_true",
        help="Rebuild the persistent memory tables from the current Chroma collection. This is now the default behavior.",
    )
    parser.add_argument(
        "--skip-memory-rebuild",
        dest="rebuild_memory",
        action="store_false",
        help="Reuse the existing persistent memory tables without rebuilding them first.",
    )
    parser.add_argument(
        "--skip-web",
        action="store_true",
        help="Disable Tavily web search for this run.",
    )
    return parser.parse_args()


def summarize_error(error: Exception, max_len: int = 220) -> str:
    message = " ".join(str(error).split())
    if len(message) > max_len:
        return message[: max_len - 3] + "..."
    return message


def resolve_cached_sentence_transformer(model_name: str) -> Optional[Path]:
    if Path(model_name).exists():
        return Path(model_name).resolve()

    repo_candidates = [model_name]
    if "/" not in model_name:
        repo_candidates.insert(0, f"sentence-transformers/{model_name}")

    for repo_id in repo_candidates:
        model_dir_name = f"models--{repo_id.replace('/', '--')}"
        hub_root = Path.home() / ".cache" / "huggingface" / "hub" / model_dir_name
        snapshots_dir = hub_root / "snapshots"
        refs_main = hub_root / "refs" / "main"

        if refs_main.exists():
            revision = refs_main.read_text(encoding="utf-8").strip()
            snapshot_path = snapshots_dir / revision
            if snapshot_path.exists():
                return snapshot_path.resolve()

        if snapshots_dir.exists():
            snapshots = sorted(
                (path for path in snapshots_dir.iterdir() if path.is_dir()),
                key=lambda path: path.stat().st_mtime,
                reverse=True,
            )
            if snapshots:
                return snapshots[0].resolve()

    return None


def normalize_source_path(value: object) -> Optional[str]:
    if not value:
        return None
    return str(Path(str(value)).resolve())


def safe_filename(name: str) -> str:
    cleaned = re.sub(r'[<>:"/\\|?*]+', " - ", name)
    cleaned = re.sub(r"\s+", " ", cleaned).strip().rstrip(".")
    return cleaned or "untitled"


def to_text(response: object) -> str:
    if isinstance(response, str):
        return response.strip()
    content = getattr(response, "content", response)
    if isinstance(content, str):
        return content.strip()
    return str(content).strip()


def dedupe_documents(documents: Iterable[Document]) -> list[Document]:
    unique_docs = []
    seen = set()
    for doc in documents:
        source = normalize_source_path(doc.metadata.get("source"))
        page = doc.metadata.get("page")
        snippet = doc.page_content[:200]
        key = (source, page, snippet)
        if key in seen:
            continue
        seen.add(key)
        unique_docs.append(doc)
    return unique_docs


def normalize_for_match(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9:./ -]+", " ", text.lower())).strip()


def normalize_slope(text: str) -> str:
    return re.sub(r"\s*[:/-]\s*", ":", text.strip())


def extract_query_terms(query: str) -> list[str]:
    query_lower = query.lower()
    terms = set()

    for law_ref in re.findall(r"\b(?:bp|pd|ra)\s*\d+\b", query_lower):
        terms.add(re.sub(r"\s+", " ", law_ref).strip())

    for slope in re.findall(r"\b\d+\s*[:/-]\s*\d+\b", query_lower):
        terms.add(normalize_slope(slope))

    for year in re.findall(r"\b(?:19|20)\d{2}\b", query_lower):
        terms.add(year)

    for token in re.findall(r"\b[a-z][a-z0-9.-]{2,}\b", query_lower):
        if token not in STOPWORDS:
            terms.add(token)

    return sorted(terms)


def build_target_items(title: str) -> list[str]:
    items = [title.strip()]

    items.extend(re.findall(r"\b(?:BP|PD|RA)\s*\d+\b",
                 title, flags=re.IGNORECASE))
    items.extend(re.findall(r"\b\d+\s*[:/-]\s*\d+\b", title))
    items.extend(re.findall(r"\b(?:19|20)\d{2}\b", title))

    for piece in re.split(r"[:()]| and |,", title):
        piece = piece.strip(" -")
        if len(piece) >= 4:
            items.append(piece)

    normalized_items = []
    seen = set()
    for item in items:
        cleaned = normalize_slope(item) if re.fullmatch(
            r"\d+\s*[:/-]\s*\d+", item.strip()) else item.strip()
        key = cleaned.lower()
        if key and key not in seen:
            seen.add(key)
            normalized_items.append(cleaned)

    return normalized_items


def is_regulatory_topic(query: str) -> bool:
    query_key = normalize_for_match(query)
    return any(hint in query_key for hint in REGULATORY_TOPIC_HINTS)


def extract_year_values(text: str) -> list[int]:
    return sorted({int(year) for year in re.findall(r"\b(?:19|20)\d{2}\b", text)})


def extract_latest_topic_year(query: str) -> Optional[int]:
    years = extract_year_values(query)
    return max(years) if years else None


def flatten_tavily_results(results: object) -> list[dict[str, object]]:
    if isinstance(results, dict):
        for key in ("results", "documents", "data"):
            value = results.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return []

    if isinstance(results, list):
        return [item for item in results if isinstance(item, dict)]

    return []


def summarize_tavily_results(results: object, limit: int = 4) -> str:
    entries = flatten_tavily_results(results)
    if not entries:
        context = str(results).strip()
        if len(context) > MAX_WEB_CONTEXT_CHARS:
            context = context[:MAX_WEB_CONTEXT_CHARS].rstrip() + "...[truncated]"
        return context or "No web context retrieved."

    blocks = []
    total_chars = 0
    for entry in entries[:limit]:
        title = str(entry.get("title", "Untitled result")).strip()
        url = str(entry.get("url", "")).strip()
        content = " ".join(str(entry.get("content", "")).split()).strip()
        published = str(entry.get("published_date", "") or entry.get("published", "")).strip()
        block = f"TITLE: {title}\nURL: {url}\nPUBLISHED: {published or 'Unknown'}\n{content[:700]}".strip()
        projected_chars = total_chars + len(block) + 4
        if projected_chars > MAX_WEB_CONTEXT_CHARS:
            break
        blocks.append(block)
        total_chars = projected_chars

    return "\n\n--\n\n".join(blocks) if blocks else "No web context retrieved."


def build_latest_official_source_check(
    web_search: Optional[TavilySearch],
    title: str,
) -> tuple[str, bool]:
    if web_search is None:
        return "STATUS: UNAVAILABLE\nDETAIL: Web search unavailable.", False

    if not is_regulatory_topic(title):
        return "STATUS: NOT_REQUIRED\nDETAIL: Topic is not a law or code topic, so latest-official-source checking is not required.", False

    law_refs = [item.lower() for item in re.findall(r"\b(?:BP|PD|RA)\s*\d+\b", title, flags=re.IGNORECASE)]
    topic_year = extract_latest_topic_year(title)
    search_terms = []
    if law_refs:
        search_terms.extend(law_refs)
    if topic_year is not None:
        search_terms.append(str(topic_year))
    search_terms.extend(["official", "amended", "irr", "pdf"])
    search_query = " ".join(dict.fromkeys(search_terms)) or f"{title} official amendment IRR pdf"

    try:
        raw_results = web_search.invoke(search_query)
    except Exception as error:
        return f"STATUS: ERROR\nDETAIL: {summarize_error(error)}", False

    entries = flatten_tavily_results(raw_results)
    if not entries:
        return "STATUS: NO_STRUCTURED_RESULTS\nDETAIL: Official web results could not be parsed.", False

    ranked_results = []
    for entry in entries:
        url = str(entry.get("url", "")).strip()
        title_text = str(entry.get("title", "")).strip()
        content_text = str(entry.get("content", "")).strip()
        published = str(entry.get("published_date", "") or entry.get("published", "")).strip()
        haystack = normalize_for_match(f"{title_text} {content_text} {url}")
        if law_refs and not any(law_ref in haystack for law_ref in law_refs):
            continue

        domain = urlparse(url).netloc.lower()
        years = extract_year_values(" ".join(filter(None, [title_text, content_text, published, url])))
        best_year = max(years) if years else None
        primary_like = any(hint in haystack for hint in PRIMARY_UPDATE_HINTS)
        score = 0
        if primary_like:
            score += 10
        if best_year is not None and topic_year is not None and best_year >= topic_year:
            score += 8
        if domain:
            score += 4
        ranked_results.append(
            {
                "title": title_text or "Untitled result",
                "url": url,
                "domain": domain or "unknown",
                "published": published or "Unknown",
                "year": best_year,
                "primary_like": primary_like,
                "score": score,
            }
        )

    ranked_results.sort(
        key=lambda item: (
            item["score"],
            item["year"] if item["year"] is not None else -1,
        ),
        reverse=True,
    )

    top_results = ranked_results[:MAX_OFFICIAL_SOURCE_RESULTS]
    newer_official_found = bool(
        topic_year is not None
        and any(
            result["primary_like"] and result["year"] is not None and result["year"] > topic_year
            for result in top_results
        )
    )

    status = "POTENTIAL_NEWER_OFFICIAL_SOURCE_FOUND" if newer_official_found else "NO_NEWER_OFFICIAL_SOURCE_FOUND"
    lines = [
        f"STATUS: {status}",
        f"TOPIC_YEAR: {topic_year if topic_year is not None else 'UNKNOWN'}",
        "OFFICIAL_RESULTS:",
    ]
    for result in top_results:
        lines.append(
            "- "
            f"{result['title']} | domain={result['domain']} | "
            f"year={result['year'] if result['year'] is not None else 'UNKNOWN'} | "
            f"published={result['published']} | primary_update_like={result['primary_like']} | "
            f"url={result['url']}"
        )

    if not top_results:
        lines.append("- No matching official-domain results found.")

    if newer_official_found:
        lines.append(
            "ASSESSMENT: At least one official-domain result appears to reference a newer year than the topic. Reconcile the article against that newer official result before treating the local source as current."
        )
    else:
        lines.append(
            "ASSESSMENT: No newer official-domain result was detected in the checked results."
        )

    return "\n".join(lines), newer_official_found


def build_query_variants(query: str) -> list[str]:
    terms = extract_query_terms(query)
    variants = [query.strip()]

    if terms:
        variants.append(" ".join(terms))

    law_refs = [term for term in terms if re.fullmatch(
        r"(?:bp|pd|ra)\s*\d+", term)]
    slopes = [term for term in terms if re.fullmatch(r"\d+:\d+", term)]
    keywords = [term for term in terms if term not in law_refs and term not in slopes and not re.fullmatch(
        r"(?:19|20)\d{2}", term)]

    focused = law_refs + keywords[:8] + slopes
    if focused:
        variants.append(" ".join(focused))

    deduped = []
    seen = set()
    for variant in variants:
        normalized = normalize_for_match(variant)
        if normalized and normalized not in seen:
            seen.add(normalized)
            deduped.append(variant)

    return deduped


def filter_target_content(topic_filters: list[str]) -> dict[str, list[str]]:
    if not topic_filters:
        return {subtopic: list(articles) for subtopic, articles in TARGET_CONTENT.items()}

    normalized_filters = [normalize_for_match(
        item) for item in topic_filters if item.strip()]
    filtered: dict[str, list[str]] = {}

    for subtopic, articles in TARGET_CONTENT.items():
        subtopic_key = normalize_for_match(subtopic)
        include_full_subtopic = any(
            filter_text in subtopic_key for filter_text in normalized_filters)
        matched_titles = []
        seen_titles = set()

        for title in articles:
            title_key = normalize_for_match(title)
            if include_full_subtopic or any(
                filter_text in title_key or filter_text in f"{subtopic_key} {title_key}"
                for filter_text in normalized_filters
            ):
                if title not in seen_titles:
                    seen_titles.add(title)
                    matched_titles.append(title)

        if matched_titles:
            filtered[subtopic] = matched_titles

    return filtered


def source_authority_score(source_text: str, query_terms: list[str]) -> tuple[int, str]:
    source_lower = normalize_for_match(source_text)
    score = 0

    for hint in OFFICIAL_SOURCE_HINTS:
        if hint in source_lower:
            score += 8

    for hint in LOW_TRUST_SOURCE_HINTS:
        if hint in source_lower:
            score -= 10

    for term in query_terms:
        if term in source_lower:
            score += 5

    query_years = [term for term in query_terms if re.fullmatch(
        r"(?:19|20)\d{2}", term)]
    if query_years:
        if any(year in source_lower for year in query_years):
            score += 6
        elif re.search(r"\b(?:19|20)\d{2}\b", source_lower):
            score -= 3

    if score >= 18:
        label = "PRIMARY OFFICIAL"
    elif score >= 8:
        label = "HIGH AUTHORITY"
    elif score >= 0:
        label = "MEDIUM AUTHORITY"
    else:
        label = "LOW AUTHORITY"

    return score, label


def document_relevance_score(doc: Document, query_terms: list[str]) -> int:
    source = normalize_source_path(doc.metadata.get("source")) or ""
    source_score, _ = source_authority_score(source, query_terms)
    content = normalize_for_match(doc.page_content)
    source_lower = normalize_for_match(source)
    score = source_score

    query_law_refs = [term for term in query_terms if re.fullmatch(
        r"(?:bp|pd|ra)\s*\d+", term)]
    query_years = [term for term in query_terms if re.fullmatch(
        r"(?:19|20)\d{2}", term)]

    for term in query_terms:
        if term in content:
            score += 3
        if term in source_lower:
            score += 2

    if any(re.fullmatch(r"\d+:\d+", term) for term in query_terms):
        slope_matches = sum(1 for term in query_terms if re.fullmatch(
            r"\d+:\d+", term) and term in content)
        score += slope_matches * 4

    if query_law_refs and not any(term in content or term in source_lower for term in query_law_refs):
        score -= 12

    if query_years and not any(year in content or year in source_lower for year in query_years):
        score -= 4

    return score


def rank_documents_for_query(documents: list[Document], query: str) -> list[Document]:
    query_terms = extract_query_terms(query)
    ranked = []

    for doc in dedupe_documents(documents):
        source = normalize_source_path(doc.metadata.get("source")) or ""
        authority_score, authority_label = source_authority_score(
            source, query_terms)
        relevance_score = document_relevance_score(doc, query_terms)
        doc.metadata["_authority_score"] = authority_score
        doc.metadata["_authority_label"] = authority_label
        doc.metadata["_relevance_score"] = relevance_score
        ranked.append(doc)

    ranked.sort(
        key=lambda doc: (
            int(doc.metadata.get("_relevance_score", 0)),
            int(doc.metadata.get("_authority_score", 0)),
        ),
        reverse=True,
    )

    query_law_refs = [term for term in query_terms if re.fullmatch(
        r"(?:bp|pd|ra)\s*\d+", term)]
    if query_law_refs:
        law_filtered = [
            doc for doc in ranked
            if any(
                law_ref in normalize_for_match((normalize_source_path(
                    doc.metadata.get("source")) or "") + " " + doc.page_content)
                for law_ref in query_law_refs
            )
        ]
        if law_filtered:
            ranked = law_filtered

    if any(doc.metadata.get("_authority_label") == "PRIMARY OFFICIAL" for doc in ranked):
        ranked = [doc for doc in ranked if doc.metadata.get(
            "_authority_label") != "LOW AUTHORITY"]

    return ranked[:MAX_LOCAL_DOCS]


def collect_used_sources(documents: Iterable[Document]) -> list[str]:
    sources = []
    seen = set()

    for doc in documents:
        source = normalize_source_path(doc.metadata.get("source"))
        if source and source not in seen:
            seen.add(source)
            sources.append(source)

    return sources


def extract_relevant_snippet(text: str, query_terms: list[str], max_chars: int) -> str:
    cleaned = text.strip()
    if len(cleaned) <= max_chars:
        return cleaned

    parts = [part.strip() for part in re.split(
        r"\n+|(?<=[.!?])\s+", cleaned) if part.strip()]
    if not parts:
        return cleaned[:max_chars].rstrip() + "\n...[truncated]"

    scored_parts = []
    for idx, part in enumerate(parts):
        part_lower = normalize_for_match(part)
        score = sum(1 for term in query_terms if term in part_lower)
        if score > 0:
            scored_parts.append((score, idx, part))

    if not scored_parts:
        return cleaned[:max_chars].rstrip() + "\n...[truncated]"

    chosen_indexes = sorted(idx for _, idx, _ in sorted(
        scored_parts, reverse=True)[:6])
    selected = []
    total = 0
    for idx in chosen_indexes:
        part = parts[idx]
        if total + len(part) + 1 > max_chars:
            break
        selected.append(part)
        total += len(part) + 1

    snippet = "\n".join(selected).strip()
    if len(snippet) < len(cleaned):
        snippet += "\n...[truncated]"
    return snippet


def make_unique_headers(headers: list[object]) -> list[str]:
    counts = defaultdict(int)
    unique_headers = []
    for idx, header in enumerate(headers, start=1):
        label = str(header).strip() if header not in (
            None, "") else f"Column {idx}"
        counts[label] += 1
        if counts[label] > 1:
            label = f"{label}_{counts[label]}"
        unique_headers.append(label)
    return unique_headers


def table_to_markdown(table: list[list[object]]) -> Optional[str]:
    if not table:
        return None

    cleaned_rows = []
    for row in table:
        if not row:
            continue
        cleaned_row = [cell.strip() if isinstance(cell, str)
                       else cell for cell in row]
        if any(cell not in (None, "") for cell in cleaned_row):
            cleaned_rows.append(cleaned_row)

    if not cleaned_rows:
        return None

    max_cols = max(len(row) for row in cleaned_rows)
    normalized_rows = [row + [None] * (max_cols - len(row))
                       for row in cleaned_rows]
    header_row = normalized_rows[0]

    if all(cell in (None, "") for cell in header_row):
        headers = [f"Column {i}" for i in range(1, max_cols + 1)]
        data_rows = normalized_rows
    else:
        headers = make_unique_headers(header_row)
        data_rows = normalized_rows[1:]

    if not data_rows:
        return None

    return pd.DataFrame(data_rows, columns=headers).to_markdown(index=False)


def looks_like_table_text(text: str) -> bool:
    if not text:
        return False

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if len(lines) < 3:
        return False

    delimiter_lines = sum(
        1 for line in lines if "\t" in line or "|" in line or "  " in line)
    short_lines = sum(1 for line in lines if len(line.split()) <= 8)
    numeric_lines = sum(1 for line in lines if len(
        re.findall(r"\d", line)) >= 2)
    code_lines = sum(
        1
        for line in lines
        if re.search(
            r"\b(?:mm|cm|sqm|sq\.?\s?m|min|max|width|height|slope|rule)\b",
            line,
            re.IGNORECASE,
        )
    )

    return (
        delimiter_lines >= 3
        or (short_lines >= 5 and numeric_lines >= 3)
        or code_lines >= 4
    )


def extract_pdf_tables(file_path: Path, candidate_pages: set[int]) -> dict[int, list[str]]:
    tables_by_page: dict[int, list[str]] = defaultdict(list)
    if not candidate_pages:
        return tables_by_page

    try:
        with pdfplumber.open(str(file_path)) as pdf:
            for page_number in sorted(candidate_pages)[:MAX_TABLE_PAGES_PER_FILE]:
                if page_number > len(pdf.pages):
                    continue
                page = pdf.pages[page_number - 1]
                try:
                    for table in page.extract_tables(PDF_TABLE_SETTINGS):
                        markdown_table = table_to_markdown(table)
                        if markdown_table:
                            tables_by_page[page_number].append(markdown_table)
                except Exception as error:
                    print(
                        f"  [!] Skipping table extraction on page {page_number} of "
                        f"{file_path.name}: {summarize_error(error)}"
                    )
    except Exception as error:
        print(
            f"  [!] Table extraction unavailable for {file_path.name}: {summarize_error(error)}. "
            "Continuing with text-only PDF loading."
        )
    return tables_by_page


def load_pdf_documents(file_path: Path) -> list[Document]:
    try:
        docs = PyPDFLoader(str(file_path)).load()
        for doc in docs:
            doc.metadata["source"] = str(file_path)

        candidate_pages = {
            int(doc.metadata.get("page", 0)) + 1
            for doc in docs
            if looks_like_table_text(doc.page_content)
        }
        tables_by_page = extract_pdf_tables(file_path, candidate_pages)

        if tables_by_page:
            for doc in docs:
                page_number = int(doc.metadata.get("page", 0)) + 1
                page_tables = tables_by_page.get(page_number)
                if page_tables:
                    doc.page_content = (
                        f"{doc.page_content}\n\n"
                        "Extracted tables:\n\n"
                        + "\n\n".join(page_tables)
                    )

        return [doc for doc in docs if doc.page_content and doc.page_content.strip()]
    except Exception as error:
        print(
            f"  [!] PyPDF text extraction failed for {file_path.name}. "
            f"Using pdfplumber fallback. Reason: {summarize_error(error)}"
        )

    try:
        with pdfplumber.open(str(file_path)) as pdf:
            full_text = []
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    full_text.append(text)
        content = "\n\n".join(full_text).strip()
        if content:
            return [Document(page_content=content, metadata={"source": str(file_path)})]
    except Exception as error:
        print(
            f"  [!] pdfplumber fallback failed for {file_path.name}: {summarize_error(error)}")

    return []


def load_docx_documents(file_path: Path) -> list[Document]:
    try:
        docs = Docx2txtLoader(str(file_path)).load()
        for doc in docs:
            doc.metadata["source"] = str(file_path)
        return [doc for doc in docs if doc.page_content and doc.page_content.strip()]
    except Exception as error:
        print(f"  [!] DOCX load failed for {file_path}: {error}")
        return []


def load_pptx_documents(file_path: Path) -> list[Document]:
    try:
        from pptx import Presentation

        deck = Presentation(str(file_path))
        docs = []
        for slide_index, slide in enumerate(deck.slides, start=1):
            slide_texts = []
            for shape in slide.shapes:
                if hasattr(shape, "text") and shape.text:
                    text = shape.text.strip()
                    if text:
                        slide_texts.append(text)
            slide_content = "\n".join(slide_texts).strip()
            if slide_content:
                docs.append(
                    Document(
                        page_content=slide_content,
                        metadata={"source": str(
                            file_path), "page": slide_index - 1},
                    )
                )
        return docs
    except Exception as error:
        print(f"  [!] PPTX load failed for {file_path}: {error}")
        return []


def load_documents(file_path: Path) -> list[Document]:
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        return load_pdf_documents(file_path)
    if suffix == ".docx":
        return load_docx_documents(file_path)
    if suffix == ".pptx":
        return load_pptx_documents(file_path)
    return []


def load_embeddings() -> HuggingFaceEmbeddings:
    preferred_device = os.getenv("ALE_EMBED_DEVICE", "").strip()
    force_remote = os.getenv("ALE_FORCE_REMOTE_EMBED_MODEL", "0").lower() in {
        "1", "true", "yes"}
    model_source = EMBED_MODEL_NAME

    if not force_remote:
        cached_model = resolve_cached_sentence_transformer(EMBED_MODEL_NAME)
        if cached_model is not None:
            model_source = str(cached_model)

    devices = []

    if preferred_device:
        devices.append(preferred_device)
    else:
        try:
            import torch

            if torch.cuda.is_available():
                devices.append("cuda")
        except Exception:
            pass
        devices.append("cpu")

    last_error = None
    for device in dict.fromkeys(devices):
        try:
            source_label = model_source if Path(
                model_source).exists() else EMBED_MODEL_NAME
            print(f"Loading embeddings on {device} from {source_label}...")
            with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                embeddings = HuggingFaceEmbeddings(
                    model_name=model_source,
                    model_kwargs={"device": device},
                    show_progress=False,
                )
                embeddings.embed_query("ale warmup")
            return embeddings
        except Exception as error:
            last_error = error
            print(f"  [!] Embedding init failed on {device}: {error}")

    raise RuntimeError(f"Could not initialize embeddings: {last_error}")


def open_vectorstore(embeddings: HuggingFaceEmbeddings) -> Optional[Chroma]:
    if not DB_DIR.exists():
        return None
    try:
        print("Database found. Loading existing Chroma index...")
        return Chroma(
            persist_directory=str(DB_DIR),
            embedding_function=embeddings,
        )
    except Exception as error:
        print(f"  [!] Could not open existing Chroma DB: {error}")
        return None


def get_existing_sources(vectorstore: Optional[Chroma]) -> set[str]:
    existing_sources = set()
    if vectorstore is None:
        return existing_sources

    try:
        count = vectorstore._collection.count()
        offset = 0
        while offset < count:
            batch_data = vectorstore._collection.get(
                include=["metadatas"],
                limit=CHROMA_FETCH_BATCH_SIZE,
                offset=offset,
            )
            for metadata in batch_data.get("metadatas") or []:
                source = normalize_source_path((metadata or {}).get("source"))
                if source:
                    existing_sources.add(source)
            offset += CHROMA_FETCH_BATCH_SIZE
        print(f"  [+] Verified {len(existing_sources)} existing source files.")
    except Exception as error:
        print(f"  [!] Metadata fetch issue: {error}")

    return existing_sources


def iter_supported_files(root: Path) -> list[Path]:
    files = []
    pattern = str(root / "**" / "*")
    for file_path in glob.glob(pattern, recursive=True):
        path = Path(file_path)
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            files.append(path.resolve())
    return sorted(files)


def collect_new_documents(existing_sources: set[str]) -> list[Document]:
    print("Scanning for supported documents...")
    documents = []

    for file_path in iter_supported_files(DATA_FOLDER):
        source = str(file_path)
        if source in existing_sources:
            continue

        try:
            for doc in load_documents(file_path):
                content = (doc.page_content or "").strip()
                if len(content) <= 5:
                    continue
                doc.page_content = content
                doc.metadata["source"] = source
                documents.append(doc)
        except Exception as error:
            print(f"  [!] Error loading {file_path}: {error}")

    documents = dedupe_documents(documents)
    print(f"  [+] Collected {len(documents)} new document units for indexing.")
    return documents


def index_documents(
    documents: list[Document],
    vectorstore: Optional[Chroma],
    embeddings: HuggingFaceEmbeddings,
) -> Optional[Chroma]:
    if not documents:
        print("Database is already up to date. Skipping indexing.")
        return vectorstore

    print(f"Chunking {len(documents)} document units...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = [
        chunk
        for chunk in splitter.split_documents(documents)
        if isinstance(chunk.page_content, str) and len(chunk.page_content.strip()) > 10
    ]
    print(f"  [+] Prepared {len(chunks)} chunks for indexing.")

    for start in range(0, len(chunks), INDEX_BATCH_SIZE):
        batch = chunks[start: start + INDEX_BATCH_SIZE]
        batch_number = start // INDEX_BATCH_SIZE + 1
        try:
            if vectorstore is None:
                vectorstore = Chroma.from_documents(
                    documents=batch,
                    embedding=embeddings,
                    persist_directory=str(DB_DIR),
                )
            else:
                vectorstore.add_documents(batch)
            print(f"  [#] Batch {batch_number} indexed.")
        except Exception as batch_error:
            print(
                f"  [!] Batch {batch_number} failed. Falling back to single-chunk adds: {batch_error}")
            for chunk in batch:
                try:
                    if vectorstore is None:
                        vectorstore = Chroma.from_documents(
                            documents=[chunk],
                            embedding=embeddings,
                            persist_directory=str(DB_DIR),
                        )
                    else:
                        vectorstore.add_documents([chunk])
                except Exception as chunk_error:
                    source = chunk.metadata.get("source", "unknown")
                    page = chunk.metadata.get("page", "?")
                    print(
                        f"    [!] Skipping chunk from {source} page {page}: {chunk_error}")

    return vectorstore


def build_llm(model_name: str, temperature: float = OLLAMA_TEMPERATURE) -> ChatOllama:
    return ChatOllama(
        model=model_name,
        temperature=temperature,
        num_ctx=OLLAMA_NUM_CTX,
        repeat_penalty=OLLAMA_REPEAT_PENALTY,
        top_p=OLLAMA_TOP_P,
    )


def build_model_council() -> dict[str, ChatOllama]:
    print("  [+] Council models:")
    print(f"      Reasoner: {REASONER_MODEL}")
    print(f"      Writer:   {WRITER_MODEL}")
    print(f"      Verifier: {VERIFIER_MODEL}")
    return {
        "reasoner": build_llm(REASONER_MODEL, REASONER_TEMPERATURE),
        "writer": build_llm(WRITER_MODEL, WRITER_TEMPERATURE),
        "verifier": build_llm(VERIFIER_MODEL, VERIFIER_TEMPERATURE),
    }


def build_web_search() -> Optional[TavilySearch]:
    tavily_api_key = os.getenv("TAVILY_API_KEY", "").strip()
    if not ENABLE_WEB_SEARCH:
        print("Web search disabled by configuration.")
        return None
    if not tavily_api_key:
        print("No Tavily API key configured. Continuing without web search.")
        return None

    try:
        api_wrapper = TavilySearchAPIWrapper(tavily_api_key=tavily_api_key)
        return TavilySearch(
            api_wrapper=api_wrapper,
            max_results=5,
            include_domains=OFFICIAL_WEB_DOMAINS,
        )
    except Exception as error:
        print(
            f"  [!] Tavily initialization failed. Continuing without web search: {error}")
        return None


def build_prompt_chain(
    llm: ChatOllama,
    strict: bool = False,
    *,
    system_text: str = SYSTEM_INSTRUCTIONS,
    human_template: str = HUMAN_TEMPLATE,
):
    active_system_text = system_text
    if strict:
        active_system_text += (
            "\n\nCRITICAL REMINDER: Every factual statement must be anchored in the given "
            "context. If the context does not contain it, do not invent it."
        )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", active_system_text),
            ("human", human_template),
        ]
    )
    return prompt | llm | StrOutputParser()


def strip_thinking_tags(text: str) -> str:
    return re.sub(r"<thinking>.*?</thinking>", "", text, flags=re.IGNORECASE | re.DOTALL).strip()


def clean_model_output(text: str) -> str:
    cleaned = strip_thinking_tags(text)
    cleaned = cleaned.strip()
    heading_match = re.search(r"^#\s+.+", cleaned, flags=re.MULTILINE)
    if heading_match:
        return cleaned[heading_match.start():].strip()
    return cleaned


def build_fact_sheet(
    reasoner_chain,
    title: str,
    target_items: list[str],
    official_fact_card: str,
    topic_title_guardrail: str,
    latest_official_source_check: str,
    local_context: str,
    internet_context: str,
) -> str:
    payload = {
        "question": title,
        "target_description": "\n".join(target_items),
        "official_fact_card": official_fact_card,
        "topic_title_guardrail": topic_title_guardrail,
        "latest_official_source_check": latest_official_source_check,
        "local_context": local_context,
        "internet_context": internet_context,
    }
    raw_output = to_text(reasoner_chain.invoke(payload))
    return strip_thinking_tags(raw_output)


def run_verifier_review(
    verifier_chain,
    title: str,
    target_items: list[str],
    official_fact_card: str,
    topic_title_guardrail: str,
    latest_official_source_check: str,
    fact_sheet: str,
    article_draft: str,
    local_context: str,
    internet_context: str,
) -> str:
    payload = {
        "question": title,
        "target_description": "\n".join(target_items),
        "official_fact_card": official_fact_card,
        "topic_title_guardrail": topic_title_guardrail,
        "latest_official_source_check": latest_official_source_check,
        "fact_sheet": fact_sheet,
        "article_draft": article_draft,
        "local_context": local_context,
        "internet_context": internet_context,
    }
    raw_output = to_text(verifier_chain.invoke(payload))
    return strip_thinking_tags(raw_output)


def verifier_passed(report: str) -> bool:
    return bool(re.search(r"VERDICT:\s*PASS\b", report, flags=re.IGNORECASE))


def extract_verifier_feedback(report: str) -> str:
    match = re.search(
        r"REVISION_INSTRUCTIONS:\s*(.*)",
        report,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    return match.group(1).strip()


def check_completeness(
    llm: ChatOllama,
    output_text: str,
    target_items: list[str],
) -> Optional[str]:
    if not target_items:
        return None

    check_prompt = "\n".join(
        [
            "Given the following article, list which required items are missing.",
            'Return only a bullet list of missing items, or "ALL COVERED" if nothing is missing.',
            "",
            "Required items:",
            *[f"- {item}" for item in target_items],
            "",
            "Article:",
            output_text,
        ]
    )

    try:
        missing = to_text(llm.invoke(check_prompt))
    except Exception as error:
        print(f"      [Completeness] Check skipped: {error}")
        return None

    return None if missing.upper() == "ALL COVERED" else missing


def expand_with_missing(
    llm: ChatOllama,
    output_text: str,
    missing_items: str,
    fact_sheet: str,
    local_context: str,
    internet_context: str,
) -> str:
    expansion_prompt = f"""
The previous article is missing these required points:
{missing_items}

Using the fact sheet and context below, generate a new section that covers only the missing points.
Follow the same style as the original article.
Add the new content as an extra section titled "## Additional Details".
Do not repeat content already present.

<FACT_SHEET>
{fact_sheet}
</FACT_SHEET>

<LOCAL_DB_SOURCES>
{local_context}
</LOCAL_DB_SOURCES>

<WEB_SEARCH_SOURCES>
{internet_context}
</WEB_SEARCH_SOURCES>

Output only the new section and nothing else.
"""

    try:
        new_section = to_text(llm.invoke(expansion_prompt))
        return f"{output_text}\n\n{new_section}".strip()
    except Exception as error:
        print(f"      [Completeness] Expansion skipped: {error}")
        return output_text


def extract_facts(text: str) -> list[str]:
    text_lower = text.lower()
    facts = set()

    facts.update(re.findall(r"\b\d+\s*:\s*\d+\b", text_lower))
    facts.update(
        re.findall(
            r"\b\d+(?:\.\d+)?\s*(?:mm|cm|m|sqm|sq\.?\s?m|ft|in|%)\b", text_lower)
    )
    facts.update(re.findall(r"\b(?:pd|bp|ra)\s*\d+\b", text_lower))
    facts.update(re.findall(
        r"\b(?:rule|section|sec\.?)\s+[a-z0-9().-]+\b", text_lower))

    return sorted(facts)


def verify_facts_against_context(
    facts: list[str],
    context_text: str,
    threshold: float = 0.6,
) -> bool:
    if not facts:
        return True

    context_lower = context_text.lower()
    found = sum(1 for fact in facts if fact in context_lower)
    ratio = found / len(facts)
    print(f"      [FactCheck] {found}/{len(facts)} facts found ({ratio:.0%})")
    return ratio >= threshold


def validate_atomic_coverage(
    content: str,
    target_items: list[str],
    context_text: str,
) -> list[str]:
    content_lower = normalize_for_match(content)
    context_lower = normalize_for_match(context_text)
    missing = []

    for item in target_items:
        normalized_item = normalize_for_match(item)
        is_atomic = bool(
            re.fullmatch(r"\d+:\d+", item)
            or re.fullmatch(r"(?:bp|pd|ra)\s*\d+", item.lower())
            or re.fullmatch(r"(?:19|20)\d{2}", item)
        )
        if not is_atomic:
            continue
        if normalized_item not in context_lower:
            continue
        if normalized_item not in content_lower:
            missing.append(item)

    return missing


def detect_precision_issues(
    content: str,
    context_text: str,
    target_items: list[str],
) -> list[str]:
    content_lower = normalize_for_match(content)
    context_lower = normalize_for_match(context_text)
    joined_targets = normalize_for_match(" ".join(target_items))
    issues = []

    is_ramp_run_topic = (
        "ramp" in joined_targets
        and "maximum run lengths" in joined_targets
        and "1:20" in joined_targets
    )
    if not is_ramp_run_topic:
        return issues

    ambiguous_no_max = (
        "no specified maximum length",
        "no fixed maximum run length",
        "no maximum run length",
        "unlimited",
    )
    content_has_ambiguous_no_max = any(phrase in content_lower for phrase in ambiguous_no_max)
    content_has_dash_row = bool(re.search(r"\|\s*1:20\s*\|\s*-\s*\|", content, flags=re.IGNORECASE))
    context_has_1_20_span_rule = (
        "1:20" in context_lower
        and ("15 m" in context_lower or "15m" in context_lower)
        and (
            "700 mm" in context_lower
            or "700mm" in context_lower
            or "landing" in context_lower
            or "1.80 m" in context_text
            or "1.8 m" in context_text
        )
    )

    if context_has_1_20_span_rule and (content_has_ambiguous_no_max or content_has_dash_row):
        content_has_span_limit = any(
            token in content_lower for token in ("15 m", "15m")
        )
        content_has_landing_precision = (
            (
                any(token in content_lower for token in ("700 mm", "700mm"))
                and any(token in content_lower for token in ("rise interval", "intermediate landing"))
            )
            or any(token in content for token in ("1.80 m", "1.8 m", "1.80m", "1.8m"))
        )
        content_mentions_precision = content_has_span_limit or content_has_landing_precision
        if not content_mentions_precision:
            issues.append(
                "The draft treats the 1:20 ramp as having no maximum length without also stating the span or landing constraint present in the context."
            )

    return issues


def latest_official_source_requires_reconciliation(latest_official_source_check: str) -> bool:
    return "STATUS: POTENTIAL_NEWER_OFFICIAL_SOURCE_FOUND" in latest_official_source_check


def article_acknowledges_recency_warning(content: str) -> bool:
    content_lower = normalize_for_match(content)
    return any(
        phrase in content_lower
        for phrase in (
            "newer official source",
            "may supersede",
            "potentially superseded",
            "latest official source",
        )
    )


def article_satisfies_title_guardrail(
    content: str,
    required_acknowledgement_groups: tuple[tuple[str, ...], ...],
) -> bool:
    if not required_acknowledgement_groups:
        return True

    content_lower = normalize_for_match(content)
    for group in required_acknowledgement_groups:
        if not any(normalize_for_match(term) in content_lower for term in group):
            return False
    return True


def extract_cited_sources(text: str) -> list[str]:
    citations = []
    for citation in re.findall(r"\[([^\[\]]+)\]", text):
        source_name = citation.split(",", 1)[0].strip()
        if len(source_name) >= 4:
            citations.append(source_name)
    return citations


def citations_supported(content: str, local_context: str, internet_context: str) -> bool:
    cited_sources = extract_cited_sources(content)
    if not cited_sources:
        return False

    combined_context = normalize_for_match(
        f"{local_context}\n{internet_context}")
    supported = 0
    for source_name in cited_sources:
        if normalize_for_match(source_name) in combined_context:
            supported += 1

    print(
        f"      [CitationCheck] {supported}/{len(cited_sources)} cited sources found in context")
    return supported == len(cited_sources)


def generate_with_verification(
    reasoner_chain,
    writer_chain,
    strict_writer_chain,
    verifier_chain,
    writer_llm: ChatOllama,
    verifier_llm: ChatOllama,
    title: str,
    target_items: list[str],
    official_fact_card: str,
    topic_title_guardrail: str,
    required_acknowledgement_groups: tuple[tuple[str, ...], ...],
    latest_official_source_check: str,
    local_context: str,
    internet_context: str,
) -> str:
    combined_context = f"{local_context}\n{internet_context}"
    last_content = ""
    verifier_feedback = ""

    print("      [Reasoner] Building evidence fact sheet...")
    fact_sheet = build_fact_sheet(
        reasoner_chain,
        title,
        target_items,
        official_fact_card,
        topic_title_guardrail,
        latest_official_source_check,
        local_context,
        internet_context,
    )

    for attempt in range(1, MAX_GENERATION_ATTEMPTS + 1):
        payload = {
            "local_context": local_context,
            "internet_context": internet_context,
            "question": title,
            "target_description": "\n".join(target_items),
            "official_fact_card": official_fact_card,
            "topic_title_guardrail": topic_title_guardrail,
            "latest_official_source_check": latest_official_source_check,
            "fact_sheet": fact_sheet,
            "verifier_feedback": verifier_feedback,
        }
        active_chain = writer_chain if attempt == 1 else strict_writer_chain
        print(f"      [Writer] Draft attempt {attempt}...")
        raw_output = to_text(active_chain.invoke(payload))
        content = clean_model_output(raw_output)

        missing = check_completeness(verifier_llm, content, target_items)
        if missing:
            print(f"      [Completeness] Missing items: {missing}")
            content = clean_model_output(
                expand_with_missing(
                    writer_llm,
                    content,
                    missing,
                    fact_sheet,
                    local_context,
                    internet_context,
                )
            )
        else:
            print("      [Completeness] All target items covered.")

        facts = extract_facts(content)
        last_content = content
        missing_atomic_items = validate_atomic_coverage(
            content,
            target_items,
            combined_context,
        )
        precision_issues = detect_precision_issues(
            content,
            combined_context,
            target_items,
        )
        title_guardrail_issue = (
            bool(topic_title_guardrail)
            and not article_satisfies_title_guardrail(content, required_acknowledgement_groups)
        )
        recency_issue = (
            latest_official_source_requires_reconciliation(latest_official_source_check)
            and not article_acknowledges_recency_warning(content)
        )
        if missing_atomic_items:
            print(
                f"      [Coverage] Missing atomic items: {', '.join(missing_atomic_items)}")
        if precision_issues:
            print(
                f"      [Precision] {' | '.join(precision_issues)}")
        if title_guardrail_issue:
            print(
                "      [TitleGuardrail] The draft does not explicitly acknowledge the title-overclaim warning."
            )
        if recency_issue:
            print(
                "      [Recency] Potential newer official source found online, but the draft does not reconcile it."
            )

        facts_ok = verify_facts_against_context(facts, combined_context)
        citations_ok = citations_supported(
            content, local_context, internet_context)
        verifier_report = run_verifier_review(
            verifier_chain,
            title,
            target_items,
            official_fact_card,
            topic_title_guardrail,
            latest_official_source_check,
            fact_sheet,
            content,
            local_context,
            internet_context,
        )
        verifier_ok = verifier_passed(verifier_report)
        print(f"      [Verifier] {'PASS' if verifier_ok else 'FAIL'}")

        if facts_ok and citations_ok and not missing_atomic_items and not precision_issues and not title_guardrail_issue and not recency_issue and verifier_ok:
            return content

        feedback_parts = []
        extracted_feedback = extract_verifier_feedback(verifier_report)
        if extracted_feedback:
            feedback_parts.append(extracted_feedback)
        if precision_issues:
            feedback_parts.append(
                "Address these precision issues:\n- " + "\n- ".join(precision_issues)
            )
        if title_guardrail_issue:
            feedback_parts.append(
                "Address this title-overclaim issue:\n- Explicitly acknowledge the title guardrail and explain the official source limitation or scope mismatch."
            )
        if recency_issue:
            feedback_parts.append(
                "Address this latest-source issue:\n- A potentially newer official source was found online. Reconcile it or explicitly state that a newer official source may supersede the local source."
            )
        verifier_feedback = "\n\n".join(feedback_parts)
        if verifier_feedback:
            print(f"      [VerifierFeedback] {verifier_feedback[:220]}")
        if attempt < MAX_GENERATION_ATTEMPTS:
            print(
                "      [Validation] Council checks failed. Retrying with stricter prompt...")

    return last_content


def build_retriever(vectorstore: Optional[Chroma]):
    if vectorstore is None:
        return None

    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": VECTOR_K})

    try:
        total_chunks = vectorstore._collection.count()
    except Exception as error:
        print(
            f"  [!] Could not count Chroma documents. Using vector retrieval only: {error}")
        return vector_retriever

    if total_chunks == 0:
        return vector_retriever

    if total_chunks > BM25_MAX_CHUNKS:
        print(
            f"  [!] Skipping BM25 setup because the index has {total_chunks} chunks "
            f"(limit: {BM25_MAX_CHUNKS})."
        )
        return vector_retriever

    print("Setting up hybrid retrieval (vector + BM25)...")
    all_texts = []
    all_metadatas = []
    offset = 0

    try:
        while offset < total_chunks:
            batch_data = vectorstore._collection.get(
                include=["documents", "metadatas"],
                limit=CHROMA_FETCH_BATCH_SIZE,
                offset=offset,
            )
            all_texts.extend(batch_data.get("documents") or [])
            all_metadatas.extend(batch_data.get("metadatas") or [])
            offset += CHROMA_FETCH_BATCH_SIZE
    except Exception as error:
        print(
            f"  [!] BM25 setup failed during collection fetch. Using vector retrieval only: {error}")
        return vector_retriever

    if not all_texts:
        return vector_retriever

    try:
        bm25_retriever = BM25Retriever.from_texts(
            all_texts, metadatas=all_metadatas)
        bm25_retriever.k = BM25_K
        print(f"  [+] Loaded {len(all_texts)} chunks into BM25.")
        return EnsembleRetriever(
            retrievers=[vector_retriever, bm25_retriever],
            weights=[0.6, 0.4],
        )
    except Exception as error:
        print(f"  [!] BM25 setup failed. Using vector retrieval only: {error}")
        return vector_retriever


def retrieve_local_docs(
    retriever,
    vectorstore: Optional[Chroma],
    query: str,
    memory_store: Optional[MemoryStore] = None,
) -> list[Document]:
    gathered_docs = []

    if memory_store is not None:
        try:
            gathered_docs.extend(memory_store.search_snippets(
                query, limit=MEMORY_SNIPPET_LIMIT))
            gathered_docs.extend(memory_store.search_source_summaries(
                query, limit=MEMORY_SUMMARY_LIMIT))
        except Exception as error:
            print(f"  [!] Memory retrieval failed for '{query}': {error}")

    for query_variant in build_query_variants(query):
        if retriever is not None:
            try:
                docs = retriever.invoke(query_variant)
                gathered_docs.extend(
                    [doc for doc in docs if isinstance(doc, Document)])
            except Exception as error:
                print(
                    f"  [!] Hybrid retrieval failed for '{query_variant}'. Falling back to vector search: {error}")

        if vectorstore is not None:
            try:
                gathered_docs.extend(
                    vectorstore.similarity_search(query_variant, k=VECTOR_K))
            except Exception as error:
                print(
                    f"  [!] Vector retrieval failed for '{query_variant}': {error}")

    if gathered_docs:
        return rank_documents_for_query(gathered_docs, query)

    if retriever is not None:
        try:
            docs = retriever.invoke(query)
            return rank_documents_for_query(
                [doc for doc in docs if isinstance(doc, Document)],
                query,
            )
        except Exception as error:
            print(
                f"  [!] Hybrid retrieval failed for '{query}'. Falling back to vector search: {error}")

    if vectorstore is not None:
        try:
            return rank_documents_for_query(vectorstore.similarity_search(query, k=VECTOR_K), query)
        except Exception as error:
            print(f"  [!] Vector retrieval failed for '{query}': {error}")

    return []


def format_local_context(documents: list[Document], query: str) -> str:
    if not documents:
        return "No local context retrieved."

    blocks = []
    total_chars = 0
    query_terms = extract_query_terms(query)

    for doc in rank_documents_for_query(documents, query):
        source = normalize_source_path(
            doc.metadata.get("source")) or "Unknown source"
        label = Path(source).name
        page = doc.metadata.get("page")
        page_label = f" | page {int(page) + 1}" if isinstance(page,
                                                              int) else ""
        authority_label = doc.metadata.get(
            "_authority_label", "MEDIUM AUTHORITY")
        relevance_score = doc.metadata.get("_relevance_score", 0)
        memory_kind = doc.metadata.get("_memory_kind")
        snippet = extract_relevant_snippet(
            doc.page_content.strip(),
            query_terms,
            MAX_DOC_SNIPPET_CHARS,
        )

        block = (
            f"SOURCE: {label}{page_label}\n"
            f"AUTHORITY: {authority_label}\n"
            f"RELEVANCE_SCORE: {relevance_score}\n"
            f"MEMORY_KIND: {str(memory_kind).upper() if memory_kind else 'VECTOR_OR_BM25'}\n"
            f"{snippet}"
        )
        projected_chars = total_chars + len(block) + 4
        if projected_chars > MAX_LOCAL_CONTEXT_CHARS:
            break

        blocks.append(block)
        total_chars = projected_chars

    return "\n\n--\n\n".join(blocks) if blocks else "No local context retrieved."


def format_exact_evidence(documents: list[Document], query: str) -> str:
    exact_docs = [
        doc for doc in rank_documents_for_query(documents, query)
        if doc.metadata.get("_memory_kind") == "exact_snippet"
    ]
    if not exact_docs:
        return "No exact memory evidence retrieved."

    blocks = []
    total_chars = 0
    query_terms = extract_query_terms(query)

    for doc in exact_docs:
        source = normalize_source_path(
            doc.metadata.get("source")) or "Unknown source"
        label = Path(source).name
        page = doc.metadata.get("page")
        page_label = f" | page {int(page) + 1}" if isinstance(page,
                                                              int) else ""
        authority_label = doc.metadata.get(
            "_authority_label", "MEDIUM AUTHORITY")
        snippet = extract_relevant_snippet(
            doc.page_content.strip(),
            query_terms,
            min(MAX_DOC_SNIPPET_CHARS, 1600),
        )
        block = (
            f"EVIDENCE_SOURCE: {label}{page_label}\n"
            f"AUTHORITY: {authority_label}\n"
            f"{snippet}"
        )
        projected_chars = total_chars + len(block) + 4
        if projected_chars > min(MAX_LOCAL_CONTEXT_CHARS, 9000):
            break

        blocks.append(block)
        total_chars = projected_chars

    return "\n\n--\n\n".join(blocks) if blocks else "No exact memory evidence retrieved."


def merge_local_context(
    local_context: str,
    exact_evidence: str,
) -> str:
    blocks = []

    if exact_evidence and exact_evidence != "No exact memory evidence retrieved.":
        blocks.append(
            "<EXACT_MEMORY_EVIDENCE>\n"
            f"{exact_evidence}\n"
            "</EXACT_MEMORY_EVIDENCE>"
        )

    if blocks:
        blocks.append(
            "<RETRIEVED_LOCAL_CONTEXT>\n"
            f"{local_context}\n"
            "</RETRIEVED_LOCAL_CONTEXT>"
        )
        return "\n\n".join(blocks)

    return local_context


def fetch_internet_context(
    web_search: Optional[TavilySearch],
    title: str,
) -> tuple[str, str, bool]:
    latest_official_source_check, newer_official_source_found = build_latest_official_source_check(
        web_search,
        title,
    )

    if web_search is None:
        return "Web search unavailable.", latest_official_source_check, newer_official_source_found

    search_query = f"{title} Philippines official technical requirements history architecture"
    try:
        results = web_search.invoke(search_query)
        context = summarize_tavily_results(results)
        return context, latest_official_source_check, newer_official_source_found
    except Exception as error:
        print(f"  [!] Web warning: {error}")
        return "Web search unavailable.", latest_official_source_check, newer_official_source_found


def should_generate_article(file_path: Path, force_regenerate: bool = False) -> tuple[bool, str]:
    if force_regenerate:
        return True, ""

    if not file_path.exists():
        return True, ""

    if file_path.stat().st_size <= THIN_FILE_BYTES:
        print(f"  [~] Found thin file for '{file_path.name}'. Regenerating...")
        return True, ""

    try:
        return False, file_path.read_text(encoding="utf-8")
    except Exception:
        return False, file_path.read_text(encoding="utf-8", errors="ignore")


def generate_articles(
    vectorstore: Optional[Chroma],
    retriever,
    model_council: dict[str, ChatOllama],
    web_search: Optional[TavilySearch],
    memory_store: Optional[MemoryStore] = None,
    target_content: Optional[dict[str, list[str]]] = None,
    force_regenerate: bool = False,
) -> list[dict[str, object]]:
    print("\nWriting ALE review modules...")

    writer_llm = model_council["writer"]
    verifier_llm = model_council["verifier"]
    reasoner_chain = build_prompt_chain(
        model_council["reasoner"],
        system_text=FACT_SYSTEM_INSTRUCTIONS,
        human_template=FACT_HUMAN_TEMPLATE,
    )
    writer_chain = build_prompt_chain(writer_llm, strict=False)
    strict_writer_chain = build_prompt_chain(writer_llm, strict=True)
    verifier_chain = build_prompt_chain(
        verifier_llm,
        system_text=VERIFIER_SYSTEM_INSTRUCTIONS,
        human_template=VERIFIER_HUMAN_TEMPLATE,
    )
    article_stats = []
    active_target_content = target_content or TARGET_CONTENT

    for subtopic, articles in active_target_content.items():
        subfolder_path = OUTPUT_FOLDER / safe_filename(subtopic)
        subfolder_path.mkdir(parents=True, exist_ok=True)

        for title in articles:
            file_path = subfolder_path / f"{safe_filename(title)}.md"
            needs_generation, content = should_generate_article(
                file_path,
                force_regenerate=force_regenerate,
            )

            if needs_generation:
                print(f"\n[Search] Gathering data for: {title}")
                target_items = build_target_items(title)
                matched_fact_cards = DEFAULT_CANONICAL_FACT_REGISTRY.find_all(title)
                official_fact_card = DEFAULT_CANONICAL_FACT_REGISTRY.resolve_content(title)
                topic_title_guardrail, required_acknowledgement_groups = DEFAULT_CANONICAL_FACT_REGISTRY.resolve_title_guardrail(
                    title
                )
                local_docs = retrieve_local_docs(
                    retriever, vectorstore, title, memory_store)
                local_context = format_local_context(local_docs, title)
                exact_evidence = format_exact_evidence(local_docs, title)
                grounded_local_context = merge_local_context(
                    local_context, exact_evidence)
                source_signature = ""
                cached_topic = None

                if official_fact_card:
                    print(
                        "  [Authority] Applied canonical official fact cards: "
                        + ", ".join(card.card_id for card in matched_fact_cards)
                    )
                if topic_title_guardrail:
                    print("  [Authority] Applied title-overclaim guardrail.")

                if memory_store is not None:
                    source_signature = memory_store.build_topic_source_signature(
                        local_docs)
                    if not force_regenerate:
                        cached_topic = memory_store.get_topic_cache(
                            title, source_signature)

                if cached_topic and len(cached_topic.get("content", "").strip()) >= MIN_ARTICLE_CHARS:
                    print(
                        "  [Cache] Reusing cached article for unchanged source set.")
                    content = cached_topic["content"]
                    local_context = cached_topic.get(
                        "local_context") or local_context
                    exact_evidence = cached_topic.get(
                        "exact_evidence") or exact_evidence
                else:
                    print("  [Web] Fetching supplemental official context...")
                    internet_context, latest_official_source_check, newer_official_source_found = fetch_internet_context(
                        web_search, title)
                    if newer_official_source_found:
                        print("  [Recency] Potential newer official source detected online.")

                    print("  [Council] Reasoning, writing, and verifying article...")
                    content = generate_with_verification(
                        reasoner_chain,
                        writer_chain,
                        strict_writer_chain,
                        verifier_chain,
                        writer_llm,
                        verifier_llm,
                        title,
                        target_items,
                        official_fact_card,
                        topic_title_guardrail,
                        required_acknowledgement_groups,
                        latest_official_source_check,
                        grounded_local_context,
                        internet_context,
                    )

                    units = re.findall(
                        r"\d+(?:\.\d+)?\s*(?:mm|cm|m|%)", content.lower())
                    word_count = len(content.split())
                    tech_score = len(units)
                    print(
                        f"  [Audit] Word Count: {word_count} | Tech Score: {tech_score}")

                if len(content.strip()) >= MIN_ARTICLE_CHARS:
                    file_path.write_text(content, encoding="utf-8")
                    print("  [OK] Article saved.")
                    if memory_store is not None:
                        if not source_signature:
                            source_signature = memory_store.build_topic_source_signature(
                                local_docs)
                        memory_store.set_topic_cache(
                            title=title,
                            source_signature=source_signature,
                            article_path=str(file_path),
                            content=content,
                            local_context=local_context,
                            exact_evidence=exact_evidence,
                            target_items=target_items,
                            used_sources=collect_used_sources(local_docs),
                        )
                else:
                    print("  [!] Article was too short. Skipping save.")

            word_count = len(content.split())
            status = "Complete" if word_count > 2000 else "Review Needed"
            article_stats.append(
                {
                    "Subtopic": subfolder_path.name,
                    "Title": title,
                    "Words": word_count,
                    "Status": status,
                    "Path": str(file_path),
                }
            )

    return article_stats


def print_summary(article_stats: list[dict[str, object]]) -> None:
    total = len(article_stats)
    completed = sum(1 for row in article_stats if row["Status"] == "Complete")
    needs_review = total - completed
    print("\nAll done.")
    print(f"  [+] Articles tracked: {total}")
    print(f"  [+] Complete: {completed}")
    print(f"  [+] Review Needed: {needs_review}")


def validate_paths() -> None:
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
    if not DATA_FOLDER.exists():
        raise FileNotFoundError(f"Data folder not found: {DATA_FOLDER}")


def main() -> None:
    args = parse_args()
    load_dotenv(
        dotenv_path=Path(__file__).resolve().parent / ".local.env",
        override=False,
    )
    configure_logging()
    validate_paths()
    print(
        "Run mode: "
        f"force_regenerate={args.force_regenerate}, "
        f"rebuild_memory={args.rebuild_memory}, "
        f"skip_web={args.skip_web}"
    )
    filtered_target_content = filter_target_content(args.topic)

    if not filtered_target_content:
        print("No matching topics found for the provided --topic filter.")
        return

    print("Initializing embeddings...")
    embeddings = load_embeddings()

    vectorstore = open_vectorstore(embeddings)
    existing_sources = get_existing_sources(vectorstore)

    new_documents = collect_new_documents(existing_sources)
    vectorstore = index_documents(new_documents, vectorstore, embeddings)

    memory_store = MemoryStore(
        MEMORY_DIR,
        stopwords=STOPWORDS,
        official_source_hints=OFFICIAL_SOURCE_HINTS,
        low_trust_source_hints=LOW_TRUST_SOURCE_HINTS,
    )

    try:
        print("Refreshing persistent memory...")
        memory_stats = memory_store.refresh_from_vectorstore(
            vectorstore,
            batch_size=CHROMA_FETCH_BATCH_SIZE,
            force=args.rebuild_memory,
            progress_callback=print,
        )
        print(
            "  [+] Memory sources seen: "
            f"{memory_stats['sources_seen']} | refreshed: {memory_stats['sources_refreshed']} | "
            f"skipped: {memory_stats['sources_skipped']}"
        )

        print("Initializing local AI council...")
        model_council = build_model_council()
        web_search = None if args.skip_web else build_web_search()
        retriever = build_retriever(vectorstore)

        article_stats = generate_articles(
            vectorstore,
            retriever,
            model_council,
            web_search,
            memory_store=memory_store,
            target_content=filtered_target_content,
            force_regenerate=args.force_regenerate,
        )
        print_summary(article_stats)
    finally:
        memory_store.close()


if __name__ == "__main__":
    main()
