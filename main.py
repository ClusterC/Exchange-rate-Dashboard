"""
สำหรับการสร้าง Dashboard ที่เกี่ยวกับอัตราแลกเปลี่ยน คุณอาจวางโครงสร้างออกเป็น 2 ส่วนหลัก คือ **สถิติ (Statistics)** และ **กราฟ/แผนภูมิ (Charts)** โดยมีรายละเอียดดังนี้:

---

### สถิติอย่างน้อย 5 รายการ
1. **อัตราแลกเปลี่ยนปัจจุบัน**  
   แสดงอัตราแลกเปลี่ยนของสกุลเงินหลัก (เช่น USD, EUR, THB ฯลฯ) ในเวลาปัจจุบัน

2. **การเปลี่ยนแปลงรายวัน**  
   คำนวณการเปลี่ยนแปลงของอัตราแลกเปลี่ยนจากวันก่อนหน้า (ในรูปแบบเปอร์เซ็นต์หรือจำนวน)

3. **ค่าสูงสุดและต่ำสุดในช่วงเวลาที่กำหนด**  
   เช่น ภายใน 1 สัปดาห์, 1 เดือน หรือ 1 ปี เพื่อดูแนวโน้มการผันผวน

4. **ค่าเฉลี่ยของอัตราแลกเปลี่ยน**  
   คำนวณค่าเฉลี่ยในช่วงเวลาที่สนใจ เพื่อให้เห็นภาพรวมของตลาดในช่วงนั้น

5. **ความผันผวน (Volatility)**  
   เช่น ค่าส่วนเบี่ยงเบนมาตรฐานหรือความแปรปรวนของอัตราแลกเปลี่ยนในช่วงเวลาที่เลือก

---

### กราฟ/แผนภูมิอย่างน้อย 10 รายการ
1. **กราฟเส้น (Line Chart)**  
   แสดงแนวโน้มการเปลี่ยนแปลงของอัตราแลกเปลี่ยนตลอดช่วงเวลาที่เลือก

2. **กราฟแท่ง (Bar Chart)**  
   เปรียบเทียบอัตราแลกเปลี่ยนของสกุลเงินต่าง ๆ ในช่วงเวลาที่กำหนด

3. **กราฟพื้นที่ (Area Chart)**  
   ใช้เพื่อเน้นแนวโน้มและการเปลี่ยนแปลงโดยรวมของข้อมูล

4. **กราฟ Candlestick**  
   แสดงข้อมูลเชิงลึก เช่น ราคาเปิด, ปิด, สูงสุด, และต่ำสุดในแต่ละช่วงเวลา

5. **กราฟ Pie/Doughnut**  
   แสดงสัดส่วนหรือการกระจายของการเปลี่ยนแปลงในแต่ละสกุลเงิน

6. **กราฟ Scatter Plot**  
   เปรียบเทียบอัตราแลกเปลี่ยนกับตัวแปรอื่น ๆ (เช่น ปริมาณการซื้อขายหรือดัชนีเศรษฐกิจ)

7. **กราฟ Heatmap**  
   แสดงความถี่หรือระดับการเปลี่ยนแปลงของอัตราแลกเปลี่ยนในแต่ละช่วงเวลา (เช่น รายชั่วโมงหรือรายวัน)

8. **กราฟ Radar Chart**  
   ใช้สำหรับเปรียบเทียบมิติหลายด้านของการวิเคราะห์อัตราแลกเปลี่ยน (เช่น ความผันผวน, การเปลี่ยนแปลงรายวัน, ค่าเฉลี่ย)

9. **กราฟ Box Plot**  
   แสดงการกระจายและค่าผิดปกติ (outliers) ของข้อมูลอัตราแลกเปลี่ยน

10. **กราฟ Trendline หรือ Moving Average Overlay**  
    แสดงแนวโน้มที่ชัดเจนโดยการวางเส้นแนวโน้มหรือค่าเฉลี่ยเคลื่อนที่บนกราฟเส้น

---
"""

import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import date, timedelta
from streamlit_echarts import st_echarts

st.set_page_config(layout="wide", page_title="Exchange Rate Statistics", page_icon="📈")

# --- Data Fetching ---
@st.cache_data
def get_exchange_data(ticker, start_date, end_date, interval="1h"):  # Added interval parameter
    data = yf.Ticker(ticker)
    hist = data.history(start=start_date, end=end_date, interval=interval)  # Added interval to history
    return hist

# --- Currency Data ---
currencies = {
    "EUR/THB": "EURTHB=X",
    "JPY/THB": "JPYTHB=X",
    "GBP/THB": "GBPTHB=X",
    "AUD/THB": "AUDTHB=X",
    "USD/THB": "USDTHB=X"
}

# --- Sidebar ---
st.sidebar.header("Date Range Selection")
today = date.today()
start_date = st.sidebar.date_input("Start date", today - timedelta(days=7))  # Reduced default range to 7 days
end_date = st.sidebar.date_input("End date", today)

# Add interval selection
interval_options = ["1h", "1d", "1wk"]  # Reduced to 3 options
selected_interval = st.sidebar.selectbox("Select Interval", interval_options, index=0)  # Default to 1h

# Create a selectbox for choosing the currency to display (outside the columns)
selected_currency = st.sidebar.selectbox("Select Currency for Charts", list(currencies.keys()))

# Fetch data for all currencies
exchange_data = {}
for currency, ticker in currencies.items():
    exchange_data[currency] = get_exchange_data(ticker, start_date, end_date, interval=selected_interval) # Pass interval

# --- Main Content ---
st.title("📊 Exchange Rate Statistics")
st.write("Explore key statistics for major currency exchange rates.")

# --- Statistics Display ---------------------------------------------------------------------------------------------------------------------------
st.header("Exchange Rate Summary")

cols = st.columns(len(currencies), gap="small")  # Create columns dynamically based on the number of currencies

for i, (currency, data) in enumerate(exchange_data.items()):
    with cols[i]:
        st.subheader(f"{currency}")
        if not data.empty:
            latest_rate = data['Close'].iloc[-1]
            previous_rate = data['Close'].iloc[-2] if len(data) >= 2 else latest_rate
            daily_change = latest_rate - previous_rate
            daily_change_percent = (daily_change / previous_rate) * 100 if previous_rate != 0 else 0
            max_rate = data['Close'].max()
            min_rate = data['Close'].min()
            average_rate = data['Close'].mean()
            volatility = data['Close'].std()

            st.metric(label="Current Rate", value=f"{latest_rate:.2f}")

            if daily_change > -1:
                st.metric(label="Daily Change", value=f"{daily_change:.3f}", delta=f"{daily_change_percent:.3f}%", delta_color="normal")
            else:
                st.metric(label="Daily Change", value=f"{daily_change:.3f}", delta=f"{daily_change_percent:.3f}%", delta_color="inverse")

            st.write(f"**Max:** {max_rate:.2f}")
            st.write(f"**Min:** {min_rate:.2f}")
            st.write(f"**Average:** {average_rate:.2f}")
            st.write(f"**Volatility:** {volatility:.2f}")
        else:
            st.warning(f"No data available for {currency}")

# --- Charts Display ---
st.header("Exchange Rate Trends")
st.write("Visualize the trends of exchange rates over the selected period using ECharts.")

# Create columns for charts
col1, col2, col3 = st.columns(3)

# --- Line: Basic Area Chart (ECharts) ---------------------------------------------------------------------------------------------------------------------------
with col1:
    st.subheader("Basic Area Chart")

    if selected_currency in exchange_data:
        data = exchange_data[selected_currency]
        if not data.empty:
            # Prepare data for ECharts
            dates = data.index.strftime('%Y-%m-%d %H:%M').tolist() if selected_interval not in ["1d", "1wk"] else data.index.strftime('%Y-%m-%d').tolist()
            rates = data['Close'].tolist()

            # Calculate the range of y-axis
            min_rate = min(rates)
            max_rate = max(rates)
            range_y = max_rate - min_rate
            
            # Find the index of the maximum and minimum values
            max_index = rates.index(max(rates)) if rates else -1
            min_index = rates.index(min(rates)) if rates else -1

            # ECharts options for Basic Area Chart
            options = {
                "title": {"text": f"{selected_currency} Exchange Rate Trend"},
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}}},
                "xAxis": {"type": "category", "boundaryGap": False, "data": dates, "name": "Date"},
                "yAxis": {
                    "type": "value",
                    "name": "Exchange Rate",
                    "min": f"{min_rate - range_y * 0.1:.2f}", # Add min
                    "max": f"{max_rate + range_y * 0.1:.2f}", # Add max
                },
                "series": [
                    {
                        "data": rates,
                        "type": "line",
                        "smooth": False,
                        "areaStyle": {},  # Enable area fill
                    }
                ],
            }

            # Display the chart using st_echarts
            st_echarts(options=options, height="500px")
        else:
            st.warning(f"No data available for {selected_currency} to display the Basic Area Chart.")
    else:
        st.warning("Please select a currency.")

# --- Bar: Basic Bar Chart (ECharts) ---------------------------------------------------------------------------------------------------------------------------
with col2:
    st.subheader("Basic Bar Chart")

    if selected_currency in exchange_data:
        data = exchange_data[selected_currency]
        if not data.empty:
            # Prepare data for ECharts
            dates = data.index.strftime('%Y-%m-%d %H:%M').tolist() if selected_interval not in ["1d", "1wk"] else data.index.strftime('%Y-%m-%d').tolist()
            rates = data['Close'].tolist()
            
            # Find the index of the maximum and minimum values
            max_index = rates.index(max(rates)) if rates else -1
            min_index = rates.index(min(rates)) if rates else -1

            # Calculate the range of y-axis
            min_rate = min(rates)
            max_rate = max(rates)
            range_y = max_rate - min_rate

            # ECharts options for Basic Bar Chart
            options = {
                "title": {"text": f"{selected_currency} Exchange Rate Trend"},
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
                "xAxis": {"type": "category", "data": dates, "name": "Date"},
                "yAxis": {
                    "type": "value",
                    "name": "Exchange Rate",
                    "min": f"{min_rate - range_y * 0.1:.2f}",
                    "max": f"{max_rate + range_y * 0.1:.2f}",
                },
                "series": [
                    {
                        "data": rates,
                        "type": "bar",
                        "itemStyle": {
                            "color": {
                                "type": "linear",
                                "x": 0,
                                "y": 0,
                                "x2": 0,
                                "y2": 1,
                                "colorStops": [
                                    {"offset": 0, "color": "#5470c6"},  # Color at the bottom
                                    {"offset": 1, "color": "#5470c6"},  # Color at the top
                                ],
                            }
                        },
                        "markPoint": {
                            "data": [
                                {
                                    "name": "Max",
                                    "coord": [max_index, max(rates)],
                                    "itemStyle": {"color": "green"},
                                },
                                {
                                    "name": "Min",
                                    "coord": [min_index, min(rates)],
                                    "itemStyle": {"color": "red"},
                                },
                            ],
                            "symbolSize": 30,
                        },
                    }
                ],
            }
            # Display the chart using st_echarts
            st_echarts(options=options, height="500px")
        else:
            st.warning(f"No data available for {selected_currency} to display the Basic Bar Chart.")
    else:
        st.warning("Please select a currency.")

# --- Basic Candlestick Chart (ECharts) ---------------------------------------------------------------------------------------------------------------------------
with col3:
    st.subheader("Basic Candlestick Chart")

    if selected_currency in exchange_data:
        data = exchange_data[selected_currency]
        if not data.empty:
            # Prepare data for ECharts
            dates = data.index.strftime('%Y-%m-%d %H:%M').tolist() if selected_interval not in ["1d", "1wk"] else data.index.strftime('%Y-%m-%d').tolist()
            
            # Candlestick data format: [open, close, lowest, highest]
            candlestick_data = data[['Open', 'Close', 'Low', 'High']].values.tolist()

            # Calculate the range of y-axis
            all_rates = data[['Open', 'Close', 'Low', 'High']].values.flatten().tolist()
            min_rate = min(all_rates)
            max_rate = max(all_rates)
            range_y = max_rate - min_rate

            # ECharts options for Basic Candlestick Chart
            options = {
                "title": {"text": f"{selected_currency} Candlestick Chart"},
                "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross"}},
                "xAxis": {"type": "category", "data": dates, "name": "Date"},
                "yAxis": {
                    "type": "value",
                    "name": "Exchange Rate",
                    "min": f"{min_rate - range_y * 0.1:.2f}",
                    "max": f"{max_rate + range_y * 0.1:.2f}",
                },
                "series": [
                    {
                        "data": candlestick_data,
                        "type": "candlestick",
                        "itemStyle": {
                            "color": "green",
                            "color0": "red",
                            "borderColor": "green",
                            "borderColor0": "red",
                        },
                    }
                ],
            }

            # Display the chart using st_echarts
            st_echarts(options=options, height="500px")
        else:
            st.warning(f"No data available for {selected_currency} to display the Basic Candlestick Chart.")
    else:
        st.warning("Please select a currency.")

# --- Gradient Stacked Area Chart (ECharts) ---------------------------------------------------------------------------------------------------------------------------
st.subheader("Gradient Stacked Area Chart (All Currencies - Daily Change %)")

if all(not data.empty for data in exchange_data.values()):
    # Prepare data for ECharts
    dates = list(exchange_data.values())[0].index.strftime('%Y-%m-%d %H:%M').tolist() if selected_interval not in ["1d", "1wk"] else list(exchange_data.values())[0].index.strftime('%Y-%m-%d').tolist()

    series_data = []
    
    # Use the provided colors directly
    colors = ['#37A2FF', '#80FFA5', '#FFBF00', '#FF0087', '#00DDFF']
    
    for i, (currency, data) in enumerate(exchange_data.items()):
        # Calculate daily change percentage
        daily_changes = data['Close'].pct_change() * 100
        daily_changes.iloc[0] = 0  # Set the first value to 0 (no change for the first day)
        rates = daily_changes.tolist()
        
        # Get colors for the current currency
        start_color = colors[i]
        
        # Create a linear gradient with the same start and end color for a solid fill
        series_data.append({
            "name": currency,
            "type": "line",
            "smooth": True,
            "stack": "Total",
            "areaStyle": {
                "color": {
                    "type": "linear",
                    "x": 0,
                    "y": 0,
                    "x2": 0,
                    "y2": 1,
                    "colorStops": [
                        {"offset": 0, "color": start_color},
                        {"offset": 1, "color": start_color},
                    ],
                }
            },
            "lineStyle": {"width": 0},
            "showSymbol": False,
            "data": rates,
        })

    # Calculate the range of y-axis
    all_changes = []
    for data in exchange_data.values():
        daily_changes = data['Close'].pct_change() * 100
        all_changes.extend(daily_changes.tolist())
    
    # Remove NaN values
    all_changes = [x for x in all_changes if pd.notna(x)]

    if all_changes: # Check if all_changes is not empty
        min_change = min(all_changes)
        max_change = max(all_changes)
        range_y = max_change - min_change
    else:
        min_change = -1
        max_change = 1
        range_y = 2

    # ECharts options for Gradient Stacked Area Chart
    options = {
        "title": {"text": "All Currencies Gradient Stacked Area Chart (Daily Change %)"},
        "tooltip": {"trigger": "axis", "axisPointer": {"type": "cross", "label": {"backgroundColor": "#6a7985"}}},
        "xAxis": {
            "type": "category",
            "boundaryGap": False,
            "data": dates,
            "name": "Date",
        },
        "yAxis": {
            "type": "value",
            "name": "Daily Change %",
            "min": f"{min_change - range_y * 1:.2f}", # Adjusted to 10% padding
            "max": f"{max_change + range_y * 1:.2f}", # Adjusted to 10% padding
        },
        "legend": {"data": list(currencies.keys())},
        "series": series_data,
    }

    # Display the chart using st_echarts
    st_echarts(options=options, height="500px")
else:
    st.warning("Not all data available for all currencies to display the Gradient Stacked Area Chart.")
    
# --- Pie/Doughnut Chart and Heatmap in Columns ---
st.subheader("Daily Change Analysis")

col_left, col_right = st.columns([0.3, 0.7])

with col_left:
    st.subheader("Pie/Doughnut Chart (Daily Change %)")

    if all(not data.empty for data in exchange_data.values()):
        # Prepare data for ECharts
        pie_data = []
        for currency, data in exchange_data.items():
            # Calculate daily change percentage
            daily_change = data['Close'].iloc[-1] - data['Close'].iloc[-2] if len(data) >= 2 else 0
            daily_change_percent = (daily_change / data['Close'].iloc[-2]) * 100 if len(data) >= 2 and data['Close'].iloc[-2] != 0 else 0
            pie_data.append({"value": abs(daily_change_percent), "name": currency})

        # ECharts options for Pie/Doughnut Chart
        options = {
            "title": {"text": "Daily Change % Distribution", "left": "center"},
            "tooltip": {"trigger": "item", "formatter": "{a} <br/>{b} : {c} ({d}%)"},
            "legend": {"orient": "vertical", "left": "left", "data": list(currencies.keys())},
            "series": [
                {
                    "name": "Daily Change %",
                    "type": "pie",
                    "radius": ["40%", "70%"],
                    "data": pie_data,
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowOffsetX": 0,
                            "shadowColor": "rgba(0, 0, 0, 0.5)",
                        }
                    },
                }
            ],
        }

        # Display the chart using st_echarts
        st_echarts(options=options, height="500px", key="pie_chart")  # Added a key for streamlit to differentiate charts
    else:
        st.warning("Not all data available for all currencies to display the Pie/Doughnut Chart.")

with col_right:
    st.subheader("Heatmap (Daily Change %)")

    if all(not data.empty for data in exchange_data.values()):
        # Prepare data for ECharts
        heatmap_data = []
        dates = list(exchange_data.values())[0].index.strftime('%Y-%m-%d %H:%M').tolist() if selected_interval not in ["1d", "1wk"] else list(exchange_data.values())[0].index.strftime('%Y-%m-%d').tolist()
        currencies_list = list(currencies.keys())

        for i, (currency, data) in enumerate(exchange_data.items()):
            # Calculate daily change percentage
            daily_changes = data['Close'].pct_change() * 100
            daily_changes.iloc[0] = 0  # Set the first value to 0 (no change for the first day)
            rates = daily_changes.tolist()
            for j, rate in enumerate(rates):
                heatmap_data.append([j, i, rate])

        # Calculate the range of values for the visual map
        all_changes = []
        for data in exchange_data.values():
            daily_changes = data['Close'].pct_change() * 100
            all_changes.extend(daily_changes.tolist())

        # Remove NaN values
        all_changes = [x for x in all_changes if pd.notna(x)]

        if all_changes:  # Check if all_changes is not empty
            min_change = min(all_changes)
            max_change = max(all_changes)
        else:
            min_change = -1
            max_change = 1

        # ECharts options for Heatmap
        options = {
            "title": {"text": "Daily Change % Heatmap"},
            "tooltip": {"position": "top", "formatter": "{c}"},
            "grid": {"height": "60%", "top": "20%"},
            "xAxis": {"type": "category", "data": dates, "splitArea": {"show": True}},
            "yAxis": {"type": "category", "data": currencies_list, "splitArea": {"show": True}},
            "visualMap": {
                "min": min_change,
                "max": max_change,
                "orient": "horizontal",
                "left": "center",
                "bottom": "1%",
                "text": ["High", "Low"],
                "calculable": True,
                "inRange": {"color": ["#fff9eb","#7c11a7"]},
            },
            "series": [
                {
                    "name": "Daily Change %",
                    "type": "heatmap",
                    "data": heatmap_data,
                    "label": {"show": False},
                    "emphasis": {
                        "itemStyle": {
                            "shadowBlur": 10,
                            "shadowColor": 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }
            ],
        }
        # Display the chart using st_echarts
        st_echarts(options=options, height="500px", key="heatmap") # Added a key for streamlit to differentiate charts
    else:
        st.warning("Not all data available for all currencies to display the Heatmap.")

    

# --- Scatter Plot ---------------------------------------------------------------------------------------------------------------------------
st.subheader("Scatter Plot (Closing Prices vs. Date)")

if selected_currency in exchange_data:
    data = exchange_data[selected_currency]
    if not data.empty:
        # Prepare data for ECharts
        dates = data.index.strftime('%Y-%m-%d %H:%M').tolist() if selected_interval not in ["1d", "1wk"] else data.index.strftime('%Y-%m-%d').tolist()
        closing_prices = data['Close'].tolist()

        scatter_data = [[price, date] for price, date in zip(closing_prices, dates)]

        # Calculate the range of x-axis
        min_price = min(closing_prices)
        max_price = max(closing_prices)
        range_x = max_price - min_price

        # ECharts options for Scatter Plot
        options = {
            "title": {"text": f"{selected_currency} Closing Prices Scatter Plot"},
            "tooltip": {
                "trigger": "item",
                "formatter": "{c}",
            },
            "xAxis": {
                "type": "value",
                "name": "Closing Price",
                "min": f"{min_price - range_x * 0.1:.2f}",
                "max": f"{max_price + range_x * 0.1:.2f}",
            },
            "yAxis": {"type": "category", "data": dates, "name": "Date"},
            "visualMap": {
                "show": True,
                "min": min_price,
                "max": max_price,
                "dimension": 0,  # Use the first dimension (price) for visual mapping
                "inRange": {
                    "color": ["#4292c6"],  # Darker blue gradient
                    "symbolSize": 10, # Adjust symbol size based on value
                },
                "calculable": True,
                "orient": "horizontal",
                "left": "center",
                "bottom": "5%",
            },
            "series": [
                {
                    "data": scatter_data,
                    "type": "scatter",
                    "symbolSize": 10,
                    "itemStyle": {
                        "color": "#08519c", # Darker default color
                    },
                    "emphasis": {
                        "focus": "series",
                        "itemStyle": {
                            "color": "#FFD700",  # Highlight color on hover (Gold)
                            "borderColor": "#8B4513", # Darker border color (Saddle Brown)
                            "borderWidth": 2,
                        },
                    },
                }
            ],
        }

        # Display the chart using st_echarts
        st_echarts(options=options, height="700px")
    else:
        st.warning(f"No data available for {selected_currency} to display the Scatter Plot.")
else:
    st.warning("Please select a currency.")


