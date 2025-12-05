# Known Limitations and Assumptions

This document outlines the simplifications, assumptions, and limitations of the ticket simulation model.

## Model Assumptions

### 1. Ticket Arrival Patterns

**Assumption**: Tickets arrive according to a lognormal distribution with constant parameters.

**Reality**:
- Ticket volumes may have:
  - Weekly patterns (weekends typically lower)
  - Monthly patterns (end-of-month spikes)
  - Seasonal trends (holidays, product launches)
  - Time-of-day variations (tickets arrive during business hours, not uniformly)

**Impact**:
- Model may underestimate real-world volatility
- Cannot capture predictable patterns like "Monday morning surge"

**Mitigation**: Adjust `volatility` parameter higher to account for these patterns.

---

### 2. Ticket Complexity Distribution

**Assumption**: Complexity distribution is constant throughout the simulation.

**Estimated Factors**:
- Low: 1.0 (baseline)
- Medium: 1.5 (50% more time)
- High: 2.5 (150% more time)

**Reality**:
- Complexity factors are **estimates**, not measured values
- Actual time multipliers may vary by:
  - Agent experience level
  - Available documentation/tools
  - Type of ticket (technical vs. billing vs. how-to)
- Complexity distribution may change over time (e.g., after product updates)

**Impact**:
- Capacity estimates may be off by 10-30%
- Wait time predictions may be optimistic or pessimistic

**Mitigation**: Calibrate factors using historical data if available.

---

### 3. Agent Efficiency

**Assumption**: All agents have the same efficiency (tickets per hour).

**Reality**:
- Experience varies: senior agents may be 2-3× faster than juniors
- Learning curves: new hires take time to ramp up
- Specialization: some agents excel at certain ticket types
- Fatigue effects: efficiency may drop during long shifts

**Impact**:
- Simplified model doesn't capture team composition effects
- Cannot model training/onboarding periods

**Mitigation**: Use weighted average efficiency based on team composition.

---

### 4. Absence Modeling

**Assumption**: Absences are uniformly distributed across agents and days.

**Reality**:
- Vacations are often clustered (summer holidays, end-of-year)
- Sick leave is not uniformly random (flu season, contagion)
- Some agents may take longer vacations than others
- Unplanned absences (emergencies) behave differently than planned ones

**Impact**:
- Model may underestimate variance in extreme scenarios
- Cannot capture "everyone on vacation in August" situations

**Mitigation**: Current model is more realistic than previous binomial approach but still simplified.

---

### 5. Same-Day Processing

**Assumption**: Tickets arriving today can be processed today if capacity allows.

**Reality**:
- Tickets arrive throughout the day
- A ticket arriving at 5 PM may not get same-day service
- Some tickets require multi-day investigation
- Handoffs between shifts may cause delays

**Impact**:
- Wait times may be slightly optimistic
- Model doesn't capture "time of arrival" effects

**Mitigation**: The 0.5-hour reaction time partially accounts for this.

---

### 6. FIFO Processing

**Assumption**: Tickets are processed in First-In-First-Out order.

**Reality**:
- Priority systems: critical issues jump the queue
- SLA-based scheduling: tickets nearing deadline get prioritized
- Agent assignment logic: certain tickets route to specific agents
- Cherry-picking: agents may choose easier tickets first

**Impact**:
- Wait time distribution in reality may differ from simulation
- High-priority tickets wait less, low-priority wait more

**Mitigation**: Model reflects "average" behavior but not priority effects.

---

### 7. No Work-in-Progress Limits

**Assumption**: Agents can work on fractional tickets (e.g., 0.8 tickets/hour).

**Reality**:
- Tickets are discrete units
- An agent can't work on 2.5 tickets simultaneously
- Context switching overhead not modeled
- Some tickets block agents for hours

**Impact**:
- Capacity calculation is simplified
- Doesn't model "one agent stuck on a hard ticket" scenarios

**Mitigation**: Large team sizes average out this effect.

---

### 8. No Escalations or Rework

**Assumption**: Each ticket is solved once and closed.

**Reality**:
- Some tickets get escalated to L2/L3 support
- Customers may reopen tickets
- Solutions may need rework (bugs, incomplete answers)
- Follow-up questions create new tickets

**Impact**:
- Model doesn't capture "ticket churn"
- Actual solved rate may be lower than simulated

**Mitigation**: Adjust `agent_efficiency` downward to account for rework.

---

### 9. Operating Hours

**Assumption**: All work happens within defined operating hours (8 hours/day for FT).

**Reality**:
- 24/7 support operations have shift overlaps
- On-call agents may work outside normal hours
- Automated processes may resolve tickets overnight

**Impact**:
- Model doesn't support 24/7 operations directly
- After-hours work not captured

**Mitigation**: Use PT agents to model additional coverage hours.

---

### 10. Automation Rate is Constant

**Assumption**: Automation deflects a fixed percentage of tickets.

**Reality**:
- Automation improves over time (ML models, better FAQs)
- Automation effectiveness varies by ticket type
- Some complex tickets can't be automated
- Customers may bypass automation ("just give me a human")

**Impact**:
- Long-term capacity planning may be inaccurate
- Cannot model "automation improvement roadmap"

**Mitigation**: Periodically update `automation_rate` parameter.

---

### 11. Independence of Days

**Assumption**: Each day's inbound tickets are independent of previous days.

**Reality**:
- Backlog creates pressure ("we need to catch up")
- Product issues may cause multi-day ticket waves
- Marketing campaigns can create predictable spikes
- Network effects: one ticket may generate follow-ups

**Impact**:
- Model doesn't capture cascading effects
- Cannot simulate "incident response" scenarios

**Mitigation**: Use higher volatility to account for spikes.

---

### 12. Wait Time is Retrospective

**Assumption**: Wait time is calculated based on end-of-day backlog.

**Reality**:
- Customers experience wait time from ticket creation to resolution
- Intra-day dynamics not modeled
- Wait time for a ticket created at 9 AM ≠ ticket created at 4 PM

**Impact**:
- Wait time estimates are averages, not actual customer experience
- Cannot answer "what's the wait time right now?"

**Mitigation**: Treat as planning metric, not real-time indicator.

---

## Validation Recommendations

To validate the model against your real system:

1. **Inbound Traffic**:
   - Plot historical daily ticket volumes
   - Fit lognormal distribution
   - Validate volatility parameter

2. **Agent Efficiency**:
   - Measure tickets resolved per agent per day
   - Calculate average hours per ticket
   - Adjust `agent_efficiency` parameter

3. **Complexity Factors**:
   - Analyze time spent on tickets by complexity level
   - Calculate actual time multipliers
   - Update `complexity_factors` dictionary

4. **Wait Times**:
   - Compare simulated wait times to measured SLA metrics
   - Identify systematic biases (too high/low?)
   - Adjust reaction time and processing time calculations

5. **Absence Rates**:
   - Calculate actual vacation/sick leave utilization
   - Validate `vacation_rate` parameter
   - Check for seasonal patterns

---

## When to Use This Model

**Good for**:
- Strategic capacity planning (months ahead)
- Comparing staffing scenarios
- Sensitivity analysis ("what if we hire 2 more agents?")
- Understanding steady-state behavior

**Not suitable for**:
- Real-time operational decisions
- Detailed SLA compliance analysis
- Modeling specific incident responses
- Sub-hourly predictions

---

## Future Improvements

Potential enhancements to address limitations:

1. **Seasonality**: Add weekly/monthly patterns to inbound traffic
2. **Priority Queues**: Model SLA-based prioritization
3. **Shift Scheduling**: Add time-of-day modeling with multiple shifts
4. **Agent Skill Matrix**: Different agents handle different ticket types
5. **Rework Rate**: Model ticket reopens and escalations
6. **Batch Effects**: Discrete ticket processing instead of continuous
7. **Learning Curves**: New agent efficiency ramp-up over time
8. **Incident Modeling**: Correlated ticket arrivals during outages

---

## Conclusion

This model provides a **useful approximation** for capacity planning and strategic decision-making. It captures the essential dynamics of a ticket system while remaining simple enough to understand and configure.

For critical business decisions, validate the model against historical data and consider the limitations discussed above. When in doubt, run multiple scenarios and examine the range of outcomes.

**Remember**: All models are wrong, but some are useful. This model is useful for planning, not prediction.
