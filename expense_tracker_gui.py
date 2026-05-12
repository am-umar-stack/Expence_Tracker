import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akhunzada's Expense Tracker")
        self.root.geometry("520x900")
        self.root.configure(bg="#0F0F0F")
        
        # Internal Data (All stored in USD for base calculation)
        self.total_spent_usd = 0.0
        self.currency_symbol = "$" 
        
        # Simple Exchange Rates (Relative to 1 USD)
        self.rates = {
            "USD ($)": 1.0,
            "EUR (€)": 0.92,
            "PKR (Rs.)": 278.0
        }

        # Custom Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color Palette
        self.bg_color = "#0F0F0F"
        self.card_color = "#1A1A1A"
        self.primary_color = "#7209B7"
        self.secondary_color = "#4CC9F0"
        self.accent_color = "#F72585"
        self.text_color = "#FFFFFF"
        self.muted_text = "#888888"

        # Configure Styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_color)
        self.style.configure("Header.TLabel", background=self.bg_color, foreground=self.secondary_color, font=("Segoe UI", 16, "bold"))
        self.style.configure("Title.TLabel", background=self.bg_color, foreground=self.text_color, font=("Segoe UI", 20, "bold"))
        self.style.configure("Label.TLabel", background=self.card_color, foreground=self.text_color, font=("Segoe UI", 10, "bold"))
        self.style.configure("Add.TButton", font=("Segoe UI", 11, "bold"), background=self.primary_color, foreground="white", borderwidth=0)
        self.style.map("Add.TButton", background=[('active', '#560BAD')], foreground=[('active', 'white')])
        self.style.configure("Clear.TButton", font=("Segoe UI", 10), background="#333333", foreground="#BBBBBB", borderwidth=0)

        # ===================== UI LAYOUT =====================
        
        # --- 1. Header ---
        header_frame = ttk.Frame(self.root, style="TFrame", padding=(20, 20, 20, 5))
        header_frame.pack(fill="x")
        
        header_top = ttk.Frame(header_frame, style="TFrame")
        header_top.pack(fill="x")
        
        ttk.Label(header_top, text="AKHUNZADA'S", style="Header.TLabel").pack(side="left")
        
        # Input Currency Selector
        input_cur_frame = ttk.Frame(header_top, style="TFrame")
        input_cur_frame.pack(side="right")
        ttk.Label(input_cur_frame, text="Input: ", font=("Segoe UI", 8), foreground=self.muted_text, background=self.bg_color).pack(side="left")
        self.input_cur_var = tk.StringVar(value="USD ($)")
        self.input_cur_menu = ttk.Combobox(input_cur_frame, textvariable=self.input_cur_var, 
                                          values=list(self.rates.keys()), 
                                          state="readonly", width=8, font=("Segoe UI", 9))
        self.input_cur_menu.pack(side="left")
        self.input_cur_menu.bind("<<ComboboxSelected>>", self.update_input_label)
        
        ttk.Label(header_frame, text="Expense Tracker", style="Title.TLabel").pack(anchor="w")

        # --- 2. Input Card ---
        input_card = ttk.Frame(self.root, style="Card.TFrame", padding=15)
        input_card.pack(fill="x", padx=20, pady=(5, 5))
        
        ttk.Label(input_card, text="ITEM NAME", style="Label.TLabel").pack(anchor="w")
        self.item_entry = tk.Entry(input_card, font=("Segoe UI", 12), bg="#2D2D2D", fg="#FFFFFF", 
                                   insertbackground="white", relief="flat", highlightthickness=1, 
                                   highlightbackground="#444444", highlightcolor=self.primary_color)
        self.item_entry.pack(fill="x", pady=(3, 10), ipady=6)
        self.item_entry.insert(0, "e.g. Coffee")
        self.item_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.item_entry, "e.g. Coffee"))
        
        self.amount_label = ttk.Label(input_card, text="AMOUNT ($)", style="Label.TLabel")
        self.amount_label.pack(anchor="w")
        self.amount_entry = tk.Entry(input_card, font=("Segoe UI", 12), bg="#2D2D2D", fg="#FFFFFF", 
                                     insertbackground="white", relief="flat", highlightthickness=1, 
                                     highlightbackground="#444444", highlightcolor=self.primary_color)
        self.amount_entry.pack(fill="x", pady=(3, 12), ipady=6)
        self.amount_entry.bind("<Return>", lambda event: self.add_expense())
        
        ttk.Button(input_card, text="ADD TO EXPENSES", style="Add.TButton", command=self.add_expense).pack(fill="x", ipady=8)

        # --- 3. Total Card (packed BEFORE history so it stays at bottom) ---
        total_card = ttk.Frame(self.root, style="Card.TFrame", padding=15)
        total_card.pack(side="bottom", fill="x", padx=20, pady=(5, 15))
        
        total_header = ttk.Frame(total_card, style="Card.TFrame")
        total_header.pack(fill="x")
        
        ttk.Label(total_header, text="TOTAL BALANCE", background=self.card_color, 
                  foreground=self.muted_text, font=("Segoe UI", 9, "bold")).pack(side="left")
        
        self.total_cur_var = tk.StringVar(value="USD ($)")
        self.total_cur_menu = ttk.Combobox(total_header, textvariable=self.total_cur_var, 
                                          values=list(self.rates.keys()), 
                                          state="readonly", width=8, font=("Segoe UI", 8))
        self.total_cur_menu.pack(side="right")
        self.total_cur_menu.bind("<<ComboboxSelected>>", self.refresh_total_display)
        
        self.total_label = tk.Label(total_card, text="$0.00", bg=self.card_color, 
                                    fg=self.accent_color, font=("Segoe UI", 28, "bold"))
        self.total_label.pack(pady=8)
        
        ttk.Button(total_card, text="RESET DATA", style="Clear.TButton", command=self.reset_tracker).pack()

        # --- 4. History Section (fills ALL remaining space between input and total) ---
        history_frame = ttk.Frame(self.root, style="TFrame", padding=(20, 10, 20, 5))
        history_frame.pack(fill="both", expand=True)
        
        tk.Label(history_frame, text="RECENT TRANSACTIONS", bg=self.bg_color, 
                 fg=self.secondary_color, font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 8))
        
        # Listbox container with a visible border
        list_container = tk.Frame(history_frame, bg="#2A2A2A", bd=1)
        list_container.pack(fill="both", expand=True)
        
        self.history_listbox = tk.Listbox(list_container, font=("Segoe UI", 11), 
                                          bg="#1A1A1A", fg="#EEEEEE", relief="flat", 
                                          borderwidth=0, highlightthickness=0, 
                                          selectbackground="#333333", activestyle="none")
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)
        
        # Initial Refresh
        self.refresh_total_display()

    def update_input_label(self, event=None):
        selection = self.input_cur_var.get()
        symbol = selection.split("(")[1].replace(")", "")
        self.amount_label.config(text=f"AMOUNT ({symbol})")

    def refresh_total_display(self, event=None):
        selection = self.total_cur_var.get()
        symbol = selection.split("(")[1].replace(")", "")
        rate = self.rates[selection]
        
        converted_total = self.total_spent_usd * rate
        self.total_label.config(text=f"{symbol}{converted_total:,.2f}")

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def add_expense(self):
        item_name = self.item_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        
        if not amount_str:
            return
        if not item_name or item_name == "e.g. Coffee":
            item_name = "General Expense"
            
        try:
            amount = float(amount_str)
            if amount < 0:
                messagebox.showerror("Error", "Expense cannot be negative!")
                return
            
            # Convert input amount to USD for internal storage
            input_cur = self.input_cur_var.get()
            rate_to_base = self.rates[input_cur]
            amount_in_usd = amount / rate_to_base
            
            self.total_spent_usd += amount_in_usd
            
            # Formatting for History (Shows original currency)
            symbol = input_cur.split("(")[1].replace(")", "")
            timestamp = datetime.now().strftime("%H:%M")
            entry_text = f"  {timestamp}   {item_name:<20}  +{symbol}{amount:,.2f}"
            
            # Update UI
            self.refresh_total_display()
            self.history_listbox.insert(0, entry_text) 
            
            self.amount_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(0, "e.g. Coffee")
            self.root.focus()
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numerical amount.")

    def reset_tracker(self):
        if messagebox.askyesno("Reset Tracker", "Clear all transaction history?"):
            self.total_spent_usd = 0.0
            self.refresh_total_display()
            self.history_listbox.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(0, "e.g. Coffee")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
