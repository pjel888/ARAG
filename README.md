# ARAG — Local RAG for ALE review modules

This repository runs a **local retrieval-augmented generation (RAG)** pipeline that ingests Philippine architecture board-exam source material (PDF, DOCX, PPTX), indexes it in **Chroma**, and uses **Ollama** models to draft structured **Architecture Licensure Exam (ALE)** review articles. Optional **Tavily** search adds supplemental web context from configured official domains.

## What it does

- **Index** supported documents under a configurable data folder into a persistent **Chroma** vector store, with optional **BM25 + vector** hybrid retrieval.
- **Remember** per-source summaries and snippets in a local **SQLite** memory store (`.ale_memory/`).
- **Ground** generation with **canonical fact cards** (JSON) for high-priority official facts and title guardrails — see [`canonical_facts/README.md`](canonical_facts/README.md).
- **Generate** Markdown articles via a small **council** of models: a reasoner (fact sheet), writer, and verifier, with optional completeness and citation checks.

Main entrypoint: [`automated_ale_writer.py`](automated_ale_writer.py). Supporting modules: [`ale_memory_store.py`](ale_memory_store.py), [`ale_canonical_facts.py`](ale_canonical_facts.py).

## Prerequisites

- **Python 3.10+** (version aligned with your virtual environment).
- **Ollama** running locally, with the models you reference via environment variables (defaults assume models such as `qwen2.5:14b-instruct` and `deepseek-r1:14b` — adjust to what you have pulled).
- **Tavily API key** if you want web search (disabled with `--skip-web`).

## Setup

1. Clone the repository and create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/Scripts/activate    # Linux/macOS/Git Bash
   # or: .venv\Scripts\activate     # Windows cmd/PowerShell
   ```

2. Install dependencies (there is no root `requirements.txt`; install the packages your environment needs). The main script expects libraries such as:

   `python-dotenv`, `pandas`, `pdfplumber`, `langchain-core`, `langchain-community`, `langchain-chroma`, `langchain-huggingface`, `langchain-ollama`, `langchain-text-splitters`, `langchain-tavily`, `sentence-transformers`, and `python-pptx` (for PPTX). Example:

   ```bash
   pip install python-dotenv pandas pdfplumber langchain-chroma langchain-community langchain-core langchain-huggingface langchain-ollama langchain-text-splitters langchain-tavily sentence-transformers python-pptx
   ```

   Adjust versions to match your stack if you hit conflicts.

3. **Secrets:** copy or create `.local.env` in the repository root (this file is gitignored):

   ```env
   TAVILY_API_KEY=your_key_here
   ```

   The app loads it automatically on startup via `load_dotenv`. You can also set `TAVILY_API_KEY` in the shell.

4. **Source documents:** place PDF / DOCX / PPTX files under the data folder. By default the script expects:

   `./RAG - ALE ARCHITECTURE BOARD EXAM`

   Override with `ALE_DATA_FOLDER` if your path differs.

## Run

From the repo root, with the venv activated:

```bash
python automated_ale_writer.py
```

Or call the interpreter explicitly:

```bash
./venv/Scripts/python.exe automated_ale_writer.py
```

### Useful CLI flags

| Flag | Meaning |
|------|--------|
| `--topic TEXT` | Only process subtopics/titles matching this string (repeatable). |
| `--reuse-existing` | Skip regenerating articles that already exist (when not thin). |
| `--skip-memory-rebuild` | Do not rebuild the SQLite memory tables from Chroma first. |
| `--skip-web` | Disable Tavily (offline / no API key). |

Defaults in code tend toward **force regenerate** and **rebuild memory**; see `parse_args()` in `automated_ale_writer.py` for exact behavior.

## Configuration (environment variables)

Paths and behavior are controlled with `ALE_*` variables (see the top of `automated_ale_writer.py`). Common ones:

| Variable | Role |
|----------|------|
| `ALE_DATA_FOLDER` | Input documents root (default: `./RAG - ALE ARCHITECTURE BOARD EXAM`) |
| `ALE_OUTPUT_FOLDER` | Generated Markdown library (default: `./ALE_Reviewer_Library`) |
| `ALE_DB_DIR` | Chroma persistence directory (default: `./chroma_db`) |
| `ALE_MEMORY_DIR` | SQLite memory store (default: `./.ale_memory`) |
| `ALE_EMBED_MODEL` | Hugging Face embedding model name (default: `all-MiniLM-L6-v2`) |
| `ALE_OLLAMA_MODEL` | Default writer/chat model when not overridden |
| `ALE_REASONER_MODEL` / `ALE_WRITER_MODEL` / `ALE_VERIFIER_MODEL` | Council models |
| `ALE_ENABLE_WEB_SEARCH` | Set to `0` / `false` / `no` to disable web search without `--skip-web` |
| `TAVILY_API_KEY` | Tavily API key (or use `.local.env`) |

## Repository layout (high level)

| Path | Purpose |
|------|---------|
| `automated_ale_writer.py` | CLI, indexing, retrieval, generation pipeline |
| `ale_memory_store.py` | SQLite-backed memory and topic cache |
| `ale_canonical_facts.py` | Loads JSON fact cards from `canonical_facts/cards/` |
| `canonical_facts/` | Canonical fact card definitions and [documentation](canonical_facts/README.md) |
| `Archives/` | Older scripts and archived library snapshots |

Generated or machine-local paths (`chroma_db/`, `.ale_memory/`, virtualenvs, `.local.env`) should stay out of version control — see `.gitignore`.

## License

Add a license file if you plan to distribute the project; none is set in this README by default.
