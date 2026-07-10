# 🚀 Core Data Ingestion Engine (Milestone 1)

**A production-ready, containerized Python ETL pipeline that securely extracts, paginates, and flattens REST API data using Docker bind mounts for persistent local storage.**

## 📌 Project Overview
This project represents the completion of Phase 1 (Local Plumbing) of my Data Engineering architecture roadmap. The pipeline is designed to handle common data extraction hurdles such as API pagination, nested JSON flattening, and environment parity.

By containerizing the script using Docker and executing it with Volume Bind Mounts, the pipeline safely extracts web data in an isolated environment and persists the cleaned output directly to the local host machine without exposing sensitive `.env` API credentials.

## 🛠️ Technology Stack
* **Language:** Python 3.9
* **Containerization:** Docker Engine
* **Libraries:** `requests` (API querying), `python-dotenv` (Secret management), `logging` (Production tracking)
* **Data Format:** JSON

## ⚙️ Core Pipeline Architecture
1. **Secure Configuration:** Loads target API endpoints and pagination limits dynamically from a hidden `.env` file.
2. **Paginated Extraction:** Executes a `while` loop with error handling and exponential backoff to fetch multi-page API payloads safely.
3. **Data Normalization:** Flattens deeply nested transactional JSON arrays into clean, uniform rows using Python dictionary comprehensions.
4. **Isolated Execution:** Runs entirely inside a lightweight Python Docker container to guarantee identical execution across any operating system.
5. **Persistent Storage:** Uses Docker `-v` bind mounts to route the extracted files from the ephemeral container directly into a local `output/` directory.
