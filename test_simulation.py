import unittest
import pandas as pd
from simulation import run_simulation

class TestSimulation(unittest.TestCase):
    def test_simulation_runs(self):
        """Test that the simulation returns a DataFrame with expected columns."""
        df = run_simulation(days=10)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 10)
        expected_cols = ['Date', 'Inbound (Raw)', 'Backlog (End of Day)']
        for col in expected_cols:
            self.assertIn(col, df.columns)

    def test_zero_staff_builds_backlog(self):
        """Test that 0 staff results in backlog accumulation equal to inbound."""
        df = run_simulation(
            days=5,
            avg_daily_tickets=100,
            volatility=0,
            full_time_agents=0,
            part_time_agents=0,
            automation_rate=0
        )
        # Total inbound should equal backlog at the end (since 0 solved)
        total_inbound = df['Inbound (Net)'].sum()
        last_backlog = df['Backlog (End of Day)'].iloc[-1]
        self.assertEqual(total_inbound, last_backlog)
        self.assertEqual(df['Solved'].sum(), 0)

    def test_high_capacity_clears_queue(self):
        """Test that massive capacity keeps backlog at 0."""
        df = run_simulation(
            days=5,
            avg_daily_tickets=10,
            full_time_agents=100, # Massive capacity
            agent_efficiency=10
        )
        self.assertTrue((df['Backlog (End of Day)'] == 0).all())

if __name__ == '__main__':
    unittest.main()
