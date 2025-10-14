import os
import chromadb
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader

# === 1. Load environment variables ===
load_dotenv()

CHROMA_API_KEY = os.getenv("CHROMA_CLOUD_API_KEY")
CHROMA_TENANT = os.getenv("CHROMA_CLOUD_TENANT")

CHROMA_DB = "Mahabharath"
CHROMA_COLLECTION = "Mahabharath"

if not CHROMA_API_KEY or not CHROMA_TENANT:
    raise EnvironmentError("❌ Missing ChromaDB API key or Tenant ID.")

# === 2. Connect to ChromaDB Cloud ===
client = chromadb.CloudClient(
    api_key=CHROMA_API_KEY,
    tenant=CHROMA_TENANT,
    database=CHROMA_DB
)

# === 3. Extract text from PDF ===
def load_pdf_text(path: str) -> str:
    """Extracts all textual content from a PDF (ignores images)."""
    try:
        reader = PdfReader(path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text()
            if text:
                pages.append(text.strip())
            else:
                print(f"⚠️ Skipped page {i + 1} (no extractable text)")
        return "\n".join(pages)
    except Exception as e:
        print(f"❌ Error reading PDF file: {e}")
        return ""

# === 4. Load and verify content ===
pdf_path = "./The Complete Mahabharata .pdf"  # Ensure correct name and path
pdf_text = load_pdf_text(pdf_path)

print(f"📝 Extracted {len(pdf_text)} characters from PDF.")
if not pdf_text.strip():
    raise ValueError("❌ No text extracted from PDF! Check file integrity or encoding.")

# === 5. Split text into chunks ===
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.create_documents([pdf_text])

documents = [doc.page_content for doc in chunks]
metadatas = [{"source": "Mahabharath_pdf"} for _ in documents]
ids = [f"Mahabharath_pdf_{i}" for i in range(len(documents))]

print(f"🧩 Number of chunks: {len(documents)}")
if documents:
    print(f"🔍 Sample from first chunk:\n{documents[0][:400]}\n---")

# === 6. Upload chunks to ChromaDB ===
collection = client.get_or_create_collection(name=CHROMA_COLLECTION)
batch_size = 100
total_uploaded = 0

for i in range(0, len(documents), batch_size):
    try:
        collection.add(
            documents=documents[i:i + batch_size],
            metadatas=metadatas[i:i + batch_size],
            ids=ids[i:i + batch_size]
        )
        print(f"✅ Uploaded batch {i // batch_size + 1} ({i + 1}-{min(i + batch_size, len(documents))})")
        total_uploaded += len(documents[i:i + batch_size])
    except Exception as e:
        print(f"❌ Error in batch {i // batch_size + 1}: {e}")

print(f"\n🎯 Upload complete — {total_uploaded} text chunks added to ChromaDB collection '{CHROMA_COLLECTION}'.")
