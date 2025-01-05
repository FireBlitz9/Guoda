import tkinter as tk
from tkinter import scrolledtext
import math
import difflib

CONFIG_FILE = "config.json"

item_prices = {
    "pro-flash": 25,
    "flashli": 15,
    "shov": 30,
    "lockpi": 20,
    "stun gre": 40,
    "boombox": 60,
    "tzp in": 120,
    "zap gun": 400,
    "extens": 60,
    "ladder": 60,
    "radar bo": 50,
    "cozy lights": 140,
    "green suit": 60,
    "hazard suit": 90,
    "pajama suit": 900,
    "bee suit": 110,
    "bunny suit": 200,
    "goldfish": 50,
    "jack o lantern": 50,
    "television": 130,
    "record player": 120,
    "romantic table": 120,
    "shower": 180,
    "table": 70,
    "toilet": 150,
    "welcome mat": 40,
    "plushie pajama man": 100,
    "disco ball": 150,
    "teleport": 375,
    "inverse": 425,
    "loud horn": 100,
    "signal tra": 255,
    "embrion": 150,
    "rend": 550,
    "dine": 600,
    "titan": 700,
    "artifice": 1500
}

version_item_prices = {
    "v50": {"cruiser": 0, "jetpack": 700, "weed ki": 0},
    "v56": {"cruiser": 370, "jetpack": 900, "weed ki": 40},
    "v68": {"cruiser": 370, "jetpack": 900, "weed ki": 25},
}

def reset_target_balance():
    target_money_entry.delete(0, tk.END)
    target_money_entry.insert(0, "0")

def update_item_prices(version):
    reset_target_balance()
    item_prices.update(version_item_prices.get(version, {}))
    calculate_target_balance()

def calculate_target_balance():
    reset_target_balance()
    text = item_codes_text.get("1.0", tk.END)
    lines = text.splitlines()

    total_cost = 0
    for line in lines:
        parts = line.split()
        if not parts:
            continue

        item_code = parts[0].lower()
        quantity = int(parts[1]) if len(parts) > 1 else 1

        combined_prices = {**item_prices, **version_item_prices.get(dropdown_var.get(), {})}

        closest_match = difflib.get_close_matches(item_code, list(combined_prices.keys()), n=1, cutoff=0.31)
        if closest_match:
            matched_item = closest_match[0]
            total_cost += combined_prices.get(matched_item, 0) * quantity
        else:
            print(f"Item '{item_code}' not recognized, skipping.")

    current_target_balance = int(target_money_entry.get()) if target_money_entry.get() else 0
    new_target_balance = current_target_balance + total_cost
    target_money_entry.delete(0, tk.END)
    target_money_entry.insert(0, str(new_target_balance))

def calculate():
    try:
        target_money = int(target_money_entry.get())
        quota = int(quota_entry.get())
        money_from_previous = int(money_from_previous_entry.get())
    except ValueError:
        result_label.config(text="Please fill all fields.")
        return

    F76 = target_money
    if F76:
        if quota < (F76 - 5 * 15):
            scrap_sell = math.ceil((5 * (F76 - money_from_previous + 15) + quota) / 6)
        else:
            scrap_sell = max(F76 - money_from_previous, quota)

    overtime_bonus = round(max(((scrap_sell - quota) / 5) - 15, 0)) if scrap_sell > quota else 0

    result_text = (
        f"Target Balance: ${target_money}        Sell Scrap: ${scrap_sell}\n"
        f"Quota: ${quota}                          Overtime: ${overtime_bonus}\n"
    )

    result_label.config(text=result_text)

    target_money_entry.delete(0, tk.END)
    target_money_entry.insert(0, "0")

is_calculator_visible = False  # Track the calculator's visibility

def toggle_calculator():
    global is_calculator_visible
    if is_calculator_visible:
        root.geometry("500x300")  # Shrink window to original size
        calculator_frame.grid_remove()  # Hide calculator
        toggle_button.config(text="% >")
    else:
        root.geometry("800x300")  # Expand window to fit calculator
        calculator_frame.grid()  # Show calculator
        toggle_button.config(text="% <")
    is_calculator_visible = not is_calculator_visible

def append_to_expression(char):
    calculator_display.insert(tk.END, char)

def clear_expression():
    calculator_display.delete(0, tk.END)

def evaluate_expression():
    try:
        # Replace GUI symbols with Python equivalents
        expression = calculator_display.get().replace("÷", "/").replace("x", "*")
        result = eval(expression)  # Evaluate the modified expression
        calculator_display.delete(0, tk.END)
        calculator_display.insert(tk.END, str(result))
    except Exception:
        calculator_display.delete(0, tk.END)
        calculator_display.insert(tk.END, "Error")

# GUI setup
root = tk.Tk()
root.title("High Guoda Sell Calc")
root.geometry("500x300")
root.configure(bg="#FFFAF0")
root.resizable(False, False)

calc_frame = tk.Frame(root, bg="#FFFAF0")
calc_frame.grid(row=0, column=0, padx=10, pady=10)

item_codes_frame = tk.Frame(root, bg="#FFFAF0")
item_codes_frame.grid(row=0, column=0, padx=10, pady=10)

dropdown_values = ["v56", "v50", "v68"]
dropdown_var = tk.StringVar(value=dropdown_values[0])
dropdown_menu = tk.OptionMenu(item_codes_frame, dropdown_var, *dropdown_values, command=update_item_prices)
dropdown_menu.config(font=("Helvetica", 10), bg="#FF6F00", fg="white")
dropdown_menu.grid(row=0, column=0, pady=5, padx=10, sticky="ne")

item_codes_label = tk.Label(item_codes_frame, text="Item Codes:", font=("Helvetica", 10), bg="#FFFAF0", fg="#FF6F00")
item_codes_label.grid(row=1, column=0, padx=10, pady=5)

item_codes_text = scrolledtext.ScrolledText(item_codes_frame, font=("Helvetica", 10), wrap=tk.WORD, height=10, width=20)
item_codes_text.grid(row=2, column=0, padx=10, pady=5)

apply_button = tk.Button(item_codes_frame, text="Apply", font=("Helvetica", 10), bg="#FF6F00", fg="white", command=calculate_target_balance)
apply_button.grid(row=3, column=0, pady=5, padx=10, sticky="ne")

sell_frame = tk.Frame(root, bg="#FFFAF0")
sell_frame.grid(row=0, column=2, padx=10, pady=10)

quota_label = tk.Label(sell_frame, text="Quota:", font=("Helvetica", 10), bg="#FFFAF0", fg="#FF6F00")
quota_label.grid(row=0, column=0, padx=10, pady=5)

quota_entry = tk.Entry(sell_frame, font=("Helvetica", 10))
quota_entry.grid(row=0, column=1, padx=10, pady=5)
quota_entry.insert(0, "130")

money_from_previous_label = tk.Label(sell_frame, text="Current Balance:", font=("Helvetica", 10), bg="#FFFAF0", fg="#FF6F00")
money_from_previous_label.grid(row=1, column=0, padx=10, pady=5)

money_from_previous_entry = tk.Entry(sell_frame, font=("Helvetica", 10))
money_from_previous_entry.grid(row=1, column=1, padx=10, pady=5)
money_from_previous_entry.insert(0, "0")

target_money_label = tk.Label(sell_frame, text="Target Balance:", font=("Helvetica", 10), bg="#FFFAF0", fg="#FF6F00")
target_money_label.grid(row=2, column=0, padx=10, pady=5)

target_money_entry = tk.Entry(sell_frame, font=("Helvetica", 10))
target_money_entry.grid(row=2, column=1, padx=10, pady=5)
target_money_entry.insert(0, "0")

calculate_button = tk.Button(sell_frame, text="Calculate", font=("Helvetica", 10), bg="#FF6F00", fg="white", command=calculate)
calculate_button.grid(row=3, column=0, pady=5, padx=10, columnspan=2)

result_label = tk.Label(sell_frame, text="", font=("Helvetica", 10), bg="#FFFAF0", fg="#FF6F00")
result_label.grid(row=4, column=0, columnspan=2, pady=10)

toggle_button = tk.Button(root, text="% >", font=("Helvetica", 10), bg="#FF6F00", fg="white", command=toggle_calculator)
toggle_button.place(x=450, y=257)  # Fixed position


# Numeral calculator frame
calculator_frame = tk.Frame(root, bg="#FFFAF0")
calculator_frame.grid(row=0, column=3, padx=10, pady=10)
calculator_frame.grid_remove()  # Initially hidden

calculator_display = tk.Entry(calculator_frame, font=("Helvetica", 12), justify="right", bd=2, relief="ridge")
calculator_display.grid(row=0, column=0, columnspan=4, pady=5)

buttons = [
    ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("÷", 1, 3),
    ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("x", 2, 3),
    ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
    ("0", 4, 1), ("C", 4, 0), ("=", 4, 2), ("+", 4, 3)
]

# Same button styling as the rest of the buttons
button_style = {"font": ("Helvetica", 12), "width": 5, "height": 2, "bg": "#FF6F00", "fg": "white"}

for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(calculator_frame, text=text, **button_style, command=evaluate_expression)
    elif text == "C":
        button = tk.Button(calculator_frame, text=text, **button_style, command=clear_expression)
    else:
        button = tk.Button(calculator_frame, text=text, **button_style, command=lambda t=text: append_to_expression(t))
    button.grid(row=row, column=col, padx=5, pady=5)


root.mainloop()