# Swedavia FlightInfo v2 – Reverse Engineering & Application Documentation

## Phase 1: Research Phase (Pre-study)

### What is Included
* **Information Gathering:** Analyzed the official Swedavia FlightInfo v2 REST API structure (Arrivals and Departures endpoints) and evaluated geographical datasets to build an offline lookup table.
* **Selection of Tools & Technologies:**
  * **Language:** Python 3.14
  * **HTTP Client:** `requests` (for REST API communication)
  * **UI Framework:** `rich` (for terminal rendering, tables, and colored status indicators)
  * **Data Storage:** JSON (`city_country.json` containing 286 cities across 82 countries)
  * **AI Collaborator:** Google Gemini (used as a thought partner for reverse engineering, pseudocode generation, and architecture design)
* **Execution Plan:** Followed the instructor's 6-step Reverse Engineering framework (Look, Ask, Guess Inputs, Guess Process, Sketch, Build) to reverse-engineer and recreate the terminal application.

### Problems & Solutions
* **Problem:** Unclear requirements regarding API access and live endpoints (lack of a active API subscription key).
  * **Solution:** Defined a clear fallback strategy by constructing a mock dataset (`MOCK_FLYG`) that mirrors the live Swedavia API structure, allowing seamless offline execution.
* **Problem:** Difficulty matching raw IATA airport/city names to full country names.
  * **Solution:** Created a standalone local lookup database (`city_country.json`) and built helper functions to perform automated data matching.

---

## Phase 2: Implementation Phase (Execution)

### What is Included
* **Project Initialization:** Set up a clean modular directory structure separating database logic (`destinationer.py`) from interface and API handling (`airport.py`).
* **Core Components Developed First:**
  1. `city_country.json`: Populated with 286 city-to-country pairs.
  2. `destinationer.py`: Developed the database loading (`ladda_city_country_db`) and destination analysis (`analysera_destinationer`) functions.
  3. `airport.py`: Implemented API fetching with timeout handling, date/time filtering support, OData query execution, and terminal UI rendering via `rich.table.Table`.
* **Feature Evolution:** Added support for query date/time endpoints and visual status indicators (🟢 On Time, 🟡 Delayed, 🔴 Cancelled).

### Problems & Solutions
* **Problem:** Relative file paths caused `FileNotFoundError` when executing `destinationer.py` or `airport.py` from different working directories.
  * **Solution:** Refactored file loading using `os.path.dirname(os.path.abspath(__file__))` to guarantee robust dynamic path resolution.
* **Problem:** Missing external library dependencies (`rich` module not found during initial execution).
  * **Solution:** Identified python environment mismatch and installed the required package via `py -3.14 -m pip install rich`.
* **Problem:** API calls failed or hung when no network or API key was available.
  * **Solution:** Wrapped API HTTP requests in `try-except` blocks with a 5-second timeout, falling back gracefully to offline mock data on status 404 or connection failures.

---

## Phase 3: Completion & Refinement Phase

### What is Included
* **Project Finalization:** Unified all components into a seamless interactive terminal menu with a 1-click automated demonstration mode (Option 6).
* **System Testing:** Verified all menu options (1–6) across offline mock modes, date inputs, search filters, and terminal table rendering.
* **Refinement & Optimization:** Enhanced table visual hierarchy using custom column styles, magenta bold headers, and color-coded status badges.
* **Presentation Readiness:** Documented the full reverse engineering workflow across `README.md`, `förklaring.md`, and `DOCUMENTATION.md`.

### Problems & Solutions
* **Problem:** API response time variations caused potential terminal freezing during bad network conditions.
  * **Solution:** Implemented a strict 5-second HTTP timeout parameter in `requests.get()`.
* **Problem:** Inconsistent date formatting between API responses and display outputs.
  * **Solution:** Sanitized ISO timestamp strings (replacing "T" and "Z" delimiters) to display clean UTC timestamps (`YYYY-MM-DD HH:MM`).

---

## Phase 4: Summary of Key Problems & Solutions

* **Problem 1: Missing API Credentials / Offline Environment**
  * **Solution:** Built an automatic mock fallback mechanism (`MOCK_FLYG`) that activates when API key validation fails (Status 404/500) or during network outages.
* **Problem 2: Unstructured Data & City Identification**
  * **Solution:** Built `destinationer.py` to parse flight responses and automatically join destination names against `city_country.json`.
* **Problem 3: Monolithic Code & Scalability Issues**
  * **Solution:** Decoupled business logic into modular components: dataset handling (`destinationer.py`) vs. presentation & networking (`airport.py`).

---

## Conclusion

### What Was Achieved
A fully functional, resilient, and visually appealing terminal-based flight information system for Swedavia airports. The application supports live/offline data switching, OData date/time parameters, flight searches, and color-coded status updates.

### What Was Learned
* Deep understanding of Reverse Engineering methodology using AI tools (Google Gemini).
* Hands-on experience with REST API integration, error handling, and offline fallback strategies.
* Mastery of Python terminal UI styling using `rich` and modular code architecture.

### Future Improvements
* Add export features to save generated flight tables to local text or JSON report files.
* Implement statistical charts displaying top destination countries per airport.