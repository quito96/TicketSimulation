import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from simulation import run_simulation

st.set_page_config(page_title="Ticket System Simulation", layout="wide")

st.title("🎫 Ticket System Resolution Time Simulation")
st.markdown("""
This simulation models the performance of a ticket support system based on staffing, inbound traffic, and complexity.
Adjust the parameters in the sidebar to see how they impact **Resolution Time** and **Backlog**.
""")

# --- Sidebar Controls ---
st.sidebar.header("⚙️ Simulation Parameters")

st.sidebar.subheader("1. Staffing")
full_time_agents = st.sidebar.slider("Full-Time Agents", 0, 20, 5, help="Number of agents working 8 hours/day")
part_time_agents = st.sidebar.slider("Part-Time Agents", 0, 10, 2, help="Number of agents working partial hours")
part_time_hours = st.sidebar.slider("Part-Time Hours/Day", 1, 8, 4)
agent_efficiency = st.sidebar.slider("Agent Efficiency (Tickets/Hour)", 1, 20, 5, help="Base number of tickets an agent can solve per hour")
vacation_rate = st.sidebar.slider("Absenteeism Rate (%)", 0, 50, 5, help="Percentage of staff absent on any given day") / 100.0

st.sidebar.subheader("2. Inbound Traffic")
avg_daily_tickets = st.sidebar.slider("Avg Daily Inbound Tickets", 10, 1000, 100)
volatility = st.sidebar.slider("Daily Volatility (%)", 0, 100, 20, help="Random fluctuation in daily ticket volume") / 100.0
seasonality_factor = st.sidebar.checkbox("Enable Seasonality/Spikes", value=False) # Placeholder for future logic

st.sidebar.subheader("3. Ticket Properties")
st.sidebar.markdown("**Complexity Distribution**")
col1, col2, col3 = st.sidebar.columns(3)
comp_low = col1.number_input("Low %", 0, 100, 50)
comp_med = col2.number_input("Med %", 0, 100, 30)
comp_high = col3.number_input("High %", 0, 100, 20)

# Normalize complexity if not 100%
total_comp = comp_low + comp_med + comp_high
if total_comp != 100:
    st.sidebar.warning(f"Total complexity is {total_comp}%. It will be normalized.")
    comp_low = comp_low / total_comp
    comp_med = comp_med / total_comp
    comp_high = comp_high / total_comp
else:
    comp_low /= 100.0
    comp_med /= 100.0
    comp_high /= 100.0

automation_rate = st.sidebar.slider("AI/Automation Deflection (%)", 0, 100, 10) / 100.0

# --- Run Simulation ---
df = run_simulation(
    days=60,
    avg_daily_tickets=avg_daily_tickets,
    volatility=volatility,
    full_time_agents=full_time_agents,
    part_time_agents=part_time_agents,
    agent_efficiency=agent_efficiency,
    part_time_hours=part_time_hours,
    vacation_rate=vacation_rate,
    complexity_mix={'Low': comp_low, 'Medium': comp_med, 'High': comp_high},
    automation_rate=automation_rate
)

# --- Dashboard ---

# 1. KPI Row
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

avg_wait = df['Est. Wait Time (Hours)'].mean()
max_backlog = df['Backlog (End of Day)'].max()
total_solved = df['Solved'].sum()
total_inbound = df['Inbound (Net)'].sum()

kpi1.metric("Avg Wait Time", f"{avg_wait:.1f} Hours", delta_color="inverse")
kpi2.metric("Max Backlog", f"{max_backlog} Tickets", delta_color="inverse")
kpi3.metric("Total Solved", f"{total_solved}")
kpi4.metric("Clearance Rate", f"{(total_solved/total_inbound)*100:.1f}%")

# 2. Main Chart: The Pulse
st.subheader("📈 The Pulse: Inbound vs. Capacity vs. Backlog")
fig_pulse = go.Figure()
fig_pulse.add_trace(go.Scatter(x=df['Date'], y=df['Inbound (Net)'], name='Net Inbound', line=dict(color='blue', dash='dot')))
fig_pulse.add_trace(go.Scatter(x=df['Date'], y=df['Capacity (Tickets)'], name='Capacity', line=dict(color='green')))
fig_pulse.add_trace(go.Scatter(x=df['Date'], y=df['Backlog (End of Day)'], name='Backlog', fill='tozeroy', line=dict(color='red')))
st.plotly_chart(fig_pulse, width="stretch")

# 3. Secondary Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📊 Resolution Time Distribution")
    # Histogram of wait times
    fig_hist = px.histogram(df, x="Est. Wait Time (Hours)", nbins=20, title="Daily Est. Wait Time Distribution")
    st.plotly_chart(fig_hist, width="stretch")

with col_right:
    st.subheader("👥 Staff Availability")
    # Stacked area of staff
    df['Total Staff Hours'] = (df['Staff Available (FT)'] * 8) + (df['Staff Available (PT)'] * part_time_hours)
    fig_staff = px.bar(df, x='Date', y=['Staff Available (FT)', 'Staff Available (PT)'], title="Daily Staff Count")
    st.plotly_chart(fig_staff, width="stretch")

# 4. Data Table
with st.expander("View Detailed Data"):
    st.dataframe(df)

