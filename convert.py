import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk  # For Managing images
import requests
from datetime import datetime, timedelta
import pygame

#  pygame mixer
pygame.mixer.init()

# Load and play the music
pygame.mixer.music.load('Pufino - Thoughtful (freetouse.com).mp3')
pygame.mixer.music.play(-1)  # Using library  -1 to loop the sound infinitely

# Replace the API key 
API_KEY = "fca_live_GdR82iAVj8ureJfnvmKEcGr2RQhJubKUfqux9Oco"
BASE_URL = "https://api.freecurrencyapi.com/v1/"

class CurrencyApp:
    def __init__(main, root):
        main.root = root
        main.root.title("Currency Converter")
        main.root.geometry("800x800")
        main.root.configure(bg="#e6f7ff")  #  background 
        
        # The Setting of background image
        main.bg_image = Image.open("17454.jpg")  # Making  the Open image
        main.bg_image = main.bg_image.resize((800, 800), Image.Resampling.LANCZOS)  # To Making fit image Resizing the screen
        main.bg_photo = ImageTk.PhotoImage(main.bg_image)

        #  label for holding  the background image
        main.bg_label = tk.Label(main.root, image=main.bg_photo)
        main.bg_label.place(relwidth=1, relheight=1)  #Making The image  Stretch for full window 

        # The Header
        Hdr = tk.Label(
            root, text="Currency Converter", font=("Helvetica", 24, "bold"), bg="#4682b4", fg="white"
        )
        Hdr.pack(fill=tk.X, pady=10)

        #The  Main frame to  bring the content in center 
        main.main_frame = ttk.Frame(root, padding=10)
        main.main_frame.pack(fill=tk.BOTH, expand=True)

        # The  Frame of Input(centered)
        main.input_frame = ttk.LabelFrame(main.main_frame, text="Input", padding=10)
        main.input_frame.pack(pady=20, anchor="center")

        # The Frame of  Output  (centered)
        main.output_frame = ttk.LabelFrame(main.main_frame, text="Output", padding=10)
        main.output_frame.pack(pady=20, anchor="center")

        # The Frame of Historical Rates  (In centered)
        main.historical_frame = ttk.LabelFrame(main.main_frame, text="Historical Rates", padding=10)
        main.historical_frame.pack(pady=20, anchor="center")

        # The Dropdown of Base Currency 
        ttk.Label(main.input_frame, text="Base Currency:", font=("Helvetica", 14)).grid(
            row=0, column=0, padx=10, pady=5, sticky="w"
        )
        main.base_currency_var = tk.StringVar()
        main.base_currency_dropdown = ttk.Combobox(main.input_frame, textvariable=main.base_currency_var, font=("Helvetica", 14))
        main.base_currency_dropdown.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # The Dropdown Target Currency 
        ttk.Label(main.input_frame, text="Target Currency:", font=("Helvetica", 14)).grid(
            row=1, column=0, padx=10, pady=5, sticky="w"
        )
        main.target_currency_var = tk.StringVar()
        main.target_currency_dropdown = ttk.Combobox(main.input_frame, textvariable=main.target_currency_var, font=("Helvetica", 14))
        main.target_currency_dropdown.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # The Amount  
        ttk.Label(main.input_frame, text="Amount:", font=("Helvetica", 14)).grid(
            row=2, column=0, padx=10, pady=5, sticky="w"
        )
        main.amount_entry = ttk.Entry(main.input_frame, font=("Helvetica", 14))
        main.amount_entry.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # The Buttons of swap, Convert and clear 
        main.convert_button = tk.Button(
            main.input_frame,
            text="Convert",
            font=("Helvetica", 14),
            bg="#4682b4",
            fg="white",
            command=main.convert_currency,
        )
        main.convert_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        main.swap_button = tk.Button(
            main.input_frame,
            text="Swap",
            font=("Helvetica", 14),
            bg="#32cd32",
            fg="white",
            command=main.swap_currencies,
        )
        main.swap_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        main.clear_button = tk.Button(
            main.input_frame,
            text="Clear",
            font=("Helvetica", 14),
            bg="#ff6347",
            fg="white",
            command=main.clear_inputs,
        )
        main.clear_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        main.result_label = tk.Label(main.output_frame, text="", font=("Helvetica", 14), bg="white", anchor="w", justify="left")
        main.result_label.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        main.historical_button = tk.Button(
            main.historical_frame,
            text="View Historical Rates",
            font=("Helvetica", 14),
            bg="#4682b4",
            fg="white",
            command=main.view_historical_data,
        )
        main.historical_button.pack(fill=tk.X, padx=10, pady=10)

        main.historical_result = tk.Text(main.historical_frame, wrap=tk.WORD, height=10)
        main.historical_result.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # The Fetch available currencies in options
        main.available_currencies = main.get_available_currencies()
        main.base_currency_dropdown['values'] = main.available_currencies
        main.target_currency_dropdown['values'] = main.available_currencies

    def get_available_currencies(main):
        """Fetches all available currencies from the API."""
        url = f"{BASE_URL}currencies"
        params = {"apikey": API_KEY}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return list(response.json()["data"].keys())
        messagebox.showerror("Error", "Unable to fetch available currencies.")
        return []

    def convert_currency(main):
        """Converts the currency based on the provided inputs."""
        base_currency = main.base_currency_var.get().upper()
        target_currency = main.target_currency_var.get().upper()
        try:
            amount = float(main.amount_entry.get())
        except ValueError:
            messagebox.showerror("Input Error", "Amount must be a valid number.")
            return
        rate = main.get_exchange_rate(base_currency, target_currency)
        if rate:
            result = amount * rate
            main.result_label.config(
                text=f"{amount:.2f} {base_currency} = {result:.2f} {target_currency}"
            )
        else:
            main.result_label.config(text="Exchange rate not available.")

    def get_exchange_rate(main, base_currency, target_currency):
        """Fetches the exchange rate for the given currencies."""
        url = f"{BASE_URL}latest"
        params = {"apikey": API_KEY, "base_currency": base_currency, "currencies": target_currency}
        response = requests.get(url, params=params)
        if response.status_code == 200:
            rates = response.json()["data"]
            return rates.get(target_currency, None)
        messagebox.showerror("Error", "Unable to fetch exchange rate.")
        return None

    def swap_currencies(main):
        """Swaps the values of the base and target currency dropdowns.""" 
        base = main.base_currency_var.get()
        target = main.target_currency_var.get()
        main.base_currency_var.set(target)
        main.target_currency_var.set(base)

    def clear_inputs(main):
        """Clears all inputs and outputs.""" 
        main.base_currency_var.set("")
        main.target_currency_var.set("")
        main.amount_entry.delete(0, tk.END)
        main.result_label.config(text="")
        main.historical_result.delete(1.0, tk.END)

    def view_historical_data(main):
        """Fetches and displays historical exchange rates for the last 30 days."""
        base_currency = main.base_currency_var.get().upper()
        target_currency = main.target_currency_var.get().upper()
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
            main.historical_result.delete(1.0, tk.END)
            main.historical_result.insert(tk.END, result_text)
            # larging  the font size and reduce the text box height 
            main.historical_result.config(font=("Helvetica", 28))  # Making Double  size of font
            main.historical_result.config(height=5)  # Making the Half size of box 

        else:
            messagebox.showerror("Error", "Unable to fetch historical rates.")

class StartPage:
    def __init__(main, root):
        main.root = root
        main.root.title("Welcome")
        main.root.geometry("800x600")
        main.root.configure(bg="#3DED97")  # Given the Green background for start page

        # Hdr
        Hdr = tk.Label(
            root, text="Welcome to Currency Converter", font=("Helvetica", 48, "bold"), bg="#3DED97", fg="black"
        )
        Hdr.pack(fill=tk.X, pady=100)

        #  The Code of the Start Button
        main.start_button = tk.Button(
            root,
            text="Start",
            font=("Helvetica", 60),  # Font size 60 
            bg="#4682b4",
            fg="white",
            command=main.start_application,
        )
        main.start_button.place(relx=0.5, rely=0.5, anchor="center")

    def start_application(main):
        """Transition to the next page (Currency Converter)."""
        main.root.destroy()
        new_root = tk.Tk()
        app = CurrencyApp(new_root)
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    start_page = StartPage(root)
    root.mainloop()
