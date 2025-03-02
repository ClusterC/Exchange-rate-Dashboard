import yfinance as yf
import streamlit as st

# รายชื่อสกุลเงินที่ต้องการดึงข้อมูล
currencies = {
    "EUR/THB": "EURTHB=X",
    "JPY/THB": "JPYTHB=X",
    "GBP/THB": "GBPTHB=X",
    "CNY/THB": "CNYTHB=X",
    "USD/THB": "USDTHB=X"
}

# ดึงข้อมูลราคาล่าสุด
exchange_rates = {}

for currency, ticker in currencies.items():
    data = yf.Ticker(ticker)
    hist = data.history(period="1d")  # ดึงข้อมูลย้อนหลัง 1 วัน
    
    if not hist.empty:
        exchange_rates[currency] = f"{hist['Close'].iloc[-1]:.2f}"  # จัดรูปแบบทศนิยม 2 ตำแหน่ง
    else:
        exchange_rates[currency] = "N/A"

print(exchange_rates)