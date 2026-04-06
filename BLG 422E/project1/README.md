# Project #1: Robust Client–Server Communication and JSON Processing

This repository contains the solution for **Project #1 (BLG 422E)**. The goal of this project is to develop a robust Python client that communicates with a remote server, submits data in JSON format, and gracefully handles network constraints and error cases.

## Features

- **Data Serialization**: Reads personal info from `original.json` and submits it via a multipart POST request.
- **Robust Retry Mechanism**: Automatically retries indefinitely upon network failure or server unavailability (e.g., when the server is restricted outside of 09:00–18:00).
- **Graceful Interruption**: Captures `KeyboardInterrupt` to auto-generate a fallback `modified_unavailable.json` report containing the original data and unavailability notes.
- **Difference Analysis**: Programmatically compares the server's response (`modified.json`) against `original.json`, categorizing fields as **ADDED**, **MODIFIED**, **UNCHANGED**, or **REMOVED**.
- **Structured Logging**: Outputs timestamped events (including all HTTP requests, error codes, and the final JSON comparison report) to standard output and dedicated log files.

## Project Structure

- `client.py` – The main Python client application. No external dependencies besides `requests`.
- `original.json` – The original JSON file containing submitted personal information.
- `modified.json` – The server's modified JSON response (generated during available hours).
- `modified_unavailable.json` – A client-generated JSON file documenting server unavailability.
- `client_available.log` – A sample log demonstrating a successful server interaction.
- `client_unavailable.log` – A sample log demonstrating multiple retries and eventual graceful exit during server downtime.
- `project_report.docx` – A detailed report analyzing the scenarios and mechanisms.

## Usage

The application requires Python 3 and the `requests` library.

```bash
pip install requests
```

The script supports a `--mode` flag to separate logs between server availability scenarios:

```bash
# Run in available mode (default)
# Logs to client_available.log and saves modified.json
python client.py --mode available

# Run in unavailable mode
# Logs to client_unavailable.log and saves modified_unavailable.json on interrupt
python client.py --mode unavailable
```
