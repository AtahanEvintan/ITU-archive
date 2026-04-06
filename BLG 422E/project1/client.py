"""
client.py — Robust Client–Server Communication and JSON Processing
Project #1

This client:
  1. Reads original.json
  2. POSTs the data to the server with automatic retry on failure
  3. Saves the server's response as modified.json
  4. Compares original vs modified JSON (added / modified / unchanged / removed fields)
  5. Logs every event with timestamps to client_available.log or client_unavailable.log

Usage:
  python client.py --mode available       # logs to client_available.log, saves modified.json
  python client.py --mode unavailable     # logs to client_unavailable.log, saves modified_unavailable.json
  python client.py                        # defaults to 'available' mode
"""

import argparse
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path

import requests

# ─── Configuration ────────────────────────────────────────────────────────────
SERVER_URL      = "https://student-server-production-528a.up.railway.app/submit-file"
ORIGINAL_FILE   = "original.json"
RETRY_DELAY     = 30          # seconds between retries
REQUEST_TIMEOUT = 30          # seconds before a request times out
MAX_RETRIES     = None        # None = retry indefinitely until success


def setup_logging(log_file: str) -> logging.Logger:
    """Configure logging to write to the given log file and stdout."""
    logger = logging.getLogger("client")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(log_file, mode="w")
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)

    return logger


# ─── File helpers ─────────────────────────────────────────────────────────────

def read_json(filepath: str, logger: logging.Logger) -> dict:
    """Read and return a JSON file as a Python dict."""
    path = Path(filepath)
    if not path.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        logger.info(f"Successfully read: {filepath}")
        return data
    except json.JSONDecodeError as exc:
        logger.error(f"JSON parse error in {filepath}: {exc}")
        raise


def save_json(filepath: str, data: dict, logger: logging.Logger) -> None:
    """Serialise *data* as pretty-printed JSON and write to *filepath*."""
    try:
        with open(filepath, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2, ensure_ascii=False)
        logger.info(f"Successfully saved: {filepath}")
    except OSError as exc:
        logger.error(f"Could not write {filepath}: {exc}")
        raise


# ─── Server communication ─────────────────────────────────────────────────────

def send_with_retry(data: dict, logger: logging.Logger) -> dict:
    """
    POST *data* to SERVER_URL, retrying indefinitely (or up to MAX_RETRIES)
    on any failure.  Returns the parsed response dict on success.
    """
    attempt = 0

    while True:
        attempt += 1
        logger.info(f"Attempt #{attempt} — POST {SERVER_URL}")

        try:
            json_bytes = json.dumps(data, indent=2).encode("utf-8")
            response = requests.post(
                SERVER_URL,
                files={"file": ("original.json", json_bytes, "application/json")},
                timeout=REQUEST_TIMEOUT,
            )

            logger.info(f"HTTP status: {response.status_code}")

            if response.status_code == 200:
                # Try to parse the response body as JSON
                try:
                    resp_data = response.json()
                    logger.info("Server responded successfully — response parsed as JSON.")
                    return resp_data
                except json.JSONDecodeError as exc:
                    logger.error(f"Server response is not valid JSON: {exc}")
                    logger.error(f"Raw response (first 300 chars): {response.text[:300]}")

            elif response.status_code in (403, 503):
                logger.warning(
                    f"Server rejected request (HTTP {response.status_code}). "
                    "Server may be outside allowed hours (09:00–18:00)."
                )
            else:
                logger.error(
                    f"Unexpected HTTP {response.status_code}: "
                    f"{response.text[:300]}"
                )

        except requests.exceptions.ConnectionError as exc:
            logger.error(f"Connection error: {exc}")
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {REQUEST_TIMEOUT}s.")
        except requests.exceptions.RequestException as exc:
            logger.error(f"Request exception: {exc}")

        # ── Check MAX_RETRIES ──────────────────────────────────────────────
        if MAX_RETRIES is not None and attempt >= MAX_RETRIES:
            logger.critical(
                f"Reached maximum retries ({MAX_RETRIES}). Giving up."
            )
            raise RuntimeError("Maximum retries exceeded.")

        logger.info(f"Retrying in {RETRY_DELAY} seconds …")
        time.sleep(RETRY_DELAY)


# ─── JSON comparison ──────────────────────────────────────────────────────────

def compare_json(original: dict, modified: dict, logger: logging.Logger) -> dict:
    """
    Compare *original* and *modified* dicts.

    Returns a report dict with four lists:
      added     — keys present in modified but not in original
      modified  — keys present in both but with different values
      unchanged — keys present in both with the same value
      removed   — keys present in original but not in modified
    """
    logger.info("─" * 50)
    logger.info("JSON COMPARISON REPORT")
    logger.info("─" * 50)

    added, changed, unchanged, removed = [], [], [], []

    for key, val in modified.items():
        if key not in original:
            added.append(key)
            logger.info(f"  [ADDED]     '{key}': {val!r}")
        elif original[key] != val:
            changed.append(key)
            logger.info(f"  [MODIFIED]  '{key}':  {original[key]!r}  →  {val!r}")
        else:
            unchanged.append(key)
            logger.info(f"  [UNCHANGED] '{key}': {val!r}")

    for key in original:
        if key not in modified:
            removed.append(key)
            logger.info(f"  [REMOVED]   '{key}': {original[key]!r}")

    logger.info("─" * 50)
    logger.info(
        f"Summary — Added: {len(added)}  |  Modified: {len(changed)}  |  "
        f"Unchanged: {len(unchanged)}  |  Removed: {len(removed)}"
    )
    logger.info("─" * 50)

    return {
        "added": added,
        "modified": changed,
        "unchanged": unchanged,
        "removed": removed,
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Robust client for server communication and JSON processing."
    )
    parser.add_argument(
        "--mode",
        choices=["available", "unavailable"],
        default="available",
        help=(
            "Run mode. 'available' logs to client_available.log and saves "
            "modified.json. 'unavailable' logs to client_unavailable.log and "
            "saves modified_unavailable.json. Default: available."
        ),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # ── Determine file names based on mode ─────────────────────────────────
    if args.mode == "unavailable":
        log_file = "client_unavailable.log"
        modified_file = "modified_unavailable.json"
    else:
        log_file = "client_available.log"
        modified_file = "modified.json"

    logger = setup_logging(log_file)

    logger.info("=" * 60)
    logger.info("CLIENT APPLICATION STARTED")
    logger.info(f"Timestamp : {datetime.now().isoformat()}")
    logger.info(f"Server URL: {SERVER_URL}")
    logger.info(f"Mode      : {args.mode}")
    logger.info(f"Log file  : {log_file}")
    logger.info("=" * 60)

    # ── Step 1: Read original JSON ─────────────────────────────────────────
    try:
        original_data = read_json(ORIGINAL_FILE, logger)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        logger.critical(f"Cannot continue without {ORIGINAL_FILE}: {exc}")
        sys.exit(1)

    # ── Step 2: Send to server with retry ─────────────────────────────────
    logger.info("Initiating server communication with automatic retry…")
    try:
        modified_data = send_with_retry(original_data, logger)
    except (RuntimeError, KeyboardInterrupt) as exc:
        logger.warning(f"Server communication ended: {exc}")
        logger.warning(f"{modified_file} will be created with unavailability notice.")

        # ── Create modified JSON indicating server was unavailable ──────
        unavailable_data = {
            "original_data": original_data,
            "server_status": "unavailable",
            "note": (
                "The server was unavailable during this run. "
                "The client retried automatically but was interrupted "
                "before a successful response was received."
            ),
            "timestamp": datetime.now().isoformat(),
        }
        save_json(modified_file, unavailable_data, logger)

        # ── Still run comparison against the unavailable response ───────
        compare_json(original_data, unavailable_data, logger)

        logger.info("=" * 60)
        logger.info("CLIENT APPLICATION ENDED WITHOUT SUCCESSFUL SERVER RESPONSE")
        logger.info(f"Timestamp : {datetime.now().isoformat()}")
        logger.info("=" * 60)
        sys.exit(1)

    # ── Step 3: Save modified JSON ─────────────────────────────────────────
    save_json(modified_file, modified_data, logger)

    # ── Step 4: Compare original and modified ─────────────────────────────
    compare_json(original_data, modified_data, logger)

    logger.info("=" * 60)
    logger.info("CLIENT APPLICATION COMPLETED SUCCESSFULLY")
    logger.info(f"Timestamp : {datetime.now().isoformat()}")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
