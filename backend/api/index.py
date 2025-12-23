"""Vercel entry point for FastAPI backend."""
import sys
from pathlib import Path

# Add parent directory to path to import modules
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from main import app

# Export the app for Vercel
handler = app
