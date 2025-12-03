import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from simulation import run_simulation

st.set_page_config(page_title="Simulation Comparison", layout="wide", page_icon="⚖️")

st.title("⚖️ Scenario Comparison")
st.markdown("Compare two staffing strategies side-by-side under the **same** inbound traffic conditions.")

# --- Shared Parameters (Sidebar) ---
st.sidebar.header("🔒 Shared Environment")
st.sidebar.info("These parameters apply to BOTH scenarios.")

# Inbound
st.sidebar.subheader("Inbound Traffic")
avg_daily_tickets = st.sidebar.slider("Avg Daily Inbound", 10, 1000, 178)
volatility = st.sidebar.slider("Volatility (%)", 0, 100, 25) / 100.0

# Ticket Properties
st.sidebar.subheader("Ticket Properties")
col1, col2, col3 = st.sidebar.columns(3)
comp_low = col1.number_input("Low %", 0, 100, 50)
comp_med = col2.number_input("Med %", 0, 100, 30)
comp_high = col3.number_input("High %", 0, 100, 20)

# Normalize complexity
total_comp = comp_low + comp_med + comp_high
if total_comp != 100:
    comp_low /= total_comp
    comp_med /= total_comp
    comp_high /= total_comp
else:
    comp_low /= 100.0
    comp_med /= 100.0
    comp_high /= 100.0

automation_rate = st.sidebar.slider("Automation (%)", 0, 100, 10) / 100.0

# --- Staffing Scenarios (Main Area) ---
col_a, col_b = st.columns(2)

with col_a:
    st.header("🔵 Scenario A")
    with st.expander("Configure Staffing A", expanded=True):
        ft_a = st.slider("🔵 FT Agents (A)", 0, 20, 5, key="ft_a")
        pt_a = st.slider("🔵 PT Agents (A)", 0, 10, 0, key="pt_a")
        eff_a = st.slider("🔵 Efficiency (A)", 1, 20, 5, key="eff_a")
        vac_a = st.slider("🔵 Absenteeism % (A)", 0, 50, 5, key="vac_a") / 100.0

with col_b:
    st.header("🟠 Scenario B")
    with st.expander("Configure Staffing B", expanded=True):
        ft_b = st.slider("🟠 FT Agents (B)", 0, 20, 5, key="ft_b")
        pt_b = st.slider("🟠 PT Agents (B)", 0, 10, 0, key="pt_b")
        eff_b = st.slider("🟠 Efficiency (B)", 1, 20, 5, key="eff_b")
        vac_b = st.slider("🟠 Absenteeism % (B)", 0, 50, 15, key="vac_b") / 100.0

# --- Run Simulations ---
# We need to use the same random seed logic or just run them. 
# Note: run_simulation uses numpy.random. If we want EXACTLY the same inbound pattern,
# we might need to modify run_simulation to accept a seed or pre-generated inbound.
# For now, we assume the "law of large numbers" or just accept slight variations, 
# OR we can hack it by setting the seed before each call if we want identical inbound.

# To ensure fair comparison, let's set the seed before EACH run so Inbound/Volatility is identical.
seed = 42

np.random.seed(seed)
df_a = run_simulation(
    days=60,
    avg_daily_tickets=avg_daily_tickets,
    volatility=volatility,
    full_time_agents=ft_a,
    part_time_agents=pt_a,
    agent_efficiency=eff_a,
    vacation_rate=vac_a,
    complexity_mix={'Low': comp_low, 'Medium': comp_med, 'High': comp_high},
    automation_rate=automation_rate
)

np.random.seed(seed) # RESET SEED for Scenario B to get identical Inbound/Vacation patterns
df_b = run_simulation(
    days=60,
    avg_daily_tickets=avg_daily_tickets,
    volatility=volatility,
    full_time_agents=ft_b,
    part_time_agents=pt_b,
    agent_efficiency=eff_b,
    vacation_rate=vac_b,
    complexity_mix={'Low': comp_low, 'Medium': comp_med, 'High': comp_high},
    automation_rate=automation_rate
)

df_a['Scenario'] = 'A'
df_b['Scenario'] = 'B'
df_combined = pd.concat([df_a, df_b])

# --- Comparison Visualizations ---

st.divider()

# 1. KPI Comparison
st.subheader("📊 KPI Comparison")
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

wait_a = df_a['Est. Wait Time (Hours)'].mean()
wait_b = df_b['Est. Wait Time (Hours)'].mean()
delta_wait = wait_b - wait_a

backlog_a = df_a['Backlog (End of Day)'].max()
backlog_b = df_b['Backlog (End of Day)'].max()
delta_backlog = backlog_b - backlog_a

kpi_col1.metric("Avg Wait Time (A)", f"{wait_a:.1f} Hours")
kpi_col1.metric("Avg Wait Time (B)", f"{wait_b:.1f} Hours", delta=f"{delta_wait:.1f} Hours", delta_color="inverse")

kpi_col2.metric("Max Backlog (A)", f"{backlog_a} Tickets")
kpi_col2.metric("Max Backlog (B)", f"{backlog_b} Tickets", delta=f"{delta_backlog} Tickets", delta_color="inverse")

# Cost/Hours proxy
hours_a = (df_a['Staff Available (FT)'].sum() * 8) + (df_a['Staff Available (PT)'].sum() * 4)
hours_b = (df_b['Staff Available (FT)'].sum() * 8) + (df_b['Staff Available (PT)'].sum() * 4)
delta_hours = hours_b - hours_a
kpi_col3.metric("Total Staff Hours (A)", f"{hours_a}")
kpi_col3.metric("Total Staff Hours (B)", f"{hours_b}", delta=f"{delta_hours}", delta_color="inverse") # Inverse? More hours = bad usually? Or neutral.

# 2. Comparative Pulse (Side-by-Side)
st.subheader("📈 Pulse Comparison")
pulse_col1, pulse_col2 = st.columns(2)

with pulse_col1:
    st.markdown("### 🔵 Scenario A Pulse")
    fig_pulse_a = go.Figure()
    fig_pulse_a.add_trace(go.Scatter(x=df_a['Date'], y=df_a['Inbound (Net)'], name='Inbound', line=dict(color='gray', dash='dot')))
    fig_pulse_a.add_trace(go.Scatter(x=df_a['Date'], y=df_a['Capacity (Tickets)'], name='Capacity', line=dict(color='green')))
    fig_pulse_a.add_trace(go.Scatter(x=df_a['Date'], y=df_a['Backlog (End of Day)'], name='Backlog', fill='tozeroy', line=dict(color='#1f77b4')))
    fig_pulse_a.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_pulse_a, width="stretch")

with pulse_col2:
    st.markdown("### 🟠 Scenario B Pulse")
    fig_pulse_b = go.Figure()
    fig_pulse_b.add_trace(go.Scatter(x=df_b['Date'], y=df_b['Inbound (Net)'], name='Inbound', line=dict(color='gray', dash='dot')))
    fig_pulse_b.add_trace(go.Scatter(x=df_b['Date'], y=df_b['Capacity (Tickets)'], name='Capacity', line=dict(color='green')))
    fig_pulse_b.add_trace(go.Scatter(x=df_b['Date'], y=df_b['Backlog (End of Day)'], name='Backlog', fill='tozeroy', line=dict(color='#ff7f0e')))
    fig_pulse_b.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_pulse_b, width="stretch")

# 3. Boxplot & CDF
col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    st.subheader("📦 Wait Time Distribution (Boxplot)")
    fig_box = px.box(df_combined, x='Scenario', y='Est. Wait Time (Hours)', color='Scenario', 
                     color_discrete_map={'A': '#1f77b4', 'B': '#ff7f0e'})
    st.plotly_chart(fig_box, width="stretch")

with col_viz2:
    st.subheader("📉 Probability of Resolution (CDF)")
    # Calculate CDF manually for cleaner plot
    # Sort data
    sorted_a = np.sort(df_a['Est. Wait Time (Hours)'])
    sorted_b = np.sort(df_b['Est. Wait Time (Hours)'])
    y_a = np.arange(1, len(sorted_a) + 1) / len(sorted_a)
    y_b = np.arange(1, len(sorted_b) + 1) / len(sorted_b)
    
    fig_cdf = go.Figure()
    fig_cdf.add_trace(go.Scatter(x=sorted_a, y=y_a, name='Scenario A', line=dict(color='#1f77b4')))
    fig_cdf.add_trace(go.Scatter(x=sorted_b, y=y_b, name='Scenario B', line=dict(color='#ff7f0e')))
    fig_cdf.update_layout(xaxis_title="Wait Time (Hours)", yaxis_title="Probability (<= x)", title="CDF of Wait Time")
    st.plotly_chart(fig_cdf, width="stretch")

