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

        # Info Page
        'page_title_info': "Project Info",
        'info_title': "ℹ️ Project Information",
        'info_subtitle': "About this simulation and how it works",

        'section_overview': "📋 Overview",
        'overview_text': """This application simulates a support ticket system to assist with staffing
        and capacity management planning. It models realistic ticket flows considering personnel,
        complexity, and automation.""",

        'section_how_it_works': "⚙️ How Does the Simulation Work?",
        'how_step_1': "**1. Ticket Arrival**: Tickets arrive daily with configurable volatility (lognormal distribution)",
        'how_step_2': "**2. Automation**: A portion of tickets is resolved automatically (e.g., FAQ bots)",
        'how_step_3': "**3. Staff Capacity**: Available agents (full-time/part-time) minus absences",
        'how_step_4': "**4. Complexity Adjustment**: Tickets have different difficulty levels (Low/Medium/High)",
        'how_step_5': "**5. Ticket Processing**: As many tickets as possible are solved",
        'how_step_6': "**6. Backlog**: Unsolved tickets carry over to the next day",

        'section_key_metrics': "📊 Key Metrics",
        'metric_wait_desc': "**Avg Wait Time**: Time until resolution (queue + processing + reaction time)",
        'metric_backlog_desc': "**Max Backlog**: Highest number of unresolved tickets on any day",
        'metric_solved_desc': "**Total Solved**: Total number of successfully processed tickets",
        'metric_clearance_desc': "**Clearance Rate**: Percentage of solved vs. incoming tickets (≥100% = sustainable)",

        'section_model_features': "✨ Model Features (v2.0)",
        'feature_1': "**Realistic Absences**: Planned vacation/sick days instead of random daily failures",
        'feature_2': "**Lognormal Distribution**: Prevents negative ticket counts, realistic spikes",
        'feature_3': "**Precise Calculation**: Float arithmetic avoids rounding errors over long periods",
        'feature_4': "**Improved Wait Time**: Accounts for queue time + processing time + reaction time",
        'feature_5': "**Complexity Factors**: Estimated multipliers (Low: 1.0, Medium: 1.5, High: 2.5)",

        'section_limitations': "⚠️ Known Limitations",
        'limitation_1': "**Constant Complexity**: Distribution doesn't change over time",
        'limitation_2': "**Equal Efficiency**: All agents have the same performance (no experience differences)",
        'limitation_3': "**FIFO Queue**: No prioritization by SLA or urgency",
        'limitation_4': "**No Escalations**: Tickets are solved once, no reopenings",
        'limitation_5': "**Daily Granularity**: Hourly dynamics are not modeled",
        'limitation_6': "**No Seasonality**: Weekly/monthly patterns not implemented",

        'section_use_cases': "✅ Recommended Use Cases",
        'use_case_good': """**Well suited for:**
        - Strategic capacity planning (months ahead)
        - Comparing staffing strategies
        - Sensitivity analyses ("what if?")
        - Understanding steady-state behavior""",

        'use_case_bad': """**Not suitable for:**
        - Real-time operational decisions
        - Detailed SLA compliance analysis
        - Modeling specific incidents
        - Sub-hourly predictions""",

        'section_docs': "📚 Detailed Documentation",
        'docs_link_logic': "**[SIMULATION_LOGIC.md](https://github.com/quito96/TicketSimulation/blob/master/docs/SIMULATION_LOGIC.md)**: Mathematical model, formulas, algorithms",
        'docs_link_limits': "**[KNOWN_LIMITATIONS.md](https://github.com/quito96/TicketSimulation/blob/master/docs/KNOWN_LIMITATIONS.md)**: All 12 assumptions and their implications",
        'docs_link_changes': "**[CHANGELOG.md](https://github.com/quito96/TicketSimulation/blob/master/docs/CHANGELOG.md)**: Version history and changes",

        'section_validation': "🔬 Validate the Model",
        'validation_text': """To validate this model with your real data:
        1. **Ticket Volumes**: Analyze historical daily numbers, adjust parameters
        2. **Agent Efficiency**: Measure tickets per agent per day
        3. **Complexity Factors**: Analyze actual processing times by level
        4. **Wait Times**: Compare simulated with measured SLA metrics
        5. **Absence Rates**: Verify actual vacation/sick leave rates""",

        'section_author': "👨‍💻 About",
        'author_text': "Developed by **Quito96** | [GitHub Repository](https://github.com/quito96/TicketSimulation)",
        'version_text': "Version 2.0.0 - December 2025",
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

        # Info Page
        'page_title_info': "Projekt Info",
        'info_title': "ℹ️ Projekt Information",
        'info_subtitle': "Über diese Simulation und ihre Funktionsweise",

        'section_overview': "📋 Überblick",
        'overview_text': """Diese Anwendung simuliert ein Support-Ticket-System, um Personalbedarfsplanung
        und Kapazitätsmanagement zu unterstützen. Sie modelliert realistische Ticket-Flows unter
        Berücksichtigung von Personal, Komplexität und Automatisierung.""",

        'section_how_it_works': "⚙️ Wie funktioniert die Simulation?",
        'how_step_1': "**1. Ticket-Eingang**: Tickets kommen täglich mit konfigurierbarer Volatilität an (Lognormal-Verteilung)",
        'how_step_2': "**2. Automatisierung**: Ein Teil der Tickets wird automatisch gelöst (z.B. FAQ-Bots)",
        'how_step_3': "**3. Personalkapazität**: Verfügbare Agenten (Vollzeit/Teilzeit) minus Abwesenheiten",
        'how_step_4': "**4. Komplexitätsanpassung**: Tickets haben unterschiedliche Schwierigkeitsgrade (Niedrig/Mittel/Hoch)",
        'how_step_5': "**5. Ticket-Bearbeitung**: So viele Tickets wie möglich werden gelöst",
        'how_step_6': "**6. Rückstau**: Ungelöste Tickets werden auf den nächsten Tag übertragen",

        'section_key_metrics': "📊 Wichtige Kennzahlen",
        'metric_wait_desc': "**Durchschn. Wartezeit**: Zeit bis zur Lösung (Queue + Bearbeitung + Reaktionszeit)",
        'metric_backlog_desc': "**Max. Rückstau**: Höchste Anzahl ungelöster Tickets an einem Tag",
        'metric_solved_desc': "**Gelöste Tickets**: Gesamtzahl erfolgreich bearbeiteter Tickets",
        'metric_clearance_desc': "**Lösungsquote**: Prozentsatz der gelösten vs. eingegangenen Tickets (≥100% = nachhaltig)",

        'section_model_features': "✨ Modell-Features (v2.0)",
        'feature_1': "**Realistische Abwesenheiten**: Geplante Urlaubs-/Krankheitstage statt zufälliger täglicher Ausfälle",
        'feature_2': "**Lognormal-Verteilung**: Verhindert negative Ticket-Zahlen, realistische Spitzen",
        'feature_3': "**Präzise Berechnung**: Float-Arithmetik vermeidet Rundungsfehler über lange Zeiträume",
        'feature_4': "**Verbesserte Wartezeit**: Berücksichtigt Queue-Zeit + Bearbeitungszeit + Reaktionszeit",
        'feature_5': "**Komplexitätsfaktoren**: Geschätzte Multiplikatoren (Niedrig: 1.0, Mittel: 1.5, Hoch: 2.5)",

        'section_limitations': "⚠️ Bekannte Einschränkungen",
        'limitation_1': "**Konstante Komplexität**: Verteilung ändert sich nicht über die Zeit",
        'limitation_2': "**Gleiche Effizienz**: Alle Agenten haben die gleiche Leistung (keine Erfahrungsunterschiede)",
        'limitation_3': "**FIFO-Warteschlange**: Keine Priorisierung nach SLA oder Dringlichkeit",
        'limitation_4': "**Keine Eskalationen**: Tickets werden einmal gelöst, keine Wiederöffnungen",
        'limitation_5': "**Tages-Granularität**: Stunden-genaue Dynamiken werden nicht modelliert",
        'limitation_6': "**Keine Saisonalität**: Wöchentliche/monatliche Muster nicht implementiert",

        'section_use_cases': "✅ Empfohlene Anwendungsfälle",
        'use_case_good': """**Gut geeignet für:**
        - Strategische Kapazitätsplanung (Monate im Voraus)
        - Vergleich von Personalstrategien
        - Sensitivitätsanalysen ("Was wäre wenn?")
        - Verständnis von Steady-State-Verhalten""",

        'use_case_bad': """**Nicht geeignet für:**
        - Echtzeit-Betriebsentscheidungen
        - Detaillierte SLA-Compliance-Analyse
        - Modellierung spezifischer Vorfälle
        - Vorhersagen unter der Stunde""",

        'section_docs': "📚 Ausführliche Dokumentation",
        'docs_link_logic': "**[SIMULATION_LOGIC.md](https://github.com/quito96/TicketSimulation/blob/master/docs/SIMULATION_LOGIC.md)**: Mathematisches Modell, Formeln, Algorithmen",
        'docs_link_limits': "**[KNOWN_LIMITATIONS.md](https://github.com/quito96/TicketSimulation/blob/master/docs/KNOWN_LIMITATIONS.md)**: Alle 12 Annahmen und ihre Auswirkungen",
        'docs_link_changes': "**[CHANGELOG.md](https://github.com/quito96/TicketSimulation/blob/master/docs/CHANGELOG.md)**: Versionshistorie und Änderungen",

        'section_validation': "🔬 Modell validieren",
        'validation_text': """Um dieses Modell mit Ihren realen Daten zu validieren:
        1. **Ticket-Volumina**: Historische tägliche Zahlen analysieren, Parameter anpassen
        2. **Agenten-Effizienz**: Tickets pro Agent pro Tag messen
        3. **Komplexitätsfaktoren**: Tatsächliche Bearbeitungszeiten nach Level analysieren
        4. **Wartezeiten**: Simulierte mit gemessenen SLA-Metriken vergleichen
        5. **Abwesenheitsquoten**: Tatsächliche Urlaubs-/Krankheitsraten überprüfen""",

        'section_author': "👨‍💻 Über",
        'author_text': "Entwickelt von **Quito96** | [GitHub Repository](https://github.com/quito96/TicketSimulation)",
        'version_text': "Version 2.0.0 - Dezember 2025",
    }
}
