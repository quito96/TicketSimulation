# Changelog

All notable changes to the Ticket Simulation project are documented in this file.

## [2.0.0] - 2024-12-05

### Major Improvements - Realistic Simulation

This release focuses on improving the realism and accuracy of the simulation model.

#### Fixed

1. **Vacation/Absence Modeling** (Critical)
   - **Problem**: Used binomial distribution where each agent independently had a vacation_rate chance of being absent each day. This led to unrealistic high variance in absences.
   - **Solution**: Implemented a pre-calculated absence schedule where the total number of absent days matches the vacation_rate over the simulation period, distributed randomly across agents and days.
   - **Impact**: More realistic absence patterns, reduced variance in daily capacity.
   - **Files**: `simulation.py:72-85`

2. **Precision Loss in Results** (Critical)
   - **Problem**: Integer conversion of floating-point values (inbound, solved, backlog) caused cumulative precision loss over 60-day simulations.
   - **Solution**: Maintain float values throughout computation, only round for display (2-3 decimal places).
   - **Impact**: Accurate ticket accounting, no "lost" tickets over time.
   - **Files**: `simulation.py:70, 168-179`

3. **Wait Time Calculation Logic** (Critical)
   - **Problem**: Simplistic calculation that added a fixed 1-hour minimum wait time regardless of actual processing time or complexity.
   - **Solution**: Improved calculation with two components:
     - Queue wait time: `backlog / daily_capacity` (days)
     - Processing time: `(complexity_factor / efficiency) + 0.5 hours reaction time`
   - **Impact**: More accurate and realistic wait time estimates.
   - **Files**: `simulation.py:142-166`

4. **Inbound Ticket Distribution** (High Priority)
   - **Problem**: Normal distribution allows negative values and unrealistic extreme outliers.
   - **Solution**: Replaced with lognormal distribution which ensures non-negative values and realistic right-skewed traffic patterns.
   - **Impact**: More realistic daily ticket volumes, no negative tickets.
   - **Files**: `simulation.py:88-97`

5. **Hardcoded Part-Time Hours in Comparison Page** (Medium Priority)
   - **Problem**: Total staff hours calculation used hardcoded 4 hours for part-time agents instead of the configured value.
   - **Solution**: Added separate `pt_hours` sliders for scenarios A and B, used actual values in calculations.
   - **Impact**: Accurate cost/hours comparison between scenarios.
   - **Files**: `pages/1_⚖️_Comparison.py:63, 72, 86, 100, 134-135`

#### Removed

6. **Non-Functional Seasonality Feature**
   - **Problem**: UI checkbox for seasonality existed but had no effect on simulation.
   - **Solution**: Removed the UI element to avoid user confusion.
   - **Impact**: Cleaner UI, no false expectations.
   - **Files**: `0_🎫_Simulation.py:41`

#### Improved

7. **Documentation and Code Comments**
   - Added comprehensive docstring to `run_simulation()` function explaining all parameters, algorithms, and return values.
   - Added inline comments throughout simulation logic explaining each step.
   - **Files**: `simulation.py:17-60`

### Technical Details

#### Distribution Changes

**Before (Normal Distribution)**:
```python
daily_volatility = np.random.normal(0, volatility)
raw_inbound = avg_daily_tickets * (1 + daily_volatility)
raw_inbound = max(0, raw_inbound)  # Clip negatives
```

**After (Lognormal Distribution)**:
```python
sigma = np.sqrt(np.log(1 + volatility**2))
mu = np.log(avg_daily_tickets) - 0.5 * sigma**2
raw_inbound = np.random.lognormal(mu, sigma)
```

The lognormal parameters are calculated to match the desired mean and coefficient of variation.

#### Absence Modeling Changes

**Before (Binomial)**:
```python
ft_agents_available = np.random.binomial(full_time_agents, 1 - vacation_rate)
```
- Independent daily rolls for each agent
- High variance: 5 agents × 5% = 0-3 absent on any day

**After (Scheduled Absences)**:
```python
expected_absent_days = int(days * vacation_rate * total_agents)
# Distribute absences across agents and days
```
- Total absences match expected rate
- Lower variance: more predictable capacity

### Breaking Changes

None. All changes are backward compatible with existing UI and parameter configurations.

### Known Limitations

See [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md) for detailed discussion of simulation assumptions and limitations.

---

## [1.0.0] - Initial Release

Initial implementation with basic simulation features:
- Day-by-day ticket simulation
- Full-time and part-time agent modeling
- Ticket complexity levels
- Automation deflection
- Bilingual UI (German/English)
- Comparison mode for scenarios