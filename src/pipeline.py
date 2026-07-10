import os
import json
import logging
import requests
import time
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_env_configurations():
    """Extract environment variables safely from memory storage with container directory mapping."""
    load_dotenv()
    
    raw_output_filename = os.getenv("DATA_OUTPUT_PATH", "raw_transactions.json")
    container_secure_path = f"/app/data/{raw_output_filename}"
    
    return {
        "url": os.getenv("API_TARGET_URL"),
        "max_pages": int(os.getenv("MAX_PAGE_TO_FETCH", 4)),
        "page_size": int(os.getenv("RECORDS_PER_PAGE", 5)),
        "output_file": container_secure_path
    }

def clean_and_normalize_posts(post):
    """Normalize and map raw API transaction items into flat analytical reporting rows."""
    return {
        "transaction_id": post.get("id"),
        "associated_user_id": post.get("userId"),
        "content_title": post.get("title", "").strip().upper(),
        "extracted_time": int(time.time())
    }

def execute_paginated_pipeline():
    """Loops through API pages, normalizes structural items, and saves data persistently."""
    logging.info("Initiating Production Pagination Ingestion Engine...")
    configs = load_env_configurations()

    all_extracted_records = []
    current_page = 1

    while current_page <= configs["max_pages"]:
        logging.info(f"Extracting data from page: {current_page} | Records per page limit: {configs['page_size']}")

        query_params = {
            "_page": current_page,
            "_limit": configs["page_size"]
        }

        try:
            response = requests.get(configs["url"], params=query_params, timeout=10)
            response.raise_for_status()
            raw_data = response.json()
        
            if not raw_data or len(raw_data) == 0:
                logging.info("Encountered empty array payload. Terminating page loop process execution loop cleanly.")
                break
                
            logging.info(f"Successfully extracted {len(raw_data)} elements from page {current_page}.")

            for item in raw_data:
                cleaned_row = clean_and_normalize_posts(item)
                all_extracted_records.append(cleaned_row)
        
            current_page += 1
            time.sleep(0.5)

        except requests.exceptions.RequestException as connection_error:
            logging.error(f"Network connectivity dropout error encountered: {connection_error}")
            break
        except requests.exceptions.HTTPError as http_error:
            logging.error(f"HTTP Status Validation Failure: {http_error}")
            break
        
    logging.info(f"Pagination processing completed. Total rows aggregated: {len(all_extracted_records)}")

    target_directory = os.path.dirname(configs["output_file"])
    os.makedirs(target_directory, exist_ok=True)

    with open(configs["output_file"], "w") as target_file:
        json.dump(all_extracted_records, target_file, indent=2)

    logging.info(f"Data engine state synchronization complete. Core metrics dumped to: {configs['output_file']}")

if __name__ == "__main__":
    execute_paginated_pipeline()
