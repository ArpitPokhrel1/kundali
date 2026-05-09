"""Vercel serverless entry — exposes the Flask app as `app`."""
import os, sys

# Add the repo root (web/) to sys.path so `app` and `astro_nepali` resolve
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from app import app  # noqa: F401  (Vercel uses `app` as the WSGI handle)
