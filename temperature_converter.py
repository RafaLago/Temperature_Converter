def get_unit(prompt: str) -> str:
    """Helper function to ask for and validate a temperature unit."""
    while True:
        unit = input(prompt).strip().upper()
        if unit in ("C", "F", "K"):
            return unit
        print("Invalid input. Please enter C, F, or K.")


def get_temperature_input() -> tuple[float, str]:
    """Gets a valid starting unit and physically possible temperature."""
    abs_zero = {
        "C": -273.15,
        "F": -459.67,
        "K": 0.0
    }

    unit = get_unit("Enter the starting unit (C, F, or K): ")

    while True:
        try:
            temperature = float(input("Enter the temperature (e.g., 25, 77, 300): "))
            if temperature < abs_zero[unit]:
                print(f"Temperature cannot be below absolute zero ({abs_zero[unit]}°{unit}). Try again.")
                continue
            return temperature, unit
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
    """Converts temperature between Celsius, Fahrenheit, and Kelvin."""
    if from_unit == to_unit:
        return temp

    if from_unit == "C":
        return (temp * 9/5) + 32 if to_unit == "F" else temp + 273.15
    elif from_unit == "F":
        return (temp - 32) * 5/9 if to_unit == "C" else (temp - 32) * 5/9 + 273.15
    elif from_unit == "K":
        return temp - 273.15 if to_unit == "C" else (temp - 273.15) * 9/5 + 32


# --- Main Execution ---
if __name__ == "__main__":
    # 1. Unpack the returned tuple from get_temperature_input()
    temperature, unit = get_temperature_input()

    # 2. Reuse get_unit() to safely get the target unit
    output_unit = get_unit("Enter the unit you want to convert to (C, F, or K): ")

    # 3. Call convert_temperature() using those exact variables
    converted_temp = convert_temperature(temperature, unit, output_unit)

    # 4. Print the result (:.2f rounds to 2 decimal places)
    print(f"{temperature}° {unit} is equal to {converted_temp:.2f}° {output_unit}.")