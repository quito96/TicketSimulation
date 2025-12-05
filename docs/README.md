# Documentation Overview

This folder contains technical documentation for the Ticket Simulation project.

## Quick Access

**📱 Want a visual overview?** Check the **Info** page in the running app!
- Start the app: `uv run streamlit run 0_🎫_Simulation.py`
- Navigate to **ℹ️ Info** in the sidebar
- Available in both German and English

---

## Documents

### [CHANGELOG.md](./CHANGELOG.md)
Complete history of changes, bug fixes, and improvements made to the simulation.

**Contents**:
- Version 2.0.0: Major realism improvements
- Detailed explanations of each fix
- Breaking changes (if any)
- Technical implementation details

**Read this to**: Understand what changed and why.

---

### [SIMULATION_LOGIC.md](./SIMULATION_LOGIC.md)
Deep dive into the mathematical model and algorithms.

**Contents**:
- Core algorithm flow
- Mathematical formulas for each component
- Distribution choices (lognormal, etc.)
- Capacity calculation methodology
- Wait time computation
- Key metrics and their interpretation

**Read this to**: Understand how the simulation works under the hood.

---

### [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md)
Honest discussion of model assumptions and limitations.

**Contents**:
- 12 major assumptions and their real-world implications
- When to use (and not use) this model
- Validation recommendations
- Future improvement ideas

**Read this to**: Understand the boundaries of the model and how to interpret results.

---

### [VERSIONING.md](./VERSIONING.md)
Versioning methodology and release process.

**Contents**:
- Semantic Versioning guidelines
- Decision matrix for version bumps
- Release process checklist
- Examples from project history
- Deprecation policy

**Read this to**: Understand how versions are assigned and how to contribute properly.

---

## Quick Reference

### For Users
1. Start with the **Info** page in the app (visual, interactive)
2. Check [CHANGELOG.md](./CHANGELOG.md) to see what's new
3. Review [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md) section "When to Use This Model"

### For Developers
1. Read [SIMULATION_LOGIC.md](./SIMULATION_LOGIC.md) for full algorithm details
2. Study [CHANGELOG.md](./CHANGELOG.md) for recent changes
3. Consult [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md) before adding features

### For Researchers/Validators
1. Start with [SIMULATION_LOGIC.md](./SIMULATION_LOGIC.md) for mathematical foundations
2. Review [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md) for validation recommendations
3. Check [CHANGELOG.md](./CHANGELOG.md) for implementation history

---

## Model Summary

This simulation models a support ticket system with:

- **Stochastic inbound traffic** (lognormal distribution)
- **Multi-level agent staffing** (full-time, part-time)
- **Ticket complexity** (low, medium, high)
- **Automation deflection** (configurable percentage)
- **Realistic absences** (pre-scheduled vacation/sick leave)
- **Queue dynamics** (backlog accumulation and clearing)

**Primary outputs**:
- Average wait time
- Maximum backlog
- Daily capacity vs. demand
- Clearance rate (% of tickets resolved)

---

## Bilingual Support

The user interface supports:
- 🇩🇪 German (Deutsch)
- 🇬🇧 English

All documentation is in English to maintain consistency with standard technical practices.

---

## App Structure

The Streamlit application has three pages:

1. **🎫 Simulation** (main page) - Interactive simulation with parameter controls
2. **⚖️ Comparison** - Side-by-side scenario comparison
3. **ℹ️ Info** - Project information, features, and limitations (NEW!)

---

## Contributing

When adding features or fixing bugs:

1. **Determine version bump** using [VERSIONING.md](./VERSIONING.md) guidelines
2. Update [CHANGELOG.md](./CHANGELOG.md) with your changes
3. Update [SIMULATION_LOGIC.md](./SIMULATION_LOGIC.md) if algorithm changes
4. Add new limitations to [KNOWN_LIMITATIONS.md](./KNOWN_LIMITATIONS.md) if applicable
5. Update the **Info** page translations if user-facing features change
6. Document your changes in code comments
7. Update docstrings for any modified functions
8. Follow the release process in [VERSIONING.md](./VERSIONING.md)

---

## Version History

- **v2.0.0** (2025-12-05): Realism improvements + Info page
  - Lognormal distribution for inbound
  - Improved absence modeling
  - Fixed precision loss
  - Enhanced wait time calculation
  - NEW: Info page with bilingual support

- **v1.0.0**: Initial release
  - Basic simulation engine
  - Bilingual UI
  - Comparison mode

---

## Contact

For questions about the simulation model or documentation, please refer to the main project README.md or open an issue on the [GitHub repository](https://github.com/quito96/TicketSimulation).
