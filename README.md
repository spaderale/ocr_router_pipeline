# OCR Router Pipeline 🏛️

A complete image processing system that integrates OCR, LLM, and database persistence for structured document extraction.

## Architecture Overview: The Data Pipeline

Equivalent to a UNIX pipe workflow: **Image → OCR → LLM → Validation → Database**

Instead of passing raw bytes through anonymous pipes, we use Python to pass structured objects in-memory RAM between isolated modules.

### Module 1: System Isolation
- **Virtual Environment (.venv)**: Isolated environment where pip installs packages exclusively for this project
- Prevents pollution of the base operating system

### Module 2: OCR Extractor
- **Pillow**: Loads images into memory buffer
- **pytesseract**: Wrapper for the Tesseract C++ OCR engine
- Exception handling: `UnidentifiedImageError`, executable failures
- Validates file existence and image format before processing

### Module 3: Semantic Parser (LLM)
- **OpenAI API**: Reads raw OCR text and extracts structured information
- **Pydantic**: Enforces deterministic data structure with runtime type validation
- Uses `gpt-4o-mini` model for cost-effective parsing
- Handles authentication, timeout, and connection errors gracefully

### Module 4: Data Persistence
- **SQLite3**: In-process relational database
- **Parameterized Queries**: Protection against SQL injection
- Automatic schema initialization with `CREATE TABLE IF NOT EXISTS`

## Project Structure

```
ocr_router_pipeline/
├── .venv/                    # Virtual Environment
├── inputs/                   
│   ├── sample1.png           # Images to process
│   ├── sample2.png
│   └── ...
├── ocr_extractor.py          # OCR extraction module
├── llm_parser.py             # LLM parsing + Pydantic schemas
├── db_writer.py              # SQLite persistence module
├── main.py                   # Pipeline orchestrator
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Initial Setup

```bash
# Clone the repository
git clone https://github.com/spaderale/ocr_router_pipeline.git
cd ocr_router_pipeline

# Create and activate Virtual Environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
```

## Running the Pipeline

```bash
python main.py
```

The pipeline will:
1. Scan the `inputs/` directory for `.png` files
2. Extract text from each image using Tesseract OCR
3. Parse extracted text with GPT-4o-mini to structure data
4. Validate extracted data against business rules (email format, required fields)
5. Save validated records to the SQLite database

## Pipeline Flow

```
Image File (.png)
    ↓
[ocr_extractor.py]  → Raw text extraction via Tesseract
    ↓
[llm_parser.py]     → Structured parsing via OpenAI API
    ↓
[main.py]           → Business rules validation
    ↓
[db_writer.py]      → Persistence to SQLite
    ↓
social_router.db    → Local database file
```

## Extracted Data Schema

The pipeline extracts documents with the following fields:

```python
class ExtractedFile:
    id_number: int | None
    name: str
    doc_number: str
    email: str
    location: str
    area: str
    company: str
```

### Database Table Structure

```sql
CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_number INTEGER,
    name TEXT,
    doc_number TEXT,
    email TEXT,
    location TEXT,
    area TEXT,
    company TEXT
)
```

## Dependencies

- **Pillow** (10.1.0): Image processing and loading
- **pytesseract** (0.3.10): OCR text extraction
- **openai** (1.3.0): LLM API client
- **pydantic** (2.5.0): Data validation and schema definition
- **python-dotenv** (1.0.0): Environment variable management
- **requests** (2.31.0): HTTP client library

## Error Handling

The pipeline implements graceful error handling at each stage:

### OCR Module
- File existence validation
- Image format validation (`UnidentifiedImageError`)
- Tesseract engine errors
- Generic exception catching

### LLM Module
- OpenAI authentication errors
- Network timeouts and connection errors
- Invalid response parsing

### Database Module
- Connection errors
- Schema initialization failures
- Data integrity errors

### Main Orchestrator
- Validation of document object existence
- Required field validation (non-empty name)
- Email format validation (`@` symbol presence)

## Key Design Patterns

1. **Pipeline Architecture**: Each module is independent and testable
2. **Type Safety**: Pydantic models enforce schema compliance
3. **Error Resilience**: Validation at multiple stages prevents invalid data persistence
4. **Resource Management**: Context managers ensure proper database connection cleanup
5. **Environment Isolation**: Virtual environment prevents dependency conflicts

## Design Philosophy

This project demonstrates high-level Python abstractions without losing visibility into what happens in RAM and on disk—a practical transition from C-level systems programming to productive Python development. 🚀

## Notes

- Ensure Tesseract OCR engine is installed on your system before running
- Store your OpenAI API key in environment variables (never hardcode)
- The database (`social_router.db`) is created automatically on first run
- PNG images in the `inputs/` directory are processed in alphabetical order
