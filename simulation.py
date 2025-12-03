import numpy as np
import pandas as pd

def run_simulation(
    days=30,
    avg_daily_tickets=100,
    volatility=0.2,
    full_time_agents=5,
    part_time_agents=2,
    agent_efficiency=5,  # tickets per hour per agent
    part_time_hours=4,   # hours per day for part-time
    vacation_rate=0.05,
    complexity_mix={'Low': 0.5, 'Medium': 0.3, 'High': 0.2},
    complexity_factors={'Low': 1.0, 'Medium': 1.5, 'High': 2.5},
    automation_rate=0.1
):
    """
    Simulates ticket flow day by day.
    """
    
    # Simulation parameters
    hours_per_day = 8 # Operating hours
    
    dates = pd.date_range(start='2024-01-01', periods=days, freq='D')
    results = []
    
    current_backlog = 0
    
    for date in dates:
        # 1. Inbound Tickets
        # Random variation based on volatility
        daily_volatility = np.random.normal(0, volatility)
        raw_inbound = avg_daily_tickets * (1 + daily_volatility)
        raw_inbound = max(0, raw_inbound) # No negative tickets
        
        # 2. Automation Deflection
        actual_inbound = raw_inbound * (1 - automation_rate)
        
        # 3. Calculate Effective Capacity
        # Full time capacity
        # Randomly decide if agents are on vacation
        ft_agents_available = np.random.binomial(full_time_agents, 1 - vacation_rate)
        pt_agents_available = np.random.binomial(part_time_agents, 1 - vacation_rate)
        
        # Total agent hours available
        total_hours = (ft_agents_available * hours_per_day) + (pt_agents_available * part_time_hours)
        
        # 4. Adjust for Complexity
        # Calculate average "complexity factor" for this day's batch
        # (Simplified: assumes the mix is constant, but could be randomized)
        avg_complexity_factor = (
            complexity_mix['Low'] * complexity_factors['Low'] +
            complexity_mix['Medium'] * complexity_factors['Medium'] +
            complexity_mix['High'] * complexity_factors['High']
        )
        
        # Effective capacity in terms of "Standard Tickets"
        # Efficiency is base tickets/hour for standard complexity (factor 1.0)
        # So actual capacity = (Total Hours * Efficiency) / Avg Complexity Factor
        daily_capacity_tickets = (total_hours * agent_efficiency) / avg_complexity_factor
        
        # 5. Process Tickets
        # Available to solve = Capacity
        # Demand = Backlog + Today's Inbound
        total_demand = current_backlog + actual_inbound
        
        solved = min(total_demand, daily_capacity_tickets)
        new_backlog = total_demand - solved
        
        # 6. Metrics
        # Wait time proxy: Backlog / Daily Capacity (Days to clear)
        # Even if backlog is 0, there is a minimum time to solve a ticket (1 / efficiency)
        # We assume tickets arrive uniformly, so avg wait for same-day solve is roughly half the day or just processing time?
        # Let's add a baseline "Processing Time" = 1 / (Total Daily Capacity / 8 hours) = 1 / (Tickets per Hour)
        # Actually simpler: 1 / agent_efficiency is hours per ticket per agent.
        # Let's say min wait is 0.5 hours (reaction time) + processing time.
        
        queue_wait_days = new_backlog / daily_capacity_tickets if daily_capacity_tickets > 0 else 999
        
        # Min wait (in days) = (1 hour) / 24
        min_wait_days = (1.0 / 24.0) 
        
        est_wait_time_days = queue_wait_days + min_wait_days
        
        results.append({
            'Date': date,
            'Inbound (Raw)': int(raw_inbound),
            'Inbound (Net)': int(actual_inbound),
            'Capacity (Tickets)': int(daily_capacity_tickets),
            'Solved': int(solved),
            'Backlog (End of Day)': int(new_backlog),
            'Est. Wait Time (Days)': round(est_wait_time_days, 2),
            'Est. Wait Time (Hours)': round(est_wait_time_days * 24, 1),
            'Staff Available (FT)': ft_agents_available,
            'Staff Available (PT)': pt_agents_available
        })
        
        current_backlog = new_backlog

    return pd.DataFrame(results)
