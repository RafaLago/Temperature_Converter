# Temperature Converter (CLI)

A command-line temperature converter written in Python that converts values between **Celsius (°C)**, **Fahrenheit (°F)**, and **Kelvin (K)** with built-in input validation.

## Features

- **Multi-Scale Conversion:** Supports all conversions between Celsius, Fahrenheit, and Kelvin.
- **Input Type Validation:** Prevents crashes from non-numeric entries using `try / except` handling.
- **Physical Range Checks:** Rejects temperatures below absolute zero for the selected unit (`-273.15 °C`, `-459.67 °F`, or `0 K`).
- **Case-Insensitive Unit Prompts:** Accepts uppercase or lowercase unit inputs (`c`, `f`, `k`) and ignores extra whitespace.

## Requirements

- Python 3.10 or higher (uses standard library only—no external packages required)