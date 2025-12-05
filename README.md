# Ticket System Simulation

A graphical simulation of a ticket system's resolution time, built with **Python** and **Streamlit**. This tool allows you to visualize how factors like staffing, inbound traffic, and ticket complexity affect key performance indicators (KPIs) such as resolution time and backlog size.

## Features

-   **Interactive Simulation**: Adjust parameters in real-time using sidebar sliders.
-   **Comprehensive Factors**:
    -   **Staffing**: Configure full-time/part-time agents, efficiency, and absenteeism.
    -   **Inbound Traffic**: Set daily volume and volatility.
    -   **Ticket Properties**: Define complexity distribution (Low/Medium/High) and automation rates.
-   **Visualizations**:
    -   **The Pulse**: Line chart showing Net Inbound, Capacity, and Backlog over time.
    -   **KPI Dashboard**: Average Wait Time, Max Backlog, Total Solved, Clearance Rate.
    -   **Distributions**: Histograms for wait times and stacked bars for staff availability.

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for fast package management.

1.  **Install uv** (if not already installed):
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

2.  **Clone the repository** (or navigate to the project directory).

3.  **Install dependencies**:
    ```bash
    uv sync
    ```
    Or manually:
    ```bash
    uv add streamlit pandas numpy plotly watchdog
    ```

## Usage

1.  **Run the Application**:
    ```bash
    uv run streamlit run 0_🎫_Simulation.py
    ```

2.  **Interact with the App**:
    -   Open the URL provided in the terminal (usually `http://localhost:8501`).
    -   Use the **Sidebar** on the left to change simulation parameters.
    -   The charts and KPIs will update automatically.

## Simulation Logic

The simulation runs a day-by-day model:
1.  **Inbound**: Generates new tickets based on the average daily volume and volatility (lognormal distribution).
2.  **Capacity**: Calculates total agent hours (Full-time + Part-time) minus vacation/sick time (pre-scheduled absences).
3.  **Throughput**: Converts agent hours into "ticket solving capacity" based on efficiency and ticket complexity.
4.  **Queue**: Unsolved tickets carry over to the next day's backlog.

**📚 For detailed technical documentation**, see:
- [docs/SIMULATION_LOGIC.md](./docs/SIMULATION_LOGIC.md) - Mathematical model and algorithms
- [docs/KNOWN_LIMITATIONS.md](./docs/KNOWN_LIMITATIONS.md) - Assumptions and limitations
- [docs/CHANGELOG.md](./docs/CHANGELOG.md) - Version history and changes

## Development

To run tests:
```bash
uv run python test_simulation.py
```

## License

This project is licensed under the MIT License.

## Author

Programmed by **Quito96**.
Original Repository: [https://github.com/quito96/TicketSimulation.git](https://github.com/quito96/TicketSimulation.git)
