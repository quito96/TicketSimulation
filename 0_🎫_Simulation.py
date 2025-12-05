import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from simulation import run_simulation
from translations import TRANSLATIONS, render_language_selector

# Initialize Session State for Language
if 'language' not in st.session_state:
    st.session_state['language'] = 'DE'

def get_text():
    return TRANSLATIONS[st.session_state['language']]

t = get_text()

st.set_page_config(page_title=t['page_title_home'], layout="wide")

# Language Selector (Sidebar Top)
render_language_selector()

# Re-fetch text after potential language change
t = get_text()

st.title(t['home_title'])
st.markdown(t['home_desc'])

# --- Sidebar Controls ---
st.sidebar.header(t['sidebar_settings'])

st.sidebar.subheader(t['header_staffing'])
full_time_agents = st.sidebar.slider(t['ft_agents'], 0, 20, 5, help=t['help_ft'])
part_time_agents = st.sidebar.slider(t['pt_agents'], 0, 10, 2, help=t['help_pt'])
part_time_hours = st.sidebar.slider(t['pt_hours'], 1, 8, 4)
agent_efficiency = st.sidebar.slider(t['efficiency'], 1, 20, 5, help=t['help_eff'])
vacation_rate = st.sidebar.slider(t['absenteeism'], 0, 50, 5, help=t['help_absent']) / 100.0

st.sidebar.subheader(t['header_inbound'])
avg_daily_tickets = st.sidebar.slider(t['avg_inbound'], 10, 1000, 100)
volatility = st.sidebar.slider(t['volatility'], 0, 100, 20, help=t['help_volatility']) / 100.0

st.sidebar.subheader(t['header_props'])
st.sidebar.markdown(t['complexity_dist'])
col1, col2, col3 = st.sidebar.columns(3)
comp_low = col1.number_input(t['comp_low'], 0, 100, 50)
comp_med = col2.number_input(t['comp_med'], 0, 100, 30)
comp_high = col3.number_input(t['comp_high'], 0, 100, 20)

# Normalize complexity if not 100%
total_comp = comp_low + comp_med + comp_high
if total_comp != 100:
    st.sidebar.warning(t['warn_normalize'].format(total=total_comp))
    comp_low = comp_low / total_comp
    comp_med = comp_med / total_comp
    comp_high = comp_high / total_comp
else:
    comp_low /= 100.0
    comp_med /= 100.0
    comp_high /= 100.0

automation_rate = st.sidebar.slider(t['automation'], 0, 100, 10) / 100.0

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

kpi1.metric(t['kpi_wait'], f"{avg_wait:.1f} Hours", delta_color="inverse")
kpi2.metric(t['kpi_backlog'], f"{max_backlog} Tickets", delta_color="inverse")
kpi3.metric(t['kpi_solved'], f"{total_solved}")
kpi4.metric(t['kpi_clearance'], f"{(total_solved/total_inbound)*100:.1f}%")

# 2. Main Chart: The Pulse
st.subheader(t['chart_pulse'])
fig_pulse = go.Figure()
fig_pulse.add_trace(go.Scatter(x=df['Date'], y=df['Inbound (Net)'], name=t['legend_inbound'], line=dict(color='blue', dash='dot')))
fig_pulse.add_trace(go.Scatter(x=df['Date'], y=df['Capacity (Tickets)'], name=t['legend_capacity'], line=dict(color='green')))
fig_pulse.add_trace(go.Scatter(x=df['Date'], y=df['Backlog (End of Day)'], name=t['legend_backlog'], fill='tozeroy', line=dict(color='red')))
st.plotly_chart(fig_pulse, width="stretch")

# 3. Secondary Charts
col_left, col_right = st.columns(2)

with col_left:
    st.subheader(t['chart_dist'])
    # Histogram of wait times
    fig_hist = px.histogram(df, x="Est. Wait Time (Hours)", nbins=20, title=t['chart_dist'])
    st.plotly_chart(fig_hist, width="stretch")

with col_right:
    st.subheader(t['chart_staff'])
    # Stacked area of staff
    df['Total Staff Hours'] = (df['Staff Available (FT)'] * 8) + (df['Staff Available (PT)'] * part_time_hours)
    fig_staff = px.bar(df, x='Date', y=['Staff Available (FT)', 'Staff Available (PT)'], title=t['chart_staff'])
    st.plotly_chart(fig_staff, width="stretch")

# 4. Data Table
with st.expander(t['expander_data']):
    st.dataframe(df)
