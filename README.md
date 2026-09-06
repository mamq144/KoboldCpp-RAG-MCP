\# KoboldCpp RAG MCP Server | خادم استرجاع المعرفة لـ KoboldCpp عبر بروتوكول MCP



An enterprise-grade, privacy-first Retrieval-Augmented Generation (RAG) server designed specifically for KoboldCpp. It leverages the Model Context Protocol (MCP) and ChromaDB to grant local Large Language Models direct semantic access to private documents with zero data leaks.



خادم استرجاع معرفة وتوليد معزز (RAG) عالي الأداء ومحلي بالكامل، مصمم لربط نماذج الذكاء الاصطناعي داخل KoboldCpp بمستنداتك وملفاتك الخاصة عبر بروتوكول MCP وقاعدة ChromaDB المتجهة بأمان وخصوصية تامة 100%.



\---



\## Key Highlights | أبرز المزايا التقنية



\- Multi-Format Ingestion: Full text and tabular parsing for PDF, DOCX, XLSX, XLS, CSV, TXT, and Markdown files.

&#x20; (دعم شامل لمختلف الصيغ: قراءة واستخراج النصوص والجداول من ملفات الـ PDF، الوورد، الإكسل، ملفات القيم المفصولة بفواصل، والنصوص الخام).

\- Local Embedding Engine: Employs sentence-transformers/all-MiniLM-L6-v2 locally via Hugging Face and ONNX runtimes.

&#x20; (معالجة متجهات محلية سريعة بالاعتماد على نموذج التضمين القياسي دون الحاجة لطلب واجهات سحابية).

\- Persistent Vector Storage: Powered by ChromaDB with persistent disk serialization in a dedicated vector space.

&#x20; (تخزين متجهي دائم ومفهرس دلالياً يضمن حفظ المقاطع وقراءتها فورياً من القرص الصلب).

\- Autonomous Tool Calling: Directly integrated into KoboldCpp's tool system, allowing models to index files or query context autonomously during conversations.

&#x20; (استدعاء ذاتي للأدوات: يستطيع النموذج استكشاف قاعدة المعرفة وفهرسة الملفات الجديدة استجابة لطلب المستخدم داخل المحادثة).

\- Zero Data Leakage: All processing, chunking, embedding, and vector querying are confined to the host machine.

&#x20; (أمان مطلق وخصوصية كاملة: لا يتم إرسال أي ملف أو متجه إلى الإنترنت).



\---



\## Architecture \& MCP Tools | بنية السيرفر والأدوات المتاحة



The server implements two primary MCP functions executed via standard I/O (stdio):



1\. index\_documents:

&#x20;  - Scans the documents/ directory.

&#x20;  - Cleans and extracts text depending on file extensions.

&#x20;  - Chunks text into 500-token windows with 50-token overlap to maintain coherence.

&#x20;  - Generates vector embeddings and upserts data into data\_db/.

&#x20;  - (مسح مجلد المستندات، استخراج المحتوى، تقسيمه إلى مقاطع متداخلة لضمان الترابط الدلالي، ثم تحديث قاعدة المتجهات).



2\. query\_knowledge\_base:

&#x20;  - Takes a search query string and a top\_k retrieval parameter.

&#x20;  - Computes query embeddings and executes semantic similarity searches.

&#x20;  - Returns matched chunks enriched with source document metadata.

&#x20;  - (استقبال استفسارات المستخدم، مطابقتها دلالياً مع المقاطع المخزنة، وإرجاع أدق الفقرات مع الإشارة لاسم المصدر).



\---



\## Directory Structure | هيكلية المشروع



RAG\_KoboldCpp/

│

├── documents/            # Drop your PDFs, Word, and Excel files here

├── data\_db/              # Persistent ChromaDB vector storage (Git-ignored)

├── server.py             # Core MCP RAG server implementation

├── test\_rag.py           # Standalone verification and indexing utility

├── run\_mcp.bat           # Automated environment launcher for KoboldCpp

├── mcp\_config.json       # MCP client configuration schema for KoboldCpp

├── requirements.txt      # Pinned dependency manifest

└── .gitignore            # Security exclusions (guards data\_db and private files)



\---



\## Installation \& Setup | خطوات التثبيت والتشغيل



1\. Clone the Repository | استنساخ المستودع:

&#x20;  git clone https://github.com/mamq144/KoboldCpp-RAG-MCP.git

&#x20;  cd KoboldCpp-RAG-MCP



2\. Prepare Virtual Environment | إعداد البيئة الافتراضية:

&#x20;  python -m venv venv

&#x20;  venv\\Scripts\\activate



3\. Install Dependencies | تثبيت المكتبات:

&#x20;  pip install -r requirements.txt



4\. Index Your Knowledge Base | إضافة المستندات وفهرستها:

&#x20;  - Place any documents (.pdf, .docx, .xlsx, .txt, etc.) inside the documents folder.

&#x20;  - Run the manual indexing check:

&#x20;    python test\_rag.py



\---



\## KoboldCpp Integration | الربط مع KoboldCpp



Option A: Via Command Line (CLI)

Run your KoboldCpp instance with the --mcp flag pointing directly to your JSON configuration:

koboldcpp.exe --model your\_model.gguf --gpulayers -1 --mcp "E:\\RAG\_KoboldCpp\\mcp\_config.json"



Option B: Via Web GUI (Settings)

1\. Launch KoboldCpp and open http://localhost:5001.

2\. Navigate to Settings -> Tools -> MCP Tool Calling.

3\. Ensure "Enable Toolcalling" and "Automatically Execute Tools" are checked.

4\. Verify that "index\_documents" and "query\_knowledge\_base" are listed and enabled.



\---



\## License | الترخيص



Distributed under the MIT License. See LICENSE for more information.

مرخص تحت مظلة رخصة MIT المفتوحة.

