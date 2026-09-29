# Swedavia FlightInfo v2 – Reverse Engineering Application

A terminal-based application reverse-engineered from the Swedavia FlightInfo v2 API using Python 3.14, `requests`, and `rich`. The project demonstrates API integration, offline data matching, date/time filtering, OData parameters, and colored terminal rendering.

---

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.14 (or Python 3.10+)
* Dependencies:
  ```bash
  py -3.14 -m pip install requests rich

Running the Application
Launch the main application menu:

py -3.14 airport.py

To run a standalone database test:

py -3.14 destinationer.py

📖 Project Documentation
Phase 1: Research Phase (Pre-study)
Information Gathering: Analyzed the official Swedavia FlightInfo v2 REST API structure (Arrivals and Departures) and evaluated geographical datasets for offline lookup.

Tech Stack: Python 3.14, requests (API client), rich (Terminal UI), and JSON (city_country.json containing 286 cities across 82 countries).

AI Collaboration: Used Google Gemini as a Generative AI thought partner for reverse engineering, pseudocode generation, and architecture design.

Problems & Solutions:

Problem: Unclear API subscription access.

Solution: Constructed an offline mock dataset (MOCK_FLYG) mirroring live API responses for seamless fallback execution.

Phase 2: Implementation Phase (Execution)
Modular Structure: Decoupled business logic and offline matching (destinationer.py) from presentation and networking (airport.py).

Feature Rollout: Developed dataset parsing, API fetching with 5-second timeouts, date/time filtering support, and terminal table rendering.

Problems & Solutions:

Problem: Relative file path errors when executing scripts from different working directories.

Solution: Resolved dynamic paths using os.path.dirname(os.path.abspath(__file__)).

Problem: Missing rich library dependency in execution environment.

Solution: Installed target package via py -3.14 -m pip install rich.

Phase 3: Completion & Refinement Phase
System Integration: Unified features into an interactive terminal menu featuring an automated 1-click demonstration mode (Option 6).

UI Polish: Applied color-coded status badges (🟢 On Time, 🟡 Delayed, 🔴 Cancelled) and clear column layouts using rich.table.Table.

Testing: Validated search filters, OData queries, date selections, and error handling across terminal menu options.

Phase 4: Summary of Key Problems & Solutions
Problem: Network outages or missing API key caused terminal crashes.

Solution: Implemented try-except blocks falling back to offline mock data on status 404/connection loss.

Problem: Raw city names required country mapping.

Solution: Built destinationer.py to match destinations dynamically against city_country.json.

🎓 Conclusion
The project successfully delivers a resilient, visually appealing terminal interface for Swedavia airports. It showcases practical experience in API reverse engineering, robust error handling, modular Python development, and terminal UI design.