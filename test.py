import yfinance as yf
import streamlit as st

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="Exchange Rate Dashboard", layout="wide")

# ใส่ CSS เพื่อเปลี่ยนฟอนต์และสีพื้นหลัง
st.markdown(
    """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Kanit:wght@400;700&display=swap');
        body, [class*="st-"] {
            background-color: #000000;
            color: white;
            font-family: 'Kanit', sans-serif;
        }
        .rate-box {
            text-align: center;
            font-size: 25px;
            font-weight: bold;
            color: white;
            background-color: #101015;
            padding: 20px;            
            width: 200px; /* กำหนดความกว้าง */
            height: 200px; /* กำหนดความสูง */
            display: flex; /* ใช้ flexbox เพื่อจัดกึ่งกลาง */
            justify-content: center; /* จัดแนวนอนกึ่งกลาง */
            align-items: center; /* จัดแนวตั้งกึ่งกลาง */
            margin: 10px auto; /* ปรับ margin */
        }
    </style>
    """,
    unsafe_allow_html=True
)

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

# จัดกล่องให้อยู่ในแนวนอน
cols = st.columns(len(currencies))

# วนลูปแสดงข้อมูลแต่ละค่า
for i, (currency, rate) in enumerate(exchange_rates.items()):
    with cols[i]:  # แสดงแต่ละค่าในคอลัมน์ของตัวเอง
        st.markdown(
            f"""    
            <div class="rate-box">
                {rate} <br>THB
            </div>
            """,
            unsafe_allow_html=True
        )