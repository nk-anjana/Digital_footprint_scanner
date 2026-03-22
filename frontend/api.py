import requests
import streamlit as st

BASE_URL = "http://localhost:8000" # Change to http://api:8000 if running inside Docker with the frontend

def get_headers():
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}

def login(username, password):
    resp = requests.post(f"{BASE_URL}/auth/login", json={"username": username, "password": password})
    return resp

def register(username, password):
    resp = requests.post(f"{BASE_URL}/auth/register", json={"username": username, "password": password})
    return resp

def get_scans():
    resp = requests.get(f"{BASE_URL}/scans", headers=get_headers())
    return resp.json().get("scans", []) if resp.status_code == 200 else []

def start_scan(payload):
    resp = requests.post(f"{BASE_URL}/scans", json=payload, headers=get_headers())
    return resp

def get_scan_result(scan_id):
    resp = requests.get(f"{BASE_URL}/scans/{scan_id}", headers=get_headers())
    return resp.json() if resp.status_code == 200 else None

def analyze_image(file_bytes, filename, mime_type):
    files = {"file": (filename, file_bytes, mime_type)}
    resp = requests.post(f"{BASE_URL}/osint/image-metadata", files=files, headers=get_headers())
    return resp