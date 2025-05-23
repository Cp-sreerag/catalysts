# ===================== app/config.py ==========================
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / ".." / "models" / "stock_models.keras"  # adjust if different
CACHE_PATH = BASE_DIR / ".." / "cache"
CACHE_PATH.mkdir(exist_ok=True)
DEFAULT_LOOKBACK = 60
