# Simulation Logic Documentation

This document explains the mathematical model and algorithms behind the ticket system simulation.

## Overview

The simulation models a support ticket system over a configurable time period (default: 60 days). Each day is simulated independently, with the backlog carrying over from the previous day.

## Core Algorithm

The simulation follows this daily cycle:

```
1. Generate inbound tickets (stochastic)
2. Apply automation deflection
3. Calculate available agent capacity
4. Adjust capacity for ticket complexity
5. Process tickets (solve as many as possible)
6. Calculate wait time metrics
7. Update backlog for next day
```

## Detailed Model Components

### 1. Inbound Ticket Generation

**Distribution**: Lognormal

**Why Lognormal?**
- Ensures non-negative values (can't have negative tickets)
- Models realistic right-skewed distributions (most days are average, occasional spikes)
- Represents multiplicative random effects better than normal distribution

**Parameters**:
```python
σ = sqrt(log(1 + volatility²))
μ = log(avg_daily_tickets) - 0.5 × σ²
raw_inbound = Lognormal(μ, σ)
```

**Volatility Interpretation**:
- 10% volatility ≈ ±10% daily variation
- 20% volatility ≈ ±20% daily variation with occasional larger spikes
- 30% volatility ≈ high unpredictability, frequent spikes

### 2. Automation Deflection

Simple percentage reduction:

```
actual_inbound = raw_inbound × (1 - automation_rate)
```

**Example**:
- 100 raw tickets, 10% automation → 90 tickets reach agents

### 3. Agent Availability

#### Model: Pre-Calculated Absence Schedule

Instead of rolling dice for each agent every day, we:

1. Calculate total expected absences over the period:
   ```
   expected_absences = days × vacation_rate × total_agents
   ```

2. Randomly distribute these absences across:
   - All agents (FT and PT)
   - All days in simulation period

3. Each day, check the absence schedule to count available agents

**Example**:
- 5 FT agents, 2 PT agents, 60 days, 5% vacation rate
- Expected absences: 60 × 0.05 × 7 = 21 agent-days
- These 21 absences are randomly distributed across the schedule

**Benefits**:
- More realistic: absences are "planned" rather than random daily coin flips
- Lower variance: total capacity over the period is more predictable
- Matches real-world vacation scheduling

### 4. Capacity Calculation

#### Step 1: Available Hours

```
total_hours = (FT_agents_available × 8) + (PT_agents_available × pt_hours)
```

#### Step 2: Adjust for Complexity

Tickets have different complexity levels, which affect processing time:

| Complexity | Factor | Meaning |
|------------|--------|---------|
| Low        | 1.0    | Baseline (fastest) |
| Medium     | 1.5    | 50% more time |
| High       | 2.5    | 150% more time |

**Note**: These factors are estimated values based on typical support scenarios.

**Weighted Average Complexity**:
```
avg_complexity = (Low% × 1.0) + (Med% × 1.5) + (High% × 2.5)
```

**Example**:
- 50% Low, 30% Medium, 20% High
- avg_complexity = 0.5×1.0 + 0.3×1.5 + 0.2×2.5 = 1.45

#### Step 3: Final Capacity

```
daily_capacity = (total_hours × agent_efficiency) / avg_complexity
```

**Interpretation**:
- `agent_efficiency`: tickets per hour for baseline complexity (1.0)
- Division by complexity adjusts for actual ticket mix

**Example**:
- 40 hours available, 5 tickets/hour efficiency, 1.45 complexity
- Capacity: (40 × 5) / 1.45 = 137.9 tickets

### 5. Ticket Processing

```
total_demand = backlog + actual_inbound
solved = min(total_demand, daily_capacity)
new_backlog = total_demand - solved
```

**Assumptions**:
- Tickets processed in FIFO order (oldest first)
- All tickets arriving today can be processed today if capacity allows
- No prioritization or SLA-based ordering

### 6. Wait Time Calculation

Wait time has two components:

#### A. Queue Wait Time

Time waiting in backlog before agent picks up the ticket:

```
queue_wait_days = backlog / daily_capacity
```

**Example**:
- 200 tickets in backlog, 100 tickets/day capacity
- Queue wait = 2 days

#### B. Processing Time

Time actively working on the ticket:

```
processing_time_hours = (avg_complexity / agent_efficiency) + 0.5
```

Components:
- `avg_complexity / efficiency`: actual work time
- `0.5 hours`: reaction time (time before agent picks up ticket)

**Example**:
- 1.45 complexity, 5 tickets/hour efficiency
- Processing time = (1.45 / 5) + 0.5 = 0.79 hours

#### Total Wait Time

```
total_wait_days = queue_wait_days + (processing_time_hours / 24)
```

### 7. Backlog Update

The backlog carries over to the next day:

```
current_backlog = new_backlog
```

This creates a feedback loop where today's unresolved tickets become tomorrow's backlog.

## Key Metrics

### Average Wait Time

Mean of daily wait time estimates across the simulation period.

**Interpretation**:
- < 4 hours: Excellent
- 4-8 hours: Good (same-day resolution)
- 8-24 hours: Acceptable (next-day resolution)
- \> 24 hours: Backlog building up

### Max Backlog

Maximum number of unresolved tickets at end of any day.

**Interpretation**:
- Indicates worst-case scenario
- If max_backlog grows unbounded → understaffed
- If max_backlog stays near 0 → potential overstaffing

### Clearance Rate

```
clearance_rate = total_solved / total_inbound
```

**Interpretation**:
- 100%: All tickets resolved (sustainable)
- < 100%: Backlog accumulating (unsustainable)
- \> 100%: Clearing historical backlog

## Comparison Mode

When comparing two scenarios (A vs B):

1. **Same Random Seed**: Both scenarios use identical random numbers
   - Same inbound pattern
   - Same absence pattern (but different agents may be absent based on team size)

2. **Fair Comparison**: Differences in metrics are purely due to staffing/efficiency differences

## Stability Analysis

A sustainable configuration should show:

1. **Clearance Rate ≥ 100%** over the simulation period
2. **Backlog Trend**: Stable or decreasing (not exponentially growing)
3. **Wait Time Distribution**: Consistent, not increasing over time

## Model Validation

The model can be validated against real data by:

1. Fitting `avg_daily_tickets` and `volatility` to historical inbound data
2. Calibrating `agent_efficiency` based on observed resolution rates
3. Adjusting `complexity_factors` to match actual processing times
4. Comparing simulated wait times to measured SLA performance

---

## Mathematical Notation Summary

| Symbol | Meaning |
|--------|---------|
| λ | Average daily inbound tickets |
| σ | Volatility (coefficient of variation) |
| α | Automation rate |
| N_FT, N_PT | Number of FT/PT agents |
| h_FT, h_PT | Hours per day for FT/PT |
| ε | Agent efficiency (tickets/hour) |
| c | Complexity factor |
| B_t | Backlog at end of day t |
| W_t | Wait time estimate on day t |

## References

- Lognormal distribution: Used in finance, telecommunications, environmental science for modeling positive-only, right-skewed phenomena
- Queueing theory: M/M/c models for similar service systems
- Capacity planning: Little's Law (L = λW) for steady-state analysis