import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akhunzada's Expense Tracker")
        self.root.geometry("480x700")
        self.root.configure(bg="#0F0F0F")  # Deep Black Background
        
        self.total_spent = 0.0
        self.history = []

        # Custom Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color Palette
        self.bg_color = "#0F0F0F"
        self.card_color = "#1A1A1A"
        self.primary_color = "#7209B7"  # Vibrant Purple
        self.secondary_color = "#4CC9F0" # Sky Blue
        self.accent_color = "#F72585"    # Pink
        self.text_color = "#FFFFFF"
        self.muted_text = "#888888"

        # Configure Styles
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Card.TFrame", background=self.card_color)
        
        self.style.configure("Header.TLabel", 
                             background=self.bg_color, 
                             foreground=self.secondary_color, 
                             font=("Segoe UI", 16, "bold"))
        
        self.style.configure("Title.TLabel", 
                             background=self.bg_color, 
                             foreground=self.text_color, 
                             font=("Segoe UI", 20, "bold"))

        self.style.configure("Sub.TLabel", 
                             background=self.bg_color, 
                             foreground=self.muted_text, 
                             font=("Segoe UI", 9))

        self.style.configure("Total.TLabel", 
                             background=self.card_color, 
                             foreground=self.accent_color, 
                             font=("Segoe UI", 32, "bold"))

        self.style.configure("Label.TLabel", 
                             background=self.card_color, 
                             foreground=self.text_color, 
                             font=("Segoe UI", 10, "bold"))

        self.style.configure("Add.TButton", 
                             font=("Segoe UI", 11, "bold"), 
                             background=self.primary_color, 
                             foreground="white",
                             borderwidth=0)
        self.style.map("Add.TButton", 
                       background=[('active', '#560BAD')],
                       foreground=[('active', 'white')])

        self.style.configure("Clear.TButton", 
                             font=("Segoe UI", 10), 
                             background="#333333", 
                             foreground="#BBBBBB",
                             borderwidth=0)
        self.style.map("Clear.TButton", background=[('active', '#444444')])

        # UI LAYOUT
        
        # 1. Header Section
        header_frame = ttk.Frame(self.root, style="TFrame", padding=(20, 30, 20, 10))
        header_frame.pack(fill="x")
        
        header_label = ttk.Label(header_frame, text="AKHUNZADA'S", style="Header.TLabel")
        header_label.pack(anchor="w")
        
        title_label = ttk.Label(header_frame, text="Expense Tracker", style="Title.TLabel")
        title_label.pack(anchor="w")
        
        sub_header = ttk.Label(header_frame, text="Premium Financial Management", style="Sub.TLabel")
        sub_header.pack(anchor="w", pady=(2, 0))

        # 2. Input Card
        input_card = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        input_card.pack(fill="x", padx=20, pady=10)
        
        # Product Name
        ttk.Label(input_card, text="ITEM NAME", style="Label.TLabel").pack(anchor="w")
        self.item_entry = tk.Entry(input_card, 
                                   font=("Segoe UI", 12), 
                                   bg="#2D2D2D", 
                                   fg="#FFFFFF", 
                                   insertbackground="white",
                                   relief="flat",
                                   highlightthickness=1,
                                   highlightbackground="#444444",
                                   highlightcolor=self.primary_color)
        self.item_entry.pack(fill="x", pady=(5, 15), ipady=8)
        self.item_entry.insert(0, "e.g. Coffee")
        self.item_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.item_entry, "e.g. Coffee"))
        
        # Amount
        ttk.Label(input_card, text="AMOUNT ($)", style="Label.TLabel").pack(anchor="w")
        self.amount_entry = tk.Entry(input_card, 
                                     font=("Segoe UI", 12), 
                                     bg="#2D2D2D", 
                                     fg="#FFFFFF", 
                                     insertbackground="white",
                                     relief="flat",
                                     highlightthickness=1,
                                     highlightbackground="#444444",
                                     highlightcolor=self.primary_color)
        self.amount_entry.pack(fill="x", pady=(5, 20), ipady=8)
        self.amount_entry.bind("<Return>", lambda event: self.add_expense())
        
        self.add_button = ttk.Button(input_card, text="ADD TO EXPENSES", style="Add.TButton", command=self.add_expense)
        self.add_button.pack(fill="x", ipady=10)

        # 3. History Section
        history_frame = ttk.Frame(self.root, style="TFrame", padding=20)
        history_frame.pack(fill="both", expand=True)
        
        ttk.Label(history_frame, text="RECENT TRANSACTIONS", 
                  background=self.bg_color, foreground=self.muted_text, font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(0, 10))
        
        self.history_listbox = tk.Listbox(history_frame, 
                                          font=("Segoe UI", 11), 
                                          bg="#1A1A1A", 
                                          fg="#EEEEEE", 
                                          relief="flat", 
                                          borderwidth=0,
                                          highlightthickness=0,
                                          selectbackground="#333333",
                                          activestyle="none")
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # 4. Footer Card (Total)
        footer_card = ttk.Frame(self.root, style="Card.TFrame", padding=20)
        footer_card.pack(fill="x", padx=20, pady=(10, 30))
        
        ttk.Label(footer_card, text="TOTAL BALANCE SPENT", 
                  background=self.card_color, foreground=self.muted_text, font=("Segoe UI", 9, "bold")).pack()
        
        self.total_label = ttk.Label(footer_card, text="$0.00", style="Total.TLabel")
        self.total_label.pack(pady=5)
        
        self.clear_button = ttk.Button(footer_card, text="RESET DATA", style="Clear.TButton", command=self.reset_tracker)
        self.clear_button.pack(pady=(10, 0))

    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def add_expense(self):
        item_name = self.item_entry.get().strip()
        amount_str = self.amount_entry.get().strip()
        
        if not amount_str or amount_str == "":
            return
        
        if not item_name or item_name == "e.g. Coffee":
            item_name = "General Expense"
            
        try:
            amount = float(amount_str)
            if amount < 0:
                messagebox.showerror("Error", "Expense cannot be negative!")
                return
            
            # Update data
            self.total_spent += amount
            timestamp = datetime.now().strftime("%H:%M")
            entry_text = f" {timestamp}  {item_name:<18}  +${amount:,.2f}"
            
            # Update UI
            self.total_label.config(text=f"${self.total_spent:,.2f}")
            self.history_listbox.insert(0, entry_text) 
            
            # Clear input
            self.amount_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(0, "e.g. Coffee")
            self.root.focus() # Unfocus entry
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numerical amount.")

    def reset_tracker(self):
        if messagebox.askyesno("Reset Tracker", "Clear all transaction history?"):
            self.total_spent = 0.0
            self.history = []
            self.total_label.config(text="$0.00")
            self.history_listbox.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)
            self.item_entry.delete(0, tk.END)
            self.item_entry.insert(0, "e.g. Coffee")

if __name__ == "__main__":
    root = tk.Tk()
    # Set window icon if possible (optional)
    app = ExpenseTrackerApp(root)
    root.mainloop()
