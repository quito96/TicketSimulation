# Versioning Methodology

This document defines the versioning strategy for the Ticket Simulation project.

## Semantic Versioning

This project follows **[Semantic Versioning 2.0.0](https://semver.org/)** (SemVer).

Version format: **MAJOR.MINOR.PATCH**

Example: `2.0.0`

---

## Version Number Meaning

### MAJOR version (X.0.0)

Increment when making **incompatible changes** that break backward compatibility:

- **Simulation Algorithm Changes**: Fundamental changes to how the simulation works
  - Example: Switching from discrete to continuous time modeling
  - Example: Changing the core queuing model

- **Breaking API Changes**: Changes that break existing usage
  - Example: Removing or renaming function parameters in `run_simulation()`
  - Example: Changing the structure of returned DataFrame columns

- **Breaking Configuration Changes**: Changes that invalidate existing configurations
  - Example: Removing or renaming UI parameters
  - Example: Changing the meaning of existing parameters (e.g., efficiency unit change)

**Migration Guide Required**: Document how users should update their usage.

---

### MINOR version (0.X.0)

Increment when adding **new functionality** in a backward-compatible manner:

- **New Features**: Adding capabilities without breaking existing ones
  - Example: Adding a new page to the UI (like the Info page in v2.0)
  - Example: Adding new simulation parameters (optional, with defaults)
  - Example: Adding new metrics or visualizations

- **Non-Breaking Improvements**: Enhancements that don't change core behavior
  - Example: Adding new translations/languages
  - Example: Improving UI layout without changing functionality
  - Example: Adding optional export features

- **Deprecations**: Marking features for future removal (still functional)
  - Example: Deprecating a parameter with a warning, but still supporting it

**Backward Compatible**: Existing code/configurations continue to work.

---

### PATCH version (0.0.X)

Increment when making **backward-compatible bug fixes**:

- **Bug Fixes**: Correcting unintended behavior
  - Example: Fixing the precision loss issue (v2.0.0)
  - Example: Fixing hardcoded values (like the part-time hours bug)
  - Example: Correcting calculation errors

- **Documentation Updates**: Fixes to documentation only
  - Example: Correcting typos in CHANGELOG
  - Example: Clarifying docstrings
  - Example: Updating README with better examples

- **Performance Improvements**: Optimizations without behavior changes
  - Example: Making simulations run faster
  - Example: Reducing memory usage

- **Refactoring**: Internal code improvements without external impact
  - Example: Code cleanup
  - Example: Better variable names

**No Functionality Change**: Users should not notice any difference except fixes.

---

## Special Cases

### Pre-release Versions

For alpha/beta/RC releases, append a hyphen and identifier:

- `2.1.0-alpha.1` - Early testing version
- `2.1.0-beta.2` - Feature-complete, testing in progress
- `2.1.0-rc.1` - Release candidate, final testing

**Not recommended for this project** unless planning major overhauls.

### Development Versions

For active development, optionally use `dev`:

- `2.1.0-dev` - Work in progress toward 2.1.0

---

## Decision Matrix

Use this table to decide version bumps:

| Change Type | Example | Version Bump |
|-------------|---------|--------------|
| Add new UI page | Info page | **MINOR** (0.X.0) |
| Fix calculation bug | Precision loss fix | **PATCH** (0.0.X) |
| Change algorithm | Replace binomial with schedule | **MAJOR** if breaks results, **MINOR** if improves |
| Improve wait time calc | Better formula | **MINOR** (better output) or **MAJOR** (breaks comparisons) |
| Add new parameter (optional) | Add seasonality_enabled | **MINOR** (0.X.0) |
| Remove parameter | Delete old parameter | **MAJOR** (X.0.0) |
| Rename parameter | efficiency → agent_speed | **MAJOR** (X.0.0) |
| Add translation | Add French support | **MINOR** (0.X.0) |
| Fix typo in docs | Correct README | **PATCH** (0.0.X) |
| Optimize performance | Faster simulation | **PATCH** (0.0.X) |
| Add new metric | Show P95 wait time | **MINOR** (0.X.0) |

---

## Project-Specific Guidelines

### When in Doubt: Use MINOR

If a change could be either MINOR or PATCH, prefer **MINOR**. This signals users that something improved.

### Model Changes

Changes to the simulation model require careful consideration:

1. **Improvements** (MINOR):
   - Better distributions (normal → lognormal)
   - More realistic modeling (binomial → scheduled absences)
   - New features that enhance accuracy
   - **Condition**: Old configurations still work, results may differ but are "better"

2. **Breaking Changes** (MAJOR):
   - Removing complexity levels
   - Changing parameter meanings
   - Incompatible result formats
   - **Condition**: Old configurations break or produce incompatible results

### UI Changes

- **New pages/features**: MINOR
- **Layout improvements**: PATCH
- **Removing features**: MAJOR
- **Fixing broken features**: PATCH

### Documentation

- Pure documentation updates: **PATCH**
- Documentation for new feature: Include in feature's **MINOR** bump

---

## Changelog Requirements

Every version bump must include:

1. **Entry in CHANGELOG.md**:
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD

   ### Added / Fixed / Changed / Removed / Deprecated

   - Description of change
   - Impact on users
   - Files affected
   ```

2. **Update Version Strings**:
   - `translations.py`: Both EN and DE `version_text`
   - `docs/README.md`: Version History section
   - `docs/CHANGELOG.md`: New version header

3. **Git Tag**:
   ```bash
   git tag -a v2.0.0 -m "Version 2.0.0: Realism improvements"
   git push origin v2.0.0
   ```

---

## Release Process

### 1. Code Freeze
- Complete all planned changes
- Ensure tests pass
- Run smoke tests

### 2. Documentation Update
- Update CHANGELOG.md
- Update version strings
- Review/update README if needed
- Update docs/README.md version history

### 3. Testing
- Run unit tests: `python test_simulation.py`
- Run smoke tests
- Manual UI testing (all three pages)
- Test both languages (DE/EN)

### 4. Version Bump
- Decide version number using rules above
- Update all version strings
- Commit: `git commit -m "Bump version to X.Y.Z"`

### 5. Tag & Release
```bash
git tag -a vX.Y.Z -m "Version X.Y.Z: Brief description"
git push origin vX.Y.Z
```

### 6. GitHub Release
- Create GitHub release from tag
- Copy CHANGELOG entry to release notes
- Upload any artifacts if needed

---

## Examples from Project History

### v2.0.0 (2025-12-05) - MAJOR → MINOR Debate

**What happened**:
- Fixed critical bugs (precision, wait time)
- Improved model realism (lognormal, absences)
- Added Info page

**Decision**: **MAJOR** (2.0.0)

**Reasoning**:
- Model changes produce different results (lognormal vs normal)
- Absence modeling fundamentally changed
- While backward compatible in API, results differ significantly
- Signals to users: "This is a major improvement, review your analyses"

**Alternative View**: Could have been **MINOR** (1.1.0) since API unchanged.

**Conclusion**: For this project, model improvements that significantly change results justify **MAJOR** bumps to alert users.

---

## Future Roadmap Versioning

### Potential v2.1.0 (MINOR)
- Add seasonality support
- Add more complexity levels (Very Low, Very High)
- Add export to CSV/Excel
- Add P50/P95/P99 metrics
- Add shift scheduling (24/7 support)

### Potential v2.0.1 (PATCH)
- Fix UI glitches
- Improve performance
- Documentation corrections
- Translation improvements

### Potential v3.0.0 (MAJOR)
- Change from daily to hourly simulation
- Implement priority queues (breaking: changes all results)
- Remove deprecated parameters
- Restructure DataFrame output columns

---

## Deprecation Policy

When planning to remove a feature:

1. **Version N**: Deprecate with warning
   ```python
   warnings.warn("Parameter 'old_name' is deprecated, use 'new_name'", DeprecationWarning)
   ```
   - Document in CHANGELOG as **Deprecated**
   - MINOR version bump

2. **Version N+1 (at least one MINOR later)**: Keep warning, still functional

3. **Version N+2 or next MAJOR**: Remove completely
   - Document in CHANGELOG as **Removed**
   - MAJOR version bump

**Minimum deprecation period**: One MINOR release cycle.

---

## Summary

- **Follow Semantic Versioning 2.0.0**
- **MAJOR**: Breaking changes, significant model changes
- **MINOR**: New features, improvements, deprecations
- **PATCH**: Bug fixes, docs, performance
- **Always update CHANGELOG.md**
- **Tag releases in Git**
- **When in doubt, bump MINOR not PATCH**

---

## References

- [Semantic Versioning 2.0.0](https://semver.org/)
- [Keep a Changelog](https://keepachangelog.com/)
- [GitHub: Creating releases](https://docs.github.com/en/repositories/releasing-projects-on-github/managing-releases-in-a-repository)
