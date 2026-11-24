from converter import (
    ABS_ZERO,
    build_ascii_thermometer,
    convert_temperature,
    save_to_file,
)


def get_unit(prompt: str) -> str:
    while True:
        unit = input(prompt).strip().upper()
        if unit in ABS_ZERO:
            return unit
        print("Invalid input. Please enter C, F, or K.")


def get_temperature(unit: str) -> float:
    while True:
        try:
            temp = float(input(f"Enter temperature in °{unit}: "))
            if temp < ABS_ZERO[unit]:
                print(f"Cannot be below absolute zero ({ABS_ZERO[unit]}°{unit}).")
                continue
            return temp
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main() -> None:
    session_history: list[str] = []

    while True:
        from_unit = get_unit("\nStarting unit (C, F, or K): ")
        temp = get_temperature(from_unit)
        to_unit = get_unit("Target unit (C, F, or K): ")

        result = convert_temperature(temp, from_unit, to_unit)
        record = f"{temp}°{from_unit} -> {result:.2f}°{to_unit}"

        print(f"\nResult: {record}")
        print(build_ascii_thermometer(result, to_unit))

        # Log to session list and save to file
        session_history.append(record)
        save_to_file(record)

        again = input("\nConvert another temperature? (y/n): ").strip().lower()
        if again != "y":
            break

    # Print all conversions done during this session
    print("\n=== Session Conversion Summary ===")
    for idx, item in enumerate(session_history, start=1):
        print(f"{idx}. {item}")
    print("Saved to conversion_history.txt.")


if __name__ == "__main__":
    main()