# ===================== app/model.py ===========================
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from .config import MODEL_PATH, DEFAULT_LOOKBACK
import pandas as pd

_scaler: MinMaxScaler | None = None
_model = None


def _ensure_model():
    global _model
    if _model is None:
        _model = load_model(MODEL_PATH)


def _ensure_scaler(df: pd.DataFrame):
    global _scaler
    if _scaler is None:
        _scaler = MinMaxScaler(feature_range=(0, 1))
        _scaler.fit(df[['Close']])


def predict_next_close(df: pd.DataFrame) -> float:
    """Predict the next day close given historic dataframe (expects 'Close')."""
    _ensure_model()
    _ensure_scaler(df)

    scaled = _scaler.transform(df[['Close']])
    lookback = DEFAULT_LOOKBACK
    if len(scaled) < lookback:
        raise ValueError("Not enough data for prediction")

    last = scaled[-lookback:]
    sample = np.reshape(last, (1, lookback, 1))
    pred_scaled = _model.predict(sample, verbose=0)
    pred = _scaler.inverse_transform(pred_scaled)
    return float(pred[0][0])


