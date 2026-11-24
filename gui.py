import tkinter as tk
from tkinter import messagebox, ttk

from converter import convert_temperature, get_thermometer_visuals, save_to_file


class TemperatureConverterApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Temperature Converter")
        self.root.geometry("380x480")
        self.root.resizable(False, False)
        self.session_history: list[str] = []

        # --- Input Frame ---
        input_frame = ttk.Frame(root, padding=15)
        input_frame.pack(fill="x")

        ttk.Label(input_frame, text="Temperature:").grid(row=0, column=0, sticky="w")
        self.temp_entry = ttk.Entry(input_frame, width=15)
        self.temp_entry.grid(row=0, column=1, padx=5, pady=5)
        self.temp_entry.focus()

        ttk.Label(input_frame, text="From:").grid(row=1, column=0, sticky="w")
        self.from_unit = ttk.Combobox(input_frame, values=["C", "F", "K"], state="readonly", width=12)
        self.from_unit.set("C")
        self.from_unit.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="To:").grid(row=2, column=0, sticky="w")
        self.to_unit = ttk.Combobox(input_frame, values=["C", "F", "K"], state="readonly", width=12)
        self.to_unit.set("F")
        self.to_unit.grid(row=2, column=1, padx=5, pady=5)

        convert_btn = ttk.Button(input_frame, text="Convert", command=self.handle_convert)
        convert_btn.grid(row=3, column=0, columnspan=2, pady=10, sticky="ew")

        # --- Result Label ---
        self.result_var = tk.StringVar(value="Enter a value and click Convert")
        ttk.Label(root, textvariable=self.result_var, font=("Segoe UI", 11, "bold")).pack(pady=(0, 5))

        # --- Graphical Thermometer Canvas ---
        self.canvas = tk.Canvas(root, width=260, height=250, bg="#f8f9fa", highlightthickness=1, highlightbackground="#dcdcdc")
        self.canvas.pack(pady=5)
        self.draw_thermometer(ratio=0.25, color="#4976c6", status="READY", display_text="--")

        # Bind Enter key and window close summary
        self.root.bind("<Return>", lambda _: self.handle_convert())
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def draw_thermometer(self, ratio: float, color: str, status: str, display_text: str) -> None:
        """Draws a colored thermometer on the Tkinter Canvas."""
        self.canvas.delete("all")

        # Tube coordinates
        tube_left, tube_right = 85, 105
        tube_top, tube_bottom = 30, 185

        # 1. Outer glass tube & bulb outline
        self.canvas.create_rectangle(tube_left, tube_top, tube_right, tube_bottom, outline="#555555", width=2, fill="#ffffff")
        self.canvas.create_oval(73, 175, 117, 219, outline="#555555", width=2, fill=color)

        # 2. Inner colored liquid column (rises from bottom to top based on ratio)
        fill_height = (tube_bottom - tube_top) * ratio
        liquid_top = tube_bottom - fill_height
        if fill_height > 0:
            self.canvas.create_rectangle(
                tube_left + 2, liquid_top, tube_right - 2, tube_bottom + 2, outline="", fill=color
            )

        # Hide seam between tube and bulb
        self.canvas.create_oval(75, 177, 115, 217, outline="", fill=color)

        # 3. Scale tick marks (0°C, 50°C, 100°C reference)
        ticks = [(tube_bottom, "0°C (Freezing)"), ((tube_top + tube_bottom) / 2, "50°C"), (tube_top, "100°C (Boiling)")]
        for y_pos, label in ticks:
            self.canvas.create_line(tube_right + 4, y_pos, tube_right + 12, y_pos, fill="#666666", width=1.5)
            self.canvas.create_text(tube_right + 16, y_pos, text=label, anchor="w", font=("Segoe UI", 8), fill="#555555")

        # 4. Status badge & converted temperature readout
        self.canvas.create_text(130, 234, text=f"{display_text}  •  {status}", font=("Segoe UI", 10, "bold"), fill=color)

    def handle_convert(self) -> None:
        try:
            temp = float(self.temp_entry.get())
            f_unit = self.from_unit.get()
            t_unit = self.to_unit.get()

            result = convert_temperature(temp, f_unit, t_unit)
            record = f"{temp}°{f_unit} -> {result:.2f}°{t_unit}"

            self.result_var.set(record)
            self.session_history.append(record)
            save_to_file(record)

            # Update colored thermometer
            ratio, color, status = get_thermometer_visuals(result, t_unit)
            self.draw_thermometer(ratio, color, status, f"{result:.1f}°{t_unit}")

        except ValueError as err:
            messagebox.showerror("Invalid Input", f"Please enter a valid temperature.\n({err})")

    def on_close(self) -> None:
        if self.session_history:
            summary = "\n".join(f"{i}. {item}" for i, item in enumerate(self.session_history, 1))
            messagebox.showinfo("Session Summary", f"Conversions this session:\n\n{summary}")
        self.root.destroy()


if __name__ == "__main__":
    window = tk.Tk()
    TemperatureConverterApp(window)
    window.mainloop()