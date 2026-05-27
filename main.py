import os
from ocr_extractor import run_ocr_pipeline
from llm_parser import parse_text_with_llm, ExtractedFile
from db_writer import initialize_database, save_to_database

INPUT_DIR = "inputs"

def setup_environment():
    os.makedirs(INPUT_DIR, exist_ok=True)
    initialize_database()

def validate_business_rules(doc: ExtractedFile) -> bool:
    if not doc:
        print("[!] Validation failed: Document object is None.")
        return False
    if not doc.name or doc.name.strip() == "":
        print("[!] Validation failed: 'name' field is empty.")
        return False
    if not doc.email or "@" not in doc.email:
        print(f"[!] Validation failed: Invalid email format for user '{doc.name}'.")
        return False
    return True

def process_single_file(file_path: str):
    print(f"\n[>>>] Processing pipeline for: {file_path}")
    
    raw_text = run_ocr_pipeline(file_path)
    if not raw_text:
        return

    structured_data = parse_text_with_llm(raw_text)
    if not structured_data:
        return

    if not validate_business_rules(structured_data):
        return

    save_to_database(structured_data)

if __name__ == "__main__":
    setup_environment()
    
    files = [f for f in os.listdir(INPUT_DIR) if f.endswith('.png')]
    
    if not files:
        print(f"[*] The '{INPUT_DIR}/' directory is empty. Add .png files to process.")
    else:
        for filename in sorted(files):
            file_path = os.path.join(INPUT_DIR, filename)
            process_single_file(file_path)
