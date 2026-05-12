# 💰 Akhunzada's Expense Tracker

A sleek, modern desktop expense tracker built with Python and Tkinter. Track your daily expenses with style.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

- **Add Expenses** — Log expenses with item names and amounts
- **Multi-Currency Support** — Input expenses in USD ($), EUR (€), or PKR (Rs.)
- **Currency Conversion** — View your total balance in any currency with built-in exchange rates
- **Transaction History** — See all recent transactions with timestamps
- **Premium Dark Theme** — Vibrant purple, sky blue, and pink accents on a deep black background
- **Reset Data** — Clear all history and start fresh

## 🖥️ Screenshot

| Feature | Description |
|---------|-------------|
| 🎨 Dark Theme | Deep black background with vibrant color accents |
| 💱 Dual Currency Selectors | Separate selectors for input and total display |
| 📜 Transaction History | Scrollable list with time, item name, and amount |
| 📊 Live Total | Real-time total with currency conversion |

## 🚀 Getting Started

### Prerequisites

- Python 3.x installed on your system
- Tkinter (comes pre-installed with Python)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/am-umar-stack/Expence_Tracker.git
   cd Expence_Tracker
   ```

2. **Run the application**
   ```bash
   python expense_tracker_gui.py
   ```

## 🎯 How to Use

1. **Select Input Currency** — Choose USD, EUR, or PKR from the top-right dropdown
2. **Enter Item Name** — Type the name of your expense (optional, defaults to "General Expense")
3. **Enter Amount** — Type the expense amount
4. **Click "ADD TO EXPENSES"** — Or press Enter to add
5. **View Total in Any Currency** — Use the dropdown next to "TOTAL BALANCE" to convert
6. **Reset** — Click "RESET DATA" to clear everything

## 💱 Exchange Rates

| Currency | Rate (relative to 1 USD) |
|----------|--------------------------|
| USD ($)  | 1.00                     |
| EUR (€)  | 0.92                     |
| PKR (Rs.)| 278.00                   |

## 🛠️ Tech Stack

- **Language:** Python 3
- **GUI Framework:** Tkinter
- **Styling:** Custom dark theme with ttk styles

## 📁 Project Structure

```
Expence_Tracker/
├── expense_tracker_gui.py   # Main application file
└── README.md                # Project documentation
```

## 👤 Author

**Akhunzada**

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
