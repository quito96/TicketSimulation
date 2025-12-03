import streamlit as st

def render_language_selector():
    """Renders the language selector in the sidebar with flags."""
    if 'language' not in st.session_state:
        st.session_state['language'] = 'DE'
    
    def format_func(option):
        return '🇩🇪 DE' if option == 'DE' else '🇬🇧 EN'
    
    st.sidebar.selectbox(
        "Sprache / Language",
        options=['DE', 'EN'],
        index=0 if st.session_state['language'] == 'DE' else 1,
        key='lang_select',
        format_func=format_func,
        on_change=lambda: st.session_state.update({'language': st.session_state.lang_select})
    )

TRANSLATIONS = {
    'EN': {
        # General
        'page_title_home': "Ticket System Simulation",
        'page_title_compare': "Simulation Comparison",
        'sidebar_settings': "⚙️ Simulation Parameters",
        'language': "Language / Sprache",
        
        # Home Page
        'home_title': "🎫 Ticket System Resolution Time Simulation",
        'home_desc': """This simulation models the performance of a ticket support system based on staffing, inbound traffic, and complexity.
Adjust the parameters in the sidebar to see how they impact **Resolution Time** and **Backlog**.""",
        
        # Sidebar - Staffing
        'header_staffing': "1. Staffing",
        'ft_agents': "Full-Time Agents",
        'pt_agents': "Part-Time Agents",
        'pt_hours': "Part-Time Hours/Day",
        'efficiency': "Agent Efficiency (Tickets/Hour)",
        'absenteeism': "Absenteeism Rate (%)",
        'help_ft': "Number of agents working 8 hours/day",
        'help_pt': "Number of agents working partial hours",
        'help_eff': "Base number of tickets an agent can solve per hour",
        'help_absent': "Percentage of staff absent on any given day",
        
        # Sidebar - Inbound
        'header_inbound': "2. Inbound Traffic",
        'avg_inbound': "Avg Daily Inbound Tickets",
        'volatility': "Daily Volatility (%)",
        'seasonality': "Enable Seasonality/Spikes",
        'help_volatility': "Random fluctuation in daily ticket volume",
        
        # Sidebar - Ticket Props
        'header_props': "3. Ticket Properties",
        'complexity_dist': "**Complexity Distribution**",
        'comp_low': "Low %",
        'comp_med': "Med %",
        'comp_high': "High %",
        'warn_normalize': "Total complexity is {total}%. It will be normalized.",
        'automation': "AI/Automation Deflection (%)",
        
        # KPIs
        'kpi_wait': "Avg Wait Time",
        'kpi_backlog': "Max Backlog",
        'kpi_solved': "Total Solved",
        'kpi_clearance': "Clearance Rate",
        
        # Charts
        'chart_pulse': "📈 The Pulse: Inbound vs. Capacity vs. Backlog",
        'chart_dist': "📊 Resolution Time Distribution",
        'chart_staff': "👥 Staff Availability",
        'legend_inbound': "Net Inbound",
        'legend_capacity': "Capacity",
        'legend_backlog': "Backlog",
        
        # Data Table
        'expander_data': "View Detailed Data",
        
        # Comparison Page
        'compare_title': "⚖️ Scenario Comparison",
        'compare_desc': "Compare two staffing strategies side-by-side under the **same** inbound traffic conditions.",
        'header_shared': "🔒 Shared Environment",
        'info_shared': "These parameters apply to BOTH scenarios.",
        'header_scen_a': "🔵 Scenario A",
        'header_scen_b': "🟠 Scenario B",
        'config_a': "Configure Staffing A",
        'config_b': "Configure Staffing B",
        'ft_agents_a': "🔵 FT Agents (A)",
        'pt_agents_a': "🔵 PT Agents (A)",
        'eff_a': "🔵 Efficiency (A)",
        'absent_a': "🔵 Absenteeism % (A)",
        'ft_agents_b': "🟠 FT Agents (B)",
        'pt_agents_b': "🟠 PT Agents (B)",
        'eff_b': "🟠 Efficiency (B)",
        'absent_b': "🟠 Absenteeism % (B)",
        
        # Comparison Visuals
        'kpi_compare': "📊 KPI Comparison",
        'kpi_wait_a': "Avg Wait Time (A)",
        'kpi_wait_b': "Avg Wait Time (B)",
        'kpi_backlog_a': "Max Backlog (A)",
        'kpi_backlog_b': "Max Backlog (B)",
        'kpi_hours_a': "Total Staff Hours (A)",
        'kpi_hours_b': "Total Staff Hours (B)",
        'pulse_compare': "📈 Pulse Comparison",
        'pulse_a': "🔵 Scenario A Pulse",
        'pulse_b': "🟠 Scenario B Pulse",
        'box_title': "📦 Wait Time Distribution (Boxplot)",
        'cdf_title': "📉 Probability of Resolution (CDF)",
        'axis_wait': "Wait Time (Hours)",
        'axis_prob': "Probability (<= x)",
        'title_cdf': "CDF of Wait Time",
    },
    'DE': {
        # General
        'page_title_home': "Ticket-System Simulation",
        'page_title_compare': "Simulations-Vergleich",
        'sidebar_settings': "⚙️ Simulations-Parameter",
        'language': "Sprache / Language",
        
        # Home Page
        'home_title': "🎫 Ticket-System Lösungszeit-Simulation",
        'home_desc': """Diese Simulation modelliert die Leistung eines Ticketsystems basierend auf Personal, Ticketaufkommen und Komplexität.
Passen Sie die Parameter in der Seitenleiste an, um die Auswirkungen auf **Lösungszeit** und **Rückstau (Backlog)** zu sehen.""",
        
        # Sidebar - Staffing
        'header_staffing': "1. Personalplanung",
        'ft_agents': "Vollzeit-Agenten",
        'pt_agents': "Teilzeit-Agenten",
        'pt_hours': "Stunden/Tag (Teilzeit)",
        'efficiency': "Effizienz (Tickets/Stunde)",
        'absenteeism': "Abwesenheitsquote (%)",
        'help_ft': "Anzahl der Agenten mit 8 Stunden/Tag",
        'help_pt': "Anzahl der Agenten mit Teilzeit",
        'help_eff': "Basis-Anzahl Tickets, die ein Agent pro Stunde lösen kann",
        'help_absent': "Prozentsatz des Personals, der an einem Tag fehlt (Krankheit/Urlaub)",
        
        # Sidebar - Inbound
        'header_inbound': "2. Ticketaufkommen (Inbound)",
        'avg_inbound': "Ø Tägliche Tickets",
        'volatility': "Tägliche Volatilität (%)",
        'seasonality': "Saisonalität aktivieren",
        'help_volatility': "Zufällige Schwankung im täglichen Volumen",
        
        # Sidebar - Ticket Props
        'header_props': "3. Ticket-Eigenschaften",
        'complexity_dist': "**Komplexitäts-Verteilung**",
        'comp_low': "Niedrig %",
        'comp_med': "Mittel %",
        'comp_high': "Hoch %",
        'warn_normalize': "Gesamtkomplexität ist {total}%. Wird normalisiert.",
        'automation': "KI/Automatisierung (%)",
        
        # KPIs
        'kpi_wait': "Ø Wartezeit",
        'kpi_backlog': "Max Rückstau",
        'kpi_solved': "Gelöst Gesamt",
        'kpi_clearance': "Lösungsquote",
        
        # Charts
        'chart_pulse': "📈 Der Puls: Eingang vs. Kapazität vs. Rückstau",
        'chart_dist': "📊 Verteilung der Lösungszeiten",
        'chart_staff': "👥 Personalverfügbarkeit",
        'legend_inbound': "Netto Eingang",
        'legend_capacity': "Kapazität",
        'legend_backlog': "Rückstau",
        
        # Data Table
        'expander_data': "Detaillierte Daten anzeigen",
        
        # Comparison Page
        'compare_title': "⚖️ Szenario-Vergleich",
        'compare_desc': "Vergleichen Sie zwei Personalstrategien Seite an Seite unter **gleichen** Eingangsbedingungen.",
        'header_shared': "🔒 Gemeinsame Umgebung",
        'info_shared': "Diese Parameter gelten für BEIDE Szenarien.",
        'header_scen_a': "🔵 Szenario A",
        'header_scen_b': "🟠 Szenario B",
        'config_a': "Konfiguration Personal A",
        'config_b': "Konfiguration Personal B",
        'ft_agents_a': "🔵 Vollzeit (A)",
        'pt_agents_a': "🔵 Teilzeit (A)",
        'eff_a': "🔵 Effizienz (A)",
        'absent_a': "🔵 Abwesenheit % (A)",
        'ft_agents_b': "🟠 Vollzeit (B)",
        'pt_agents_b': "🟠 Teilzeit (B)",
        'eff_b': "🟠 Effizienz (B)",
        'absent_b': "🟠 Abwesenheit % (B)",
        
        # Comparison Visuals
        'kpi_compare': "📊 KPI Vergleich",
        'kpi_wait_a': "Ø Wartezeit (A)",
        'kpi_wait_b': "Ø Wartezeit (B)",
        'kpi_backlog_a': "Max Rückstau (A)",
        'kpi_backlog_b': "Max Rückstau (B)",
        'kpi_hours_a': "Personalstunden (A)",
        'kpi_hours_b': "Personalstunden (B)",
        'pulse_compare': "📈 Puls-Vergleich",
        'pulse_a': "🔵 Szenario A Puls",
        'pulse_b': "🟠 Szenario B Puls",
        'box_title': "📦 Wartezeit-Verteilung (Boxplot)",
        'cdf_title': "📉 Lösungswahrscheinlichkeit (CDF)",
        'axis_wait': "Wartezeit (Stunden)",
        'axis_prob': "Wahrscheinlichkeit (<= x)",
        'title_cdf': "CDF der Wartezeit",
    }
}
