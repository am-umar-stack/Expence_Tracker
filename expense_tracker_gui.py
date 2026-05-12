import tkinter as tk
from tkinter import ttk, messagebox

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Akhunzada's Expense Tracker")
        self.root.geometry("450x600")
        self.root.configure(bg="#121212")  # Sleek Dark Background
        
        self.total_spent = 0.0
        self.history = []

        # Custom Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure Styles
        self.style.configure("TFrame", background="#121212")
        self.style.configure("Header.TLabel", 
                             background="#121212", 
                             foreground="#00A8E8", 
                             font=("Segoe UI", 18, "bold"))
        
        self.style.configure("Total.TLabel", 
                             background="#121212", 
                             foreground="#00FF41",  # Matrix green for total
                             font=("Segoe UI", 24, "bold"))

        self.style.configure("History.TLabel", 
                             background="#121212", 
                             foreground="#BBBBBB", 
                             font=("Segoe UI", 10))

        self.style.configure("Add.TButton", 
                             font=("Segoe UI", 11, "bold"), 
                             background="#00A8E8", 
                             foreground="white",
                             borderwidth=0)
        self.style.map("Add.TButton", background=[('active', '#007BB0')])

        self.style.configure("Clear.TButton", 
                             font=("Segoe UI", 10), 
                             background="#333333", 
                             foreground="white",
                             borderwidth=0)

        # UI LAYOUT
        
        # 1. Header
        header_frame = ttk.Frame(self.root, style="TFrame", padding=20)
        header_frame.pack(fill="x")
        
        header_label = ttk.Label(header_frame, text="AKHUNZADA'S EXPENSE TRACKER", style="Header.TLabel")
        header_label.pack()
        
        sub_header = ttk.Label(header_frame, text="Personal Expense Management", 
                               background="#121212", foreground="#666666", font=("Segoe UI", 8))
        sub_header.pack()

        # 2. Input Area
        input_frame = ttk.Frame(self.root, style="TFrame", padding=20)
        input_frame.pack(fill="x")
        
        ttk.Label(input_frame, text="Enter Amount:", background="#121212", foreground="#FFFFFF", font=("Segoe UI", 10)).pack(anchor="w")
        
        self.amount_entry = tk.Entry(input_frame, 
                                     font=("Segoe UI", 14), 
                                     bg="#1E1E1E", 
                                     fg="#FFFFFF", 
                                     insertbackground="white",
                                     relief="flat",
                                     highlightthickness=1,
                                     highlightbackground="#333333",
                                     highlightcolor="#00A8E8")
        self.amount_entry.pack(fill="x", pady=(5, 15), ipady=5)
        self.amount_entry.bind("<Return>", lambda event: self.add_expense())
        
        self.add_button = ttk.Button(input_frame, text="ADD EXPENSE", style="Add.TButton", command=self.add_expense)
        self.add_button.pack(fill="x", ipady=5)

        # 3. History Area
        history_frame = ttk.Frame(self.root, style="TFrame", padding=20)
        history_frame.pack(fill="both", expand=True)
        
        ttk.Label(history_frame, text="RECENT HISTORY", style="History.TLabel").pack(anchor="w", pady=(0, 5))
        
        self.history_listbox = tk.Listbox(history_frame, 
                                          font=("Segoe UI", 10), 
                                          bg="#1E1E1E", 
                                          fg="#CCCCCC", 
                                          relief="flat", 
                                          borderwidth=0,
                                          highlightthickness=0,
                                          selectbackground="#333333")
        self.history_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        # 4. Total Area
        total_frame = ttk.Frame(self.root, style="TFrame", padding=20)
        total_frame.pack(fill="x")
        
        ttk.Label(total_frame, text="TOTAL SPENT", background="#121212", foreground="#BBBBBB", font=("Segoe UI", 10)).pack()
        
        self.total_label = ttk.Label(total_frame, text="$0.00", style="Total.TLabel")
        self.total_label.pack()
        
        self.clear_button = ttk.Button(total_frame, text="RESET ALL", style="Clear.TButton", command=self.reset_tracker)
        self.clear_button.pack(pady=(10, 0))

    def add_expense(self):
        amount_str = self.amount_entry.get().strip()
        
        if not amount_str:
            return
            
        try:
            amount = float(amount_str)
            if amount < 0:
                messagebox.showerror("Error", "Expense cannot be negative!")
                return
            
            # Update data
            self.total_spent += amount
            self.history.append(amount)
            
            # Update UI
            self.total_label.config(text=f"${self.total_spent:,.2f}")
            self.history_listbox.insert(0, f" + ${amount:,.2f}") # Insert at top
            
            # Clear input
            self.amount_entry.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid numerical amount.")

    def reset_tracker(self):
        if messagebox.askyesno("Reset", "Are you sure you want to clear all data?"):
            self.total_spent = 0.0
            self.history = []
            self.total_label.config(text="$0.00")
            self.history_listbox.delete(0, tk.END)
            self.amount_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
