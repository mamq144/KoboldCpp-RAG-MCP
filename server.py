import os
import glob
from pathlib import Path
from typing import Any
import pandas as pd
from pypdf import PdfReader
import docx
import chromadb
from chromadb.utils import embedding_functions
from mcp.server.mcpserver import MCPServer

# 1. إعداد المسارات وقاعدة البيانات المحلية
BASE_DIR = Path(__file__).resolve().parent
DOCS_DIR = BASE_DIR / "documents"
DB_DIR = BASE_DIR / "data_db"

DOCS_DIR.mkdir(exist_ok=True)
DB_DIR.mkdir(exist_ok=True)

# استخدام نموذج تضمين محلي
emb_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = chromadb.PersistentClient(path=str(DB_DIR))
collection = client.get_or_create_collection(
    name="kobold_knowledge_base",
    embedding_function=emb_fn
)

# 2. إنشاء سيرفر MCP
mcp = MCPServer("KoboldCpp-RAG-Server")

def extract_text_from_file(file_path: Path) -> str:
    """استخراج النصوص من مختلف صيغ الملفات (PDF, Word, Excel, CSV, TXT, MD)"""
    suffix = file_path.suffix.lower()
    text = ""
    try:
        if suffix in [".txt", ".md"]:
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                text = f.read()

        elif suffix == ".pdf":
            reader = PdfReader(str(file_path))
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"

        elif suffix == ".docx":
            doc = docx.Document(str(file_path))
            full_text = [para.text for para in doc.paragraphs if para.text]
            text = "\n".join(full_text)

        elif suffix in [".xlsx", ".xls"]:
            excel_data = pd.read_excel(str(file_path), sheet_name=None)
            for sheet_name, df in excel_data.items():
                text += f"\n--- ورقة العمل: {sheet_name} ---\n"
                text += df.to_string(index=False) + "\n"

        elif suffix == ".csv":
            df = pd.read_csv(str(file_path))
            text = df.to_string(index=False)

    except Exception as e:
        print(f"خطأ أثناء قراءة الملف {file_path.name}: {e}")
        return ""

    return text.strip()

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    """تجزئة النصوص إلى فقرات متداخلة للحفاظ على الترابط الدلالي"""
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk = " ".join(tokens[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks

@mcp.tool()
def index_documents() -> str:
    """مسح مجلد documents وقراءة كافة المستندات بمختلف صيغها وفهرستها دلالياً"""
    supported_patterns = ["*.txt", "*.md", "*.pdf", "*.docx", "*.xlsx", "*.xls", "*.csv"]
    files = []
    for pattern in supported_patterns:
        files.extend(DOCS_DIR.glob(pattern))

    if not files:
        return "لم يتم العثور على أي مستندات مدعومة داخل مجلد documents."

    total_chunks = 0
    indexed_files_count = 0

    for file_path in files:
        content = extract_text_from_file(file_path)
        if not content:
            continue

        chunks = chunk_text(content)
        if not chunks:
            continue

        ids = [f"{file_path.stem}_{idx}" for idx in range(len(chunks))]
        metadatas = [{"source": file_path.name, "chunk_id": idx} for idx in range(len(chunks))]

        collection.upsert(
            documents=chunks,
            ids=ids,
            metadatas=metadatas
        )
        total_chunks += len(chunks)
        indexed_files_count += 1

    return f"تمت الفهرسة بنجاح! تمت معالجة {indexed_files_count} ملف وإضافة {total_chunks} مقطع دلالي إلى قاعدة البيانات."

@mcp.tool()
def query_knowledge_base(query: str, top_k: int = 3) -> str:
    """البحث الدلالي في قاعدة البيانات واسترجاع أهم المقاطع المطابقة للاستعلام"""
    if collection.count() == 0:
        return "قاعدة البيانات فارغة حالياً. يرجى إضافة ملفات في مجلد documents واستدعاء index_documents أولاً."

    results = collection.query(
        query_texts=[query],
        n_results=min(top_k, collection.count())
    )

    retrieved_texts = []
    if results and "documents" in results and results["documents"]:
        for idx, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][idx] if "metadatas" in results and results["metadatas"] else {}
            src = meta.get("source", "Unknown")
            retrieved_texts.append(f"--- [المصدر: {src}] ---\n{doc}")

    if not retrieved_texts:
        return "لم يتم العثور على معلومات مطابقة في قاعدة البيانات."

    return "\n\n".join(retrieved_texts)

if __name__ == "__main__":
    mcp.run(transport="stdio")