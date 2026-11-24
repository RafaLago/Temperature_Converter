# Temperature Converter (CLI & GUI)

A Python temperature converter available as both an interactive **command-line interface (CLI)** and a **Tkinter desktop application**. Converts between **Celsius (°C)**, **Fahrenheit (°F)**, and **Kelvin (K)** with input validation, session tracking, persistent file logging, and ASCII thermometer visuals.

## Features

- **Dual Interfaces:** Run either the terminal app (`cli.py`) or the Tkinter desktop window (`gui.py`).
- **Continuous Session Loop:** Perform multiple conversions in a single run and view a full session summary when exiting.
- **Persistent History Logging:** Automatically saves timestamped conversions to `conversion_history.txt`.
- **ASCII Thermometer:** Displays a visual thermometer scaled from freezing to boiling alongside each result.
- **Input & Physical Validation:** Rejects non-numeric entries and temperatures below absolute zero (`-273.15 °C`, `-459.67 °F`, or `0 K`).

## Requirements

- Python 3.10 or higher (uses standard library only, including `tkinter`—no external packages required)