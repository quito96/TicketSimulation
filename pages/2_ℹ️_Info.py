import streamlit as st
from translations import TRANSLATIONS, render_language_selector

# Ensure language is set (if user lands directly here)
if 'language' not in st.session_state:
    st.session_state['language'] = 'DE'

def get_text():
    return TRANSLATIONS[st.session_state['language']]

t = get_text()

st.set_page_config(page_title=t['page_title_info'], layout="wide", page_icon="ℹ️")

# Language Selector
render_language_selector()

# Re-fetch text after potential language change
t = get_text()

st.title(t['info_title'])
st.markdown(f"*{t['info_subtitle']}*")
st.divider()

# Overview Section
st.header(t['section_overview'])
st.markdown(t['overview_text'])

st.divider()

# How it Works Section
st.header(t['section_how_it_works'])
col1, col2 = st.columns(2)

with col1:
    st.markdown(t['how_step_1'])
    st.markdown(t['how_step_2'])
    st.markdown(t['how_step_3'])

with col2:
    st.markdown(t['how_step_4'])
    st.markdown(t['how_step_5'])
    st.markdown(t['how_step_6'])

st.divider()

# Key Metrics Section
st.header(t['section_key_metrics'])
col1, col2 = st.columns(2)

with col1:
    st.markdown(t['metric_wait_desc'])
    st.markdown(t['metric_backlog_desc'])

with col2:
    st.markdown(t['metric_solved_desc'])
    st.markdown(t['metric_clearance_desc'])

st.divider()

# Model Features Section
st.header(t['section_model_features'])
st.success("""
""" + t['feature_1'] + """

""" + t['feature_2'] + """

""" + t['feature_3'] + """

""" + t['feature_4'] + """

""" + t['feature_5'])

st.divider()

# Limitations Section
st.header(t['section_limitations'])
st.warning("""
""" + t['limitation_1'] + """

""" + t['limitation_2'] + """

""" + t['limitation_3'] + """

""" + t['limitation_4'] + """

""" + t['limitation_5'] + """

""" + t['limitation_6'])

st.divider()

# Use Cases Section
st.header(t['section_use_cases'])
col1, col2 = st.columns(2)

with col1:
    st.info(t['use_case_good'])

with col2:
    st.error(t['use_case_bad'])

st.divider()

# Documentation Section
st.header(t['section_docs'])
st.markdown(t['docs_link_logic'])
st.markdown(t['docs_link_limits'])
st.markdown(t['docs_link_changes'])

st.divider()

# Validation Section
st.header(t['section_validation'])
st.markdown(t['validation_text'])

st.divider()

# Author Section
st.header(t['section_author'])
st.markdown(t['author_text'])
st.caption(t['version_text'])
