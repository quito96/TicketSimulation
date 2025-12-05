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
    Simulates ticket flow day by day with realistic modeling.

    This simulation models a support ticket system considering:
    - Stochastic inbound ticket arrivals (lognormal distribution)
    - Variable agent availability (planned absences)
    - Ticket complexity and its impact on processing time
    - Automation deflection
    - Queue-based wait time calculation

    Parameters:
    -----------
    days : int
        Number of days to simulate
    avg_daily_tickets : float
        Average number of tickets arriving per day
    volatility : float
        Daily volatility as a proportion (e.g., 0.2 = 20%). Uses lognormal distribution.
    full_time_agents : int
        Number of full-time agents (8 hours/day)
    part_time_agents : int
        Number of part-time agents
    agent_efficiency : float
        Base tickets per hour per agent (for complexity factor 1.0)
    part_time_hours : float
        Working hours per day for part-time agents
    vacation_rate : float
        Proportion of staff absent on average (e.g., 0.05 = 5%)
    complexity_mix : dict
        Distribution of ticket complexity levels (must sum to 1.0)
    complexity_factors : dict
        Time multiplier for each complexity level (estimated values)
        - Low: 1.0 (baseline)
        - Medium: 1.5 (50% more time)
        - High: 2.5 (150% more time)
    automation_rate : float
        Proportion of tickets deflected by automation (e.g., 0.1 = 10%)

    Returns:
    --------
    pd.DataFrame
        Daily simulation results with columns for inbound, capacity, solved tickets,
        backlog, and estimated wait times.
    """
    
    # Simulation parameters
    hours_per_day = 8  # Operating hours for full-time agents

    # Use current date as start
    start_date = pd.Timestamp.now().normalize()
    dates = pd.date_range(start=start_date, periods=days, freq='D')
    results = []

    current_backlog = 0.0  # Use float to maintain precision

    # Pre-calculate absence schedule for more realistic vacation modeling
    # Instead of binomial per day, we model planned absences more realistically
    # Each agent has a certain number of absent days over the period
    total_agents = full_time_agents + part_time_agents
    expected_absent_days = int(days * vacation_rate * total_agents)

    # Create absence schedule: randomly assign absent days to agents
    absence_schedule = np.zeros((total_agents, days), dtype=bool)
    if expected_absent_days > 0 and total_agents > 0:
        # Randomly distribute absences across agents and days
        for _ in range(expected_absent_days):
            agent_idx = np.random.randint(0, total_agents)
            day_idx = np.random.randint(0, days)
            absence_schedule[agent_idx, day_idx] = True

    for day_idx, date in enumerate(dates):
        # 1. Inbound Tickets
        # Use lognormal distribution for more realistic traffic modeling
        # Lognormal ensures non-negative values and realistic right-skewed distribution
        if volatility > 0:
            # Parameters for lognormal distribution to achieve desired mean and CV
            sigma = np.sqrt(np.log(1 + volatility**2))
            mu = np.log(avg_daily_tickets) - 0.5 * sigma**2
            raw_inbound = np.random.lognormal(mu, sigma)
        else:
            raw_inbound = avg_daily_tickets
        
        # 2. Automation Deflection
        actual_inbound = raw_inbound * (1 - automation_rate)

        # 3. Calculate Effective Capacity
        # Count available agents based on pre-calculated absence schedule
        ft_agents_available = full_time_agents
        pt_agents_available = part_time_agents

        if total_agents > 0:
            # Check absence schedule for this day
            for agent_idx in range(full_time_agents):
                if absence_schedule[agent_idx, day_idx]:
                    ft_agents_available -= 1

            for agent_idx in range(full_time_agents, total_agents):
                if absence_schedule[agent_idx, day_idx]:
                    pt_agents_available -= 1

        # Total agent hours available
        total_hours = (ft_agents_available * hours_per_day) + (pt_agents_available * part_time_hours)
        
        # 4. Adjust for Complexity
        # Calculate weighted average complexity factor
        # This represents how much longer an "average" ticket takes compared to baseline
        avg_complexity_factor = (
            complexity_mix['Low'] * complexity_factors['Low'] +
            complexity_mix['Medium'] * complexity_factors['Medium'] +
            complexity_mix['High'] * complexity_factors['High']
        )

        # Effective capacity in terms of tickets (accounting for complexity)
        # Base capacity: total_hours * agent_efficiency (for complexity factor 1.0)
        # Adjusted for actual complexity: divide by avg_complexity_factor
        daily_capacity_tickets = (total_hours * agent_efficiency) / avg_complexity_factor if avg_complexity_factor > 0 else 0

        # 5. Process Tickets
        # Total demand = backlog from previous days + today's new tickets
        total_demand = current_backlog + actual_inbound

        # Solve as many tickets as capacity allows
        solved = min(total_demand, daily_capacity_tickets)
        new_backlog = total_demand - solved

        # 6. Calculate Wait Time Metrics
        # Wait time has two components:
        # a) Queue wait: time spent waiting in backlog
        # b) Processing time: time to actually resolve the ticket

        # Queue wait time (in days): backlog / daily capacity
        # This represents how many days it would take to clear the current backlog
        if daily_capacity_tickets > 0:
            queue_wait_days = new_backlog / daily_capacity_tickets
        else:
            queue_wait_days = 999  # Infinite wait if no capacity

        # Processing time per ticket (in hours)
        # Average time to process one ticket = (avg_complexity_factor / agent_efficiency)
        # This is the time spent actively working on the ticket
        if agent_efficiency > 0:
            processing_time_hours = avg_complexity_factor / agent_efficiency
        else:
            processing_time_hours = 0

        # Add minimum reaction time (time before agent picks up ticket): 0.5 hours
        reaction_time_hours = 0.5

        # Total estimated wait time
        est_wait_time_days = queue_wait_days + (processing_time_hours + reaction_time_hours) / 24.0
        
        results.append({
            'Date': date,
            'Inbound (Raw)': round(raw_inbound, 2),
            'Inbound (Net)': round(actual_inbound, 2),
            'Capacity (Tickets)': round(daily_capacity_tickets, 2),
            'Solved': round(solved, 2),
            'Backlog (End of Day)': round(new_backlog, 2),
            'Est. Wait Time (Days)': round(est_wait_time_days, 3),
            'Est. Wait Time (Hours)': round(est_wait_time_days * 24, 2),
            'Staff Available (FT)': ft_agents_available,
            'Staff Available (PT)': pt_agents_available
        })
        
        current_backlog = new_backlog

    return pd.DataFrame(results)
