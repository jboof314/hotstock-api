import os
from fastapi import FastAPI, Header, HTTPException, Query, Path
from typing import Optional

app = FastAPI(title="Hot Stock API", version="1.0.1")

API_KEY = os.getenv("API_KEY")  # set this on Render later

DEMO_TOP10 = [
    {"ticker": "NVDA", "mentions": 47, "bullish": "AI/datacenter demand strong.", "bearish": "Rich valuation; China exposure."},
    {"ticker": "TSLA", "mentions": 39, "bullish": "Delivery momentum; software margins.", "bearish": "Price cuts; competition."},
    {"ticker": "AAPL", "mentions": 31, "bullish": "Services growth; ecosystem lock-in.", "bearish": "Hardware maturity; regulation."},
    {"ticker": "MSFT", "mentions": 29, "bullish": "Cloud + AI monetization.", "bearish": "Capex intensity; antitrust risk."},
    {"ticker": "AMZN", "mentions": 27, "bullish": "Retail efficiency; AWS reacceleration.", "bearish": "Margin variability; ad cyclicality."},
    {"ticker": "META", "mentions": 24, "bullish": "Ad recovery; Reels monetization.", "bearish": "AI spend; regulatory scrutiny."},
    {"ticker": "GOOGL", "mentions": 22, "bullish": "Search durability; Cloud margin lift.", "bearish": "AI competitive risk; antitrust."},
    {"ticker": "AMD", "mentions": 20, "bullish": "AI GPU ramp; share gains.", "bearish": "Supply constraints; competition."},
    {"ticker": "AVGO", "mentions": 18, "bullish": "AI networking; VMware synergies.", "bearish": "Integration risk; cycle turns."},
    {"ticker": "JPM", "mentions": 16, "bullish": "NII strength; scale advantages.", "bearish": "Credit normalization; regulation."},
]

def _require_key(x_api_key: Optional[str]):
    if API_KEY:
        if not x_api_key or x_api_key != API_KEY:
            raise HTTPException(status_code=401, detail="Unauthorized")

@app.get("/top10")
def top10(
    date: str = Query(..., description="YYYY-MM-DD"),
    x_api_key: Optional[str] = Header(default=None, alias="x-api-key"),
):
    _require_key(x_api_key)
    return DEMO_TOP10

@app.get("/ticker/{symbol}")
def ticker_summary(
    symbol: str = Path(..., description="Ticker symbol, e.g. NVDA"),
    date: str = Query(..., description="YYYY-MM-DD"),
    x_api_key: Optional[str] = Header(default=None, alias="x-api-key"),
):
    _require_key(x_api_key)
    s = symbol.upper()
    for item in DEMO_TOP10:
        if item["ticker"] == s:
            return item
    return {"error": "No data for this ticker/date"}
