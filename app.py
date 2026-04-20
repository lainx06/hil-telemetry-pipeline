import streamlit as st
import serial
import pandas as pd
import plotly.express as px
import time

# --- System Configuration ---
SERIAL_PORT = 'COM3' # UPDATE THIS TO YOUR PORT (e.g., COM4, /dev/cu.usbmodem...)
BAUD_RATE = 9600

# Initialize Serial Connection
@st.cache_resource
def init_serial():
    try:
        return serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    except Exception as e:
        st.error(f"Hardware connection failed: {e}")
        return None

ser = init_serial()

# --- Dashboard UI ---
st.title("Ultrasonic Telemetry Pipeline")
st.markdown("Real-time hardware-in-the-loop sensor data integration.")

graph_placeholder = st.empty()

if 'sensor_data' not in st.session_state:
    st.session_state.sensor_data = pd.DataFrame(columns=['Time', 'Distance_cm'])

# --- Data Ingestion Loop ---
if st.button("Start Data Pipeline") and ser:
    while True:
        try:
            # Read raw data from the microcontroller
            raw_data = ser.readline().decode('utf-8').strip()
            
            if raw_data.replace('.', '', 1).isdigit():
                distance = float(raw_data)
                current_time = time.strftime('%H:%M:%S')
                
                # Append new data
                new_row = pd.DataFrame({'Time': [current_time], 'Distance_cm': [distance]})
                st.session_state.sensor_data = pd.concat([st.session_state.sensor_data, new_row], ignore_index=True)
                
                # Maintain memory efficiency (keep last 50 points)
                if len(st.session_state.sensor_data) > 50:
                    st.session_state.sensor_data = st.session_state.sensor_data.iloc[-50:]
                
                # Render the updated graph
                fig = px.line(st.session_state.sensor_data, x='Time', y='Distance_cm', title='Live Distance Tracking (cm)')
                fig.update_yaxes(range=[0, 200]) 
                graph_placeholder.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.warning(f"Pipeline interrupted: {e}")
            break
        
        time.sleep(0.1)
        #use python -m streamlit run radar_dashboard.py to run
