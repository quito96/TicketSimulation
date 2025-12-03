import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from simulation import run_simulation
from translations import TRANSLATIONS, render_language_selector

# Ensure language is set (if user lands directly here)
if 'language' not in st.session_state:
    st.session_state['language'] = 'DE'

def get_text():
    return TRANSLATIONS[st.session_state['language']]

t = get_text()

st.set_page_config(page_title=t['page_title_compare'], layout="wide", page_icon="⚖️")

# Language Selector
render_language_selector()

st.title(t['compare_title'])
st.markdown(t['compare_desc'])

# --- Shared Parameters (Sidebar) ---
st.sidebar.header(t['header_shared'])
st.sidebar.info(t['info_shared'])

# Inbound
st.sidebar.subheader(t['header_inbound'])
avg_daily_tickets = st.sidebar.slider(t['avg_inbound'], 10, 1000, 195)
volatility = st.sidebar.slider(t['volatility'], 0, 100, 25, help=t['help_volatility']) / 100.0

# Ticket Properties
st.sidebar.subheader(t['header_props'])
col1, col2, col3 = st.sidebar.columns(3)
comp_low = col1.number_input(t['comp_low'], 0, 100, 50)
comp_med = col2.number_input(t['comp_med'], 0, 100, 30)
comp_high = col3.number_input(t['comp_high'], 0, 100, 20)

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

automation_rate = st.sidebar.slider(t['automation'], 0, 100, 10) / 100.0

# --- Staffing Scenarios (Main Area) ---
col_a, col_b = st.columns(2)

with col_a:
    st.header(t['header_scen_a'])
    with st.expander(t['config_a'], expanded=True):
        ft_a = st.slider(t['ft_agents_a'], 0, 20, 5, key="ft_a", help=t['help_ft'])
        pt_a = st.slider(t['pt_agents_a'], 0, 10, 0, key="pt_a", help=t['help_pt'])
        eff_a = st.slider(t['eff_a'], 1, 20, 5, key="eff_a", help=t['help_eff'])
        vac_a = st.slider(t['absent_a'], 0, 50, 5, key="vac_a", help=t['help_absent']) / 100.0

with col_b:
    st.header(t['header_scen_b'])
    with st.expander(t['config_b'], expanded=True):
        ft_b = st.slider(t['ft_agents_b'], 0, 20, 5, key="ft_b", help=t['help_ft'])
        pt_b = st.slider(t['pt_agents_b'], 0, 10, 0, key="pt_b", help=t['help_pt'])
        eff_b = st.slider(t['eff_b'], 1, 20, 5, key="eff_b", help=t['help_eff'])
        vac_b = st.slider(t['absent_b'], 0, 50, 15, key="vac_b", help=t['help_absent']) / 100.0

# --- Run Simulations ---
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

np.random.seed(seed) # RESET SEED for Scenario B
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
st.subheader(t['kpi_compare'])
kpi_col1, kpi_col2, kpi_col3 = st.columns(3)

wait_a = df_a['Est. Wait Time (Hours)'].mean()
wait_b = df_b['Est. Wait Time (Hours)'].mean()
delta_wait = wait_b - wait_a

backlog_a = df_a['Backlog (End of Day)'].max()
backlog_b = df_b['Backlog (End of Day)'].max()
delta_backlog = backlog_b - backlog_a

kpi_col1.metric(t['kpi_wait_a'], f"{wait_a:.1f} Hours")
kpi_col1.metric(t['kpi_wait_b'], f"{wait_b:.1f} Hours", delta=f"{delta_wait:.1f} Hours", delta_color="inverse")

kpi_col2.metric(t['kpi_backlog_a'], f"{backlog_a} Tickets")
kpi_col2.metric(t['kpi_backlog_b'], f"{backlog_b} Tickets", delta=f"{delta_backlog} Tickets", delta_color="inverse")

# Cost/Hours proxy
hours_a = (df_a['Staff Available (FT)'].sum() * 8) + (df_a['Staff Available (PT)'].sum() * 4)
hours_b = (df_b['Staff Available (FT)'].sum() * 8) + (df_b['Staff Available (PT)'].sum() * 4)
delta_hours = hours_b - hours_a
kpi_col3.metric(t['kpi_hours_a'], f"{hours_a}")
kpi_col3.metric(t['kpi_hours_b'], f"{hours_b}", delta=f"{delta_hours}", delta_color="inverse")

# 2. Comparative Pulse (Side-by-Side)
st.subheader(t['pulse_compare'])
pulse_col1, pulse_col2 = st.columns(2)

with pulse_col1:
    st.markdown(f"### {t['pulse_a']}")
    fig_pulse_a = go.Figure()
    fig_pulse_a.add_trace(go.Scatter(x=df_a['Date'], y=df_a['Inbound (Net)'], name=t['legend_inbound'], line=dict(color='gray', dash='dot')))
    fig_pulse_a.add_trace(go.Scatter(x=df_a['Date'], y=df_a['Capacity (Tickets)'], name=t['legend_capacity'], line=dict(color='green')))
    fig_pulse_a.add_trace(go.Scatter(x=df_a['Date'], y=df_a['Backlog (End of Day)'], name=t['legend_backlog'], fill='tozeroy', line=dict(color='#1f77b4')))
    fig_pulse_a.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_pulse_a, width="stretch")

with pulse_col2:
    st.markdown(f"### {t['pulse_b']}")
    fig_pulse_b = go.Figure()
    fig_pulse_b.add_trace(go.Scatter(x=df_b['Date'], y=df_b['Inbound (Net)'], name=t['legend_inbound'], line=dict(color='gray', dash='dot')))
    fig_pulse_b.add_trace(go.Scatter(x=df_b['Date'], y=df_b['Capacity (Tickets)'], name=t['legend_capacity'], line=dict(color='green')))
    fig_pulse_b.add_trace(go.Scatter(x=df_b['Date'], y=df_b['Backlog (End of Day)'], name=t['legend_backlog'], fill='tozeroy', line=dict(color='#ff7f0e')))
    fig_pulse_b.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
    st.plotly_chart(fig_pulse_b, width="stretch")

# 3. Boxplot & CDF
col_viz1, col_viz2 = st.columns(2)

with col_viz1:
    st.subheader(t['box_title'])
    fig_box = px.box(df_combined, x='Scenario', y='Est. Wait Time (Hours)', color='Scenario', 
                     color_discrete_map={'A': '#1f77b4', 'B': '#ff7f0e'})
    st.plotly_chart(fig_box, width="stretch")

with col_viz2:
    st.subheader(t['cdf_title'])
    # Calculate CDF manually for cleaner plot
    # Sort data
    sorted_a = np.sort(df_a['Est. Wait Time (Hours)'])
    sorted_b = np.sort(df_b['Est. Wait Time (Hours)'])
    y_a = np.arange(1, len(sorted_a) + 1) / len(sorted_a)
    y_b = np.arange(1, len(sorted_b) + 1) / len(sorted_b)
    
    fig_cdf = go.Figure()
    fig_cdf.add_trace(go.Scatter(x=sorted_a, y=y_a, name=t['header_scen_a'], line=dict(color='#1f77b4')))
    fig_cdf.add_trace(go.Scatter(x=sorted_b, y=y_b, name=t['header_scen_b'], line=dict(color='#ff7f0e')))
    fig_cdf.update_layout(xaxis_title=t['axis_wait'], yaxis_title=t['axis_prob'], title=t['title_cdf'])
    st.plotly_chart(fig_cdf, width="stretch")
