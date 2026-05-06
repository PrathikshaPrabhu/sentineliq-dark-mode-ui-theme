import os
import logging

_collection = None

# Day 12 — 10 domain knowledge documents seeded into ChromaDB
DOMAIN_DOCUMENTS = [
    {
        "id": "doc1",
        "text": "Dark mode reduces eye strain in low-light environments by using dark backgrounds with light text."
    },
    {
        "id": "doc2",
        "text": "High contrast ratios of at least 4.5:1 are required for WCAG AA accessibility compliance in dark themes."
    },
    {
        "id": "doc3",
        "text": "Neon accent colors like electric blue (#00BFFF) and green (#39FF14) work well against dark backgrounds (#1a1a2e)."
    },
    {
        "id": "doc4",
        "text": "Typography in dark mode should use slightly lighter font weights as dark backgrounds make text appear bolder."
    },
    {
        "id": "doc5",
        "text": "Spacing in dark mode UIs should follow an 8px grid system for visual consistency and alignment."
    },
    {
        "id": "doc6",
        "text": "Avoid pure black (#000000) backgrounds; use dark navy or charcoal (#121212, #1a1a2e) for a softer dark mode."
    },
    {
        "id": "doc7",
        "text": "Sidebar navigation in dark mode works best with a slightly lighter shade than the main background to create depth."
    },
    {
        "id": "doc8",
        "text": "Color temperature matters: cool blues and purples feel modern in dark themes; warm oranges feel energetic."
    },
    {
        "id": "doc9",
        "text": "Interactive elements in dark mode need clear hover and focus states — use subtle glows or border highlights."
    },
    {
        "id": "doc10",
        "text": "Icons in dark mode should use outlined styles rather than filled to appear lighter and less heavy on dark backgrounds."
    },
]


# Day 11 — Pre-load ChromaDB at startup
def init_chroma():
    global _collection
    try:
        import chromadb
        chroma_path = os.getenv("CHROMA_DATA_PATH", "./chroma_data")
        client = chromadb.PersistentClient(path=chroma_path)
        _collection = client.get_or_create_collection("dark_mode_knowledge")

        existing = _collection.count()
        if existing == 0:
            _collection.add(
                documents=[d["text"] for d in DOMAIN_DOCUMENTS],
                ids=[d["id"] for d in DOMAIN_DOCUMENTS]
            )
            logging.info(f"[ChromaDB] Seeded {len(DOMAIN_DOCUMENTS)} domain documents")
        else:
            logging.info(f"[ChromaDB] Collection already has {existing} documents")

    except ImportError:
        logging.warning("[ChromaDB] chromadb not installed — run: pip install chromadb")
    except Exception as e:
        logging.warning(f"[ChromaDB] Init failed: {e}")


def query_chroma(query_text: str, n_results: int = 3):
    global _collection
    if _collection is None:
        return []
    try:
        results = _collection.query(query_texts=[query_text], n_results=n_results)
        return results.get("documents", [[]])[0]
    except Exception as e:
        logging.warning(f"[ChromaDB] Query failed: {e}")
        return []
