from datetime import datetime

ABS_ZERO = {
    "C": -273.15,
    "F": -459.67,
    "K": 0.0,
}

HISTORY_FILE = "conversion_history.txt"


def convert_temperature(temp: float, from_unit: str, to_unit: str) -> float:
    """Converts temperature between Celsius, Fahrenheit, and Kelvin."""
    if temp < ABS_ZERO[from_unit]:
        raise ValueError(f"Below absolute zero ({ABS_ZERO[from_unit]}° {from_unit})")

    if from_unit == to_unit:
        return temp

    if from_unit == "C":
        return (temp * 9 / 5) + 32 if to_unit == "F" else temp + 273.15
    elif from_unit == "F":
        return (temp - 32) * 5 / 9 if to_unit == "C" else (temp - 32) * 5 / 9 + 273.15
    elif from_unit == "K":
        return temp - 273.15 if to_unit == "C" else (temp - 273.15) * 9 / 5 + 32


def build_ascii_thermometer(temp: float, unit: str) -> str:
    """Returns a fun ASCII thermometer scaled from 0°C (freezing) to 100°C (boiling)."""
    # Normalize to Celsius so the visual scale is consistent
    celsius = convert_temperature(temp, unit, "C")

    # Clamp fill level between 0 and 10 bars
    fill = int(max(0, min(10, round((celsius / 100) * 10))))

    if celsius <= 0:
        label = "FREEZING"
    elif celsius <= 20:
        label = "COOL"
    elif celsius <= 30:
        label = "WARM"
    elif celsius < 100:
        label = "HOT"
    else:
        label = "BOILING"

    lines = ["   .--."]
    for level in range(10, 0, -1):
        bar = "██" if level <= fill else "  "
        marker = f" <- {label}" if level == max(1, fill) else ""
        lines.append(f"  |{bar}|{marker}")
    lines.extend([
        "  |  |",
        " (████)  " + f"{temp:.1f}°{unit}",
        "  `--'",
    ])
    return "\n".join(lines)


def save_to_file(record: str, filename: str = HISTORY_FILE) -> None:
    """Appends a timestamped conversion record to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] {record}\n")

def get_thermometer_visuals(temp: float, unit: str) -> tuple[float, str, str]:
    """
    Returns (fill_ratio, hex_color, status_label) using realistic human-perceived
    color stops (blue <= 0°C, amber at 25°C, orange-red by 35°C-45°C).
    """
    celsius = convert_temperature(temp, unit, "C")

    # Tube fill height still scales from 0°C (freezing) to 100°C (boiling)
    fill_ratio = max(0.0, min(1.0, celsius / 100.0))

    # Realistic thermal color stops: (temp_in_C, (R, G, B))
    stops = [
        (0.0,  (30, 136, 229)),   # Deep Blue (Freezing)
        (15.0, (0, 172, 193)),    # Cyan / Cool
        (25.0, (255, 179, 0)),    # Warm Amber
        (35.0, (244, 81, 30)),    # Hot Orange-Red
        (45.0, (211, 47, 47)),    # Crimson Red (Extreme Heat / Boiling)
    ]

    if celsius <= stops[0][0]:
        r, g, b = stops[0][1]
    elif celsius >= stops[-1][0]:
        r, g, b = stops[-1][1]
    else:
        for i in range(len(stops) - 1):
            t0, c0 = stops[i]
            t1, c1 = stops[i + 1]
            if t0 <= celsius <= t1:
                segment_ratio = (celsius - t0) / (t1 - t0)
                r = int(c0[0] + (c1[0] - c0[0]) * segment_ratio)
                g = int(c0[1] + (c1[1] - c0[1]) * segment_ratio)
                b = int(c0[2] + (c1[2] - c0[2]) * segment_ratio)
                break

    hex_color = f"#{r:02x}{g:02x}{b:02x}"

    if celsius <= 0:
        label = "FREEZING"
    elif celsius <= 18:
        label = "COOL"
    elif celsius <= 28:
        label = "WARM"
    elif celsius < 100:
        label = "HOT"
    else:
        label = "BOILING"

    return fill_ratio, hex_color, label