
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import requests
from datetime import datetime, timedelta

import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load and play the music
pygame.mixer.music.load('Pufino - Thoughtful (freetouse.com).mp3')
pygame.mixer.music.play(-1)  # Use -1 to loop the sound infinitely



# Replace with your actual API key
API_KEY = "fca_live_GdR82iAVj8ureJfnvmKEcGr2RQhJubKUfqux9Oco"
BASE_URL = "https://api.freecurrencyapi.com/v1/"

class CurrencyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Currency Converter")
        self.root.geometry("800x800")
        self.root.configure(bg="#f5f5f5")

        # Header
        header = tk.Label(
            root, text="Currency Converter", font=("Helvetica", 24, "bold"), bg="#4682b4", fg="white"
        )
        header.pack(fill=tk.X, pady=10)

        # Frames
        self.main_frame = ttk.Frame(root, padding=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Input Frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Input", padding=10)
        self.input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Output Frame
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Output", padding=10)
        self.output_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Historical Rates Frame
        self.historical_frame = ttk.LabelFrame(self.main_frame, text="Historical Rates", padding=10)
        self.historical_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        # Add weights for resizing
        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Base Currency Dropdown
        ttk.Label(self.input_frame, text="Base Currency:", font=("Helvetica", 14)).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        self.base_currency_var = tk.StringVar()
        self.base_currency_dropdown = ttk.Combobox(self.input_frame, textvariable=self.base_currency_var, font=("Helvetica", 14))
        self.base_currency_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Target Currency Dropdown
        ttk.Label(self.input_frame, text="Target Currency:", font=("Helvetica", 14)).grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        self.target_currency_var = tk.StringVar()
        self.target_currency_dropdown = ttk.Combobox(self.input_frame, textvariable=self.target_currency_var, font=("Helvetica", 14))
        self.target_currency_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Amount
        ttk.Label(self.input_frame, text="Amount:", font=("Helvetica", 14)).grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        self.amount_entry = ttk.Entry(self.input_frame, font=("Helvetica", 14))
        self.amount_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Buttons
        self.convert_button = tk.Button(
            self.input_frame,
            text="Convert",
            font=("Helvetica", 14),
            bg="#4682b4",
            fg="white",
            command=self.convert_currency,
        )
        self.convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.swap_button = tk.Button(
            self.input_frame,
            text="Swap",
            font=("Helvetica", 14),
            bg="#32cd32",
            fg="white",
            command=self.swap_currencies,
        )
        self.swap_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.clear_button = tk.Button(
            self.input_frame,
            text="Clear",
            font=("Helvetica", 14),
            bg="#ff6347",
            fg="white",
            command=self.clear_inputs,
        )
        self.clear_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.result_label = tk.Label(self.output_frame, text="", font=("Helvetica", 14), bg="white", anchor="w", justify="left")
        self.result_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.historical_button = tk.Button(
            self.historical_frame,
            text="View Historical Rates",
            font=("Helvetica", 14),
            bg="#4682b4",
            fg="white",
            command=self.view_historical_data,
        )
        self.historical_button.pack(fill=tk.X, padx=10, pady=10)

        self.historical_result = tk.Text(self.historical_frame, wrap=tk.WORD, height=10)
        self.historical_result.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Fetch available currencies
        self.available_currencies = self.get_available_currencies()
        self.base_currency_dropdown['values'] = self.available_currencies
        self.target_currency_dropdown['values'] = self.available_currencies

    def get_available_currencies(self):
        """Fetches all available currencies from the API."""
        url = f"{BASE_URL}currencies"
        params = {"apikey": API_KEY}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return list(response.json()["data"].keys())
        messagebox.showerror("Error", "Unable to fetch available currencies.")
        return []

    def convert_currency(self):
        """Converts the currency based on the provided inputs."""
        base_currency = self.base_currency_var.get().upper()
        target_currency = self.target_currency_var.get().upper()
        try:
            amount = float(self.amount_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.")
            return
        rate = self.get_exchange_rate(base_currency, target_currency)
        if rate:
            result = amount * rate
            self.result_label.config(
                text=f"{amount:.2f} {base_currency} = {result:.2f} {target_currency}"
            )
        else:
            self.result_label.config(text="Exchange rate not available.")

    def get_exchange_rate(self, base_currency, target_currency):
        """Fetches the exchange rate for the given currencies."""
        url = f"{BASE_URL}latest"
        params = {"apikey": API_KEY, "base_currency": base_currency, "currencies": target_currency}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            rates = response.json()["data"]
            return rates.get(target_currency, None)
        messagebox.showerror("Error", "Unable to fetch exchange rate.")
        return None

    def swap_currencies(self):
        """Swaps the values of the base and target currency dropdowns."""
        base = self.base_currency_var.get()
        target = self.target_currency_var.get()
        self.base_currency_var.set(target)
        self.target_currency_var.set(base)

    def clear_inputs(self):
        """Clears all inputs and outputs."""
        self.base_currency_var.set("")
        self.target_currency_var.set("")
        self.amount_entry.delete(0, tk.END)
        self.result_label.config(text="")
        self.historical_result.delete(1.0, tk.END)

    def view_historical_data(self):
        """Fetches and displays historical exchange rates for the last 30 days."""
        base_currency = self.base_currency_var.get().upper()
        target_currency = self.target_currency_var.get().upper()
        if not base_currency or not target_currency:
            messagebox.showerror("Input Error", "Please select both currencies.")
            return

        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        url = f"{BASE_URL}historical"
        params = {
            "apikey": API_KEY,
            "base_currency": base_currency,
            "symbols": target_currency,
            "start_date": start_date,
            "end_date": end_date,
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            historical_data = response.json()["data"]
            result_text = f"Rates from {start_date} to {end_date}:\n"
            for date, rates in historical_data.items():
                rate = rates.get(target_currency, "N/A")
                result_text += f"{date}: 1 {base_currency} = {rate} {target_currency}\n"
            self.historical_result.delete(1.0, tk.END)
            self.historical_result.insert(tk.END, result_text)
        else:
            messagebox.showerror("Error", "Unable to fetch historical rates.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CurrencyApp(root)
    root.mainloop()
