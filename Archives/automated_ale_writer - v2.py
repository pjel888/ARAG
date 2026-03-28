# ./venv/Scripts/python.exe automated_ale_writer.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.documents import Document
from langchain_classic.chains import RetrievalQA
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain_core.output_parsers import StrOutputParser
from langchain_tavily import TavilySearch
import os
import glob
import pandas as pd
from pptx import Presentation
import re

# --- 1. CONFIGURATION ---
# Put your actual API key right here
os.environ["TAVILY_API_KEY"] = "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"

DATA_FOLDER = "./RAG - ALE ARCHITECTURE BOARD EXAM"
OUTPUT_FOLDER = "./ALE_Reviewer_Library"
DB_DIR = "./chroma_db"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

TARGET_CONTENT = {
    "Accessibility Standards (BP 344 - RA 9442)": [
        "BP 344 (2024 IRR): Ramp Slope Tiers (1:20, 1:15, 1:12) and Maximum Run Lengths",
        "BP 344 (2024 IRR): Accessible Washrooms – Clearance, Grab Bars, and Fixture Heights",
        "BP 344 (2024 IRR): Tactile Warning Surfaces, Braille Signage, and Visual Alarms",
        "RA 9442: Mandatory PWD Privileges, Incentives, and Design Integration",
        "Dimensions for Wheelchair Maneuvering, Parking Slots (4.00m min.), and Passing Spaces"
    ],
    "National Building Code Application (PD 1096)": [
        "PD 1096 Rule VII: Classification and General Requirements of all Buildings",
        "PD 1096 Rule VIII: Light and Ventilation (Window Sizes and Court Dimensions)",
        "PD 1096 Rule XII: General Requirements for Egress and Occupant Loads",
        "Calculating GFA, TGFA, PSO, and Building Height Limits (BHL)",
        "Building Permit Process, Fines, and the Role of the Building Official"
    ],
    "Housing & Human Settlements (BP 220 - PD 957)": [
        "BP 220: Technical Standards for Socialized and Economic Housing",
        "PD 957: Subdivision and Condominium Buyer's Protective Decree",
        "Comparison of Road Widths and Open Space: BP 220 vs PD 957",
        "Housing Policies and Relocation Strategies for Informal Settlements"
    ],
    "Anthropometrics & Human Dimensions": [
        "Anthropometrics: Standard Human Body Dimensions (Standing, Sitting, Reaching)",
        "Residential Clearances: Kitchen Work Triangles and Bedroom Layouts",
        "Commercial Clearances: Office Workstations and Retail Aisle Widths",
        "Human Dimensions for Institutional Design (Schools and Hospitals)"
    ],
    "Planning: Environmental Factors & Site Analysis": [
        "Microclimate Analysis: Wind Paths (Amihan/Habagat) and Solar Orientation",
        "Topography and Slope Analysis: Cut-and-Fill and Buildability Limits",
        "Geological Hazards: Identifying Fault Lines, Liquefaction, and Flood Zones",
        "Hydrology in Site Planning: Stormwater Runoff and Drainage Systems"
    ],
    "History: Philippine Architecture & Identity": [
        "Pre-Colonial Vernacular: The Evolution of the Bahay Kubo",
        "Spanish Colonial Era: The Bahay na Bato and Earthquake Baroque",
        "American Colonial Era: Daniel Burnham’s Manila and the Pensionado Architects",
        "Masters of the Golden Age: Juan Nakpil, Pablo Antonio, and Leandro Locsin",
        "The Search for Modern Filipino Identity: Mañosa and the New Vernacular"
    ],
    "ALE Mastery & Study Strategies": [
        "Architectural Design & Site Planning: Mastery and Study Strategy",
        "Building Utilities & MEPF: Integrated Review and Connections",
        "Building Materials & Construction: Common Board Exam Materials",
        "Professional Practice & Jurisprudence: The 15-Year Liability Framework",
        "Structural Conceptualization: Load Paths and Seismic Zone 4 Rules"
    ]
}

# --- 2. GPU EMBEDDINGS ---
print("Waking up the RTX 4070...")
embeddings = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2",
    model_kwargs={'device': 'cuda'}
)

# --- 3. SMART LOADING (SQL Paginated Fix) ---
existing_sources = set()
if os.path.exists(DB_DIR):
    print("Database found! Safely fetching existing index (Paginated)...")
    vectorstore = Chroma(persist_directory=DB_DIR,
                         embedding_function=embeddings)
    try:
        count = vectorstore._collection.count()
        offset, limit = 0, 5000
        while offset < count:
            batch_data = vectorstore._collection.get(
                include=['metadatas'], limit=limit, offset=offset)
            for meta in batch_data['metadatas']:
                if meta and 'source' in meta:
                    existing_sources.add(meta['source'])
            offset += limit
        print(
            f" [+] Verified {len(existing_sources)} existing source files in the brain.")
    except Exception as e:
        print(f" [!] Metadata fetch issue: {e}")
else:
    vectorstore = None

# --- 4. DOCUMENT LOADING & CLEANING ---
print("Scanning for documents...")
new_docs = []
all_files = glob.glob(os.path.join(DATA_FOLDER, "**", "*.*"), recursive=True)
for file_path in all_files:
    abs_path = os.path.abspath(file_path)
    if abs_path in existing_sources:
        continue
    ext = abs_path.lower().split('.')[-1]
    try:
        if ext == 'pdf':
            loader = PyPDFLoader(abs_path)
            new_docs.extend([d for d in loader.load() if d.page_content and len(
                d.page_content.strip()) > 5])
        elif ext == 'docx':
            loader = Docx2txtLoader(abs_path)
            new_docs.extend(loader.load())
        elif ext == 'pptx':
            prs = Presentation(abs_path)
            text = " ".join(
                [shape.text for slide in prs.slides for shape in slide.shapes if hasattr(shape, "text")])
            if len(text.strip()) > 10:
                new_docs.append(Document(page_content=text,
                                metadata={"source": abs_path}))
    except Exception:
        continue

# --- 5. UNSTOPPABLE BATCHER ---
if new_docs:
    print(f"Slicing {len(new_docs)} new sections...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=100)
    valid_chunks = [c for c in text_splitter.split_documents(new_docs) if isinstance(
        c.page_content, str) and len(c.page_content.strip()) > 10]
    batch_size = 500
    for i in range(0, len(valid_chunks), batch_size):
        batch = valid_chunks[i: i + batch_size]
        try:
            if not vectorstore:
                vectorstore = Chroma.from_documents(
                    documents=batch, embedding=embeddings, persist_directory=DB_DIR)
            else:
                vectorstore.add_documents(batch)
            print(f"  [#] Batch {i//batch_size + 1} indexed...")
        except Exception:
            for chunk in batch:
                try:
                    vectorstore.add_documents([chunk])
                except:
                    continue
else:
    print("Database up to date! Jumping to generation.")

# --- 6. SIMPLIFIED, DIRECT SYSTEM PROMPT ---
llm = ChatOllama(
    model="qwen2.5:14b-instruct",
    temperature=0,             # Absolute precision
    num_ctx=16384,             # Larger window to fit more RAG context
    repeat_penalty=1.2,
    top_p=0.1                  # Forces the model to stick to the most likely facts
)

web_search = TavilySearch(max_results=3)

system_instructions = r"""
You are the UAP Architecture Board Exam Chairman writing the definitive ALE reviewer.
Your chapters must be both **comprehensive** (2500–3500 words) and **factually accurate**.
Follow the structure and style of the example below, but adapt the content to the given topic.

---

**EXAMPLE (Ramp Slopes – correct data):**

## What You Need to Know for the ALE
**Scenario:** On the ALE, you may encounter a problem like: “A proposed ramp has a total rise of 0.70 m. If the site allows a maximum run of 12 m, what slope must be used to comply with BP 344 (2024 IRR)?” Many candidates incorrectly calculate the slope as 1:12 without checking the run limit, leading to a non‑compliant design. To master this topic, memorise:
- Maximum gradient tiers: 1:12, 1:15, 1:20
- Run = Rise × slope ratio (e.g., for 1:15, Run = Rise × 15)
- Landing intervals: every 8 m for 1:12, every 10 m for 1:15, every 12 m for 1:20
- Minimum width: 1.20 m; landing length: 1.50 m

## Core Concept
**Historical/Legal Context:** BP 344 (Accessibility Law) was updated in 2024 to align with international standards. The 2024 IRR sets clear technical requirements for ramps, including slope tiers, run limits, and landing dimensions.

**Definitions:**
- **Ramp:** A sloped pedestrian way with gradient >5%.
- **Gradient (slope):** Ratio of vertical rise to horizontal run (e.g., 1:12 means 1 unit rise for every 12 units run).
- **Maximum Rise per Run:** The greatest vertical height allowed in one continuous ramp segment.
- **Landing:** A level platform at top, bottom, and intermediate points.

**Specific Dimensions and Formulas (2024 IRR):**
- Maximum gradient for new construction: **1:12**
- For 1:12: \( \text{{Run}} = \text{{Rise}} \times 12 \)
- For 1:15: \( \text{{Run}} = \text{{Rise}} \times 15 \)
- For 1:20: \( \text{{Run}} = \text{{Rise}} \times 20 \)
- Maximum rise per run (for any slope): **0.70 m** (700 mm)
- Minimum ramp width: **1.20 m**
- Landing length (minimum): **1.50 m** (same width as ramp)
- Intermediate landings required every **8 m** of horizontal run for 1:12 slopes; every **10 m** for 1:15; every **12 m** for 1:20.

**Analogies:**
1. **Ramp as a gentle hill:** The flatter the slope, the easier to climb.
2. **Slope ratio as a ruler:** For 1:12, every metre of rise needs 12 m of run.
3. **Landings as bus stops:** They provide rest and turning space.

**Practical Design Implications:** In dense urban areas like Manila, space constraints often force steeper slopes, but the 2024 IRR mandates that steeper ramps must be shorter and have more frequent landings.

**Links to Other Subjects:** Structural (loads on ramps), Utilities (drainage), History (evolution of accessibility laws).

---

Now produce a chapter on the given topic, following the structure and level of detail shown in the example. Use the correct formulas and dimensions provided above for any accessibility‑related topics. If the topic is different, infer similar technical standards from your knowledge.

## What You Need to Know for the ALE
**Craft a realistic board exam scenario** that tests the key concepts of the topic. Describe the question or design problem, then explain why candidates often miss it. Finally, outline the 4–5 critical concepts the examinee must master.

## Core Concept
Provide an in‑depth explanation covering:
- Historical/legal context, especially the 2024 IRR updates.
- Definitions of key terms.
- Specific dimensions, formulas (using LaTeX). **Double‑check that your formulas are mathematically correct** (e.g., for slope 1:n, rise = run / n, or run = rise × n).
- At least 3 analogies to clarify.
- Practical design implications in the Philippine context.
- Links to other ALE subjects (Structural, Utilities, History).

## Key Facts and Testable Items
Create a markdown table with at least 12 rows. Columns:
| Code Reference | Requirement | Dimension / Formula | Exam Trap / 2024 Update |
Include exact code sections and use LaTeX for all formulas. Flag 2024 IRR updates.

## How It’s Tested on the ALE
List 4–5 typical question patterns. For each:
- Describe the question style.
- Explain what concept it tests.
- Provide a short example or strategy.
- Include one sample problem with a **correct step‑by‑step solution** using LaTeX.

## Common Mistakes
List 5–7 common mistakes. For each:
- State the misconception.
- Give the correct understanding.
- Explain how to avoid it.

## Key Terms
Provide at least 10 technical terms with concise definitions. Use a bulleted list or table.

## Source
List your sources (e.g., “2024 IRR of BP 344; PD 1096; Author, Title, Year”).

Now produce the chapter.
"""


human_template = r"""
USER QUERY: {question}

<CONTEXT_START>
<LOCAL_DB>
{local_context}
</LOCAL_DB>

<WEB_SEARCH>
{internet_context}
</WEB_SEARCH>
<CONTEXT_END>

Analyze the context above. If the context contains conflicting dimensions, use the most recent (2024). 
If the information is missing, do not hallucinate; focus deeply on the parts of the topic that ARE present.

Begin writing the chapter:
"""

# Re-initialize the prompt and chain
PROMPT = ChatPromptTemplate.from_messages([
    ("system", system_instructions),
    ("human", human_template)
])

hybrid_chain = PROMPT | llm | StrOutputParser()

# --- Helper to strip reasoning output ---


def clean_deepseek_output(text):
    """Remove anything before the first markdown heading (##)."""
    match = re.search(r'##\s+', text)
    if match:
        return text[match.start():]
    return text


# --- 7. HYBRID GENERATION & CONTENT AUDIT ---
print("\nWRITING CONNECTED MASTERCLASS ARTICLES...")
article_stats = []

for subtopic, articles in TARGET_CONTENT.items():
    clean_subfolder = subtopic.replace(
        ":", " -").replace("/", "-").replace("?", "").replace('"', "")
    subfolder_path = os.path.join(OUTPUT_FOLDER, clean_subfolder)
    os.makedirs(subfolder_path, exist_ok=True)

    for title in articles:
        safe_name = title.replace(
            ":", " -").replace("/", "-").replace("?", "").replace('"', "") + ".md"
        file_path = os.path.join(subfolder_path, safe_name)

        needs_generation = True
        content = ""
        if os.path.exists(file_path):
            if os.path.getsize(file_path) > 1500:
                needs_generation = False
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            else:
                print(f"  [↻] Found thin file for '{title}'. Regenerating...")

        if needs_generation:
            print(f"\n[Search] Gathering data for: {title}...")

            # 1. Retrieval from your local Chroma DB (High density)
            local_context = ""
            if vectorstore:
                local_docs = vectorstore.similarity_search(title, k=20)
                local_context = "\n--\n".join(
                    [f"SOURCE {d.metadata.get('source')}:\n{d.page_content}" for d in local_docs])

            # 2. Retrieval from Web (Tavily)
            print("  [🌐] Pinging Tavily API for live context...")
            try:
                internet_results = web_search.invoke(
                    f"{title} BP 344 PD 1096 Philippines 2024 IRR technical")
                internet_context = str(internet_results)
            except Exception as e:
                print(f"  [!] Web warning: {e}")
                internet_context = "Web search unavailable."

            # 3. Execution using the grounded prompt
            print(f"  [✍️] Writing grounded 2500+ word chapter...")
            try:
                # This is the call that uses the new separate context fields
                raw_content = hybrid_chain.invoke({
                    "local_context": local_context,
                    "internet_context": internet_context,
                    "question": title
                })
                content = clean_deepseek_output(raw_content)

                # Audit logic
                units = re.findall(
                    r'\d+(?:\s?mm|\s?m|\s?cm|\s?%|\s?deg)', content.lower())
                latex_matches = re.findall(r'\\\(|\\\[|\$', content)
                c_word_count = len(content.split())
                tech_score = len(units) + len(latex_matches)

                print(
                    f"  [Audit] Word Count: {c_word_count} | Tech Score: {tech_score}")

                if len(content.strip()) > 500:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(content)
                    print("  [✓] Successfully written and saved.")
                else:
                    print("  [!] LLM returned empty or too short. Skipping save.")
                    content = ""

            except Exception as e:
                print(f"  [!] Generation Error: {e}")
                content = ""

        word_count = len(content.split())
        status = "✅ Complete" if word_count > 2000 else "⚠️ Review Needed"
        article_stats.append({
            "Subtopic": clean_subfolder,
            "Title": title,
            "Words": word_count,
            "Status": status,
            "Path": f"./{clean_subfolder}/{safe_name}"
        })
