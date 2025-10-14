"""
Smart Expense Manager (Enhanced)
--------------------------------
Modes:
 - GUI Mode (Desktop): python app.py gui
 - Web Mode (Browser): python app.py web
Dependencies:
 pip install customtkinter matplotlib flask
"""

import csv, os, sys
from datetime import datetime
from collections import defaultdict

# --- Shared Data Logic ---
CSV_FILE = 'expenses.csv'

def ensure_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            f.write('Date,Category,Amount\n')

def add_expense_to_csv(date, category, amount):
    with open(CSV_FILE, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([date, category, f"{amount:.2f}"])

def read_all_expenses():
    ensure_csv()
    rows = []
    with open(CSV_FILE, 'r') as f:
        reader = csv.reader(f)
        next(reader, None)
        for row in reader:
            if len(row) == 3:
                rows.append((row[0], row[1], float(row[2])))
    return rows

def get_category_summary():
    sums = defaultdict(float)
    for d, c, a in read_all_expenses():
        sums[c] += a
    return dict(sums)

def generate_rule_based_advice():
    summary = get_category_summary()
    total = sum(summary.values())
    if total == 0:
        return "No expenses recorded yet. Add some entries and I'll give tips!"
    advice_lines = []
    for cat, amt in summary.items():
        pct = (amt / total) * 100
        if pct > 40:
            advice_lines.append(f"- {cat}: {pct:.1f}% of spending — reduce non-essential costs here.")
        elif pct > 25:
            advice_lines.append(f"- {cat}: {pct:.1f}% — monitor this category.")
        else:
            advice_lines.append(f"- {cat}: {pct:.1f}% — looks reasonable.")
    if total > 20000:
        advice_lines.append("\nOverall: Spending is high. Consider weekly budgeting.")
    else:
        advice_lines.append("\nOverall: Spending is moderate. Good work!")
    return "\n".join(advice_lines)

# --- GUI Mode using CustomTkinter ---
def run_gui():
    import customtkinter as ctk
    import tkinter.messagebox as messagebox
    from tkinter import ttk
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    class SmartExpenseApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("💰 Smart Expense Manager - Modern Edition")
            self.geometry("950x600")
            self.resizable(False, False)
            self.chart_window = None
            self.create_ui()
            self.refresh_table()

        def create_ui(self):
            # Input Frame
            frame = ctk.CTkFrame(self, corner_radius=15)
            frame.pack(padx=10, pady=10, fill="x")

            self.date_entry = ctk.CTkEntry(frame, placeholder_text="YYYY-MM-DD", width=150)
            self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
            self.date_entry.pack(side="left", padx=5)

            self.cat_entry = ctk.CTkEntry(frame, placeholder_text="Category", width=150)
            self.cat_entry.pack(side="left", padx=5)

            self.amt_entry = ctk.CTkEntry(frame, placeholder_text="Amount (₹)", width=120)
            self.amt_entry.pack(side="left", padx=5)

            ctk.CTkButton(frame, text="Add Expense", command=self.add_expense).pack(side="left", padx=10)
            ctk.CTkButton(frame, text="Bar Chart", command=self.show_bar_chart).pack(side="left", padx=5)
            ctk.CTkButton(frame, text="Pie Chart", command=self.show_pie_chart).pack(side="left", padx=5)

            # Read-only Expense Table
            table_frame = ctk.CTkFrame(self)
            table_frame.pack(padx=10, pady=10, fill="both", expand=True)

            style = ttk.Style()
            style.theme_use('default')
            style.configure("Treeview", background="#222", foreground="white", fieldbackground="#222", rowheight=25)
            style.map('Treeview', background=[('selected', '#444')])

            self.table = ttk.Treeview(table_frame, columns=("Date", "Category", "Amount"), show="headings", selectmode="browse")
            for col in ("Date", "Category", "Amount"):
                self.table.heading(col, text=col)
                self.table.column(col, anchor="center", width=200)
            self.table.pack(fill="both", expand=True)

            scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
            self.table.configure(yscroll=scrollbar.set)
            scrollbar.pack(side="right", fill="y")

            # AI Text Area (read-only)
            self.ai_text = ctk.CTkTextbox(self, height=150)
            self.ai_text.pack(padx=10, pady=(0,10), fill="x")
            self.ai_text.configure(state="disabled")

            ctk.CTkButton(self, text="💡 Ask AI for Advice", command=self.show_advice).pack(pady=5)

        def add_expense(self):
            date = self.date_entry.get().strip()
            cat = self.cat_entry.get().strip()
            amt = self.amt_entry.get().strip()
            try:
                amt = float(amt)
                datetime.strptime(date, "%Y-%m-%d")
            except:
                messagebox.showerror("Input Error", "Enter a valid date (YYYY-MM-DD) and numeric amount.")
                return
            add_expense_to_csv(date, cat, amt)
            messagebox.showinfo("Success", "Expense added successfully.")
            self.refresh_table()
            self.cat_entry.delete(0, "end")
            self.amt_entry.delete(0, "end")

        def refresh_table(self):
            for item in self.table.get_children():
                self.table.delete(item)
            for d, c, a in read_all_expenses():
                self.table.insert("", "end", values=(d, c, f"₹{a:.2f}"))

        def _show_chart_window(self, fig, title):
            # Close any previous chart window first
            if self.chart_window and self.chart_window.winfo_exists():
                self.chart_window.destroy()
            self.chart_window = ctk.CTkToplevel(self)
            self.chart_window.title(title)
            self.chart_window.geometry("600x400")
            canvas = FigureCanvasTkAgg(fig, master=self.chart_window)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            ctk.CTkButton(self.chart_window, text="Close", command=self.chart_window.destroy).pack(pady=5)

        def show_bar_chart(self):
            summary = get_category_summary()
            if not summary:
                messagebox.showinfo("Info", "No data to display.")
                return
            fig = Figure(figsize=(5, 3))
            ax = fig.add_subplot(111)
            ax.bar(summary.keys(), summary.values(), color="#0078ff")
            ax.set_title("Expenses by Category")
            ax.set_ylabel("Amount (₹)")
            self._show_chart_window(fig, "Bar Chart")

        def show_pie_chart(self):
            summary = get_category_summary()
            if not summary:
                messagebox.showinfo("Info", "No data to display.")
                return
            fig = Figure(figsize=(5, 3))
            ax = fig.add_subplot(111)
            ax.pie(summary.values(), labels=summary.keys(), autopct='%1.1f%%', startangle=140)
            ax.set_title("Expense Distribution")
            self._show_chart_window(fig, "Pie Chart")

        def show_advice(self):
            advice = generate_rule_based_advice()
            self.ai_text.configure(state="normal")
            self.ai_text.delete("1.0", "end")
            self.ai_text.insert("end", advice)
            self.ai_text.configure(state="disabled")

    app = SmartExpenseApp()
    app.mainloop()
# --- Web Mode using Flask ---
def run_web():
    from flask import Flask, render_template_string, request, redirect, url_for

    app = Flask(__name__)

    HTML = """
    <!DOCTYPE html><html><head>
    <title>Smart Expense Manager (Web)</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css">
    </head><body class="bg-dark text-light">
    <div class="container py-4">
      <h2 class="mb-4">💰 Smart Expense Manager (Web)</h2>
      <form method="POST" class="row g-3 mb-4">
        <div class="col-md-3"><input class="form-control" name="date" type="date" required></div>
        <div class="col-md-3"><input class="form-control" name="category" placeholder="Category" required></div>
        <div class="col-md-3"><input class="form-control" name="amount" placeholder="Amount" required></div>
        <div class="col-md-3"><button class="btn btn-primary w-100">Add Expense</button></div>
      </form>
      <table class="table table-dark table-striped">
        <tr><th>Date</th><th>Category</th><th>Amount (₹)</th></tr>
        {% for d,c,a in expenses %}
          <tr><td>{{d}}</td><td>{{c}}</td><td>{{a}}</td></tr>
        {% endfor %}
      </table>
      <hr>
      <h5>AI Insights</h5>
      <pre>{{advice}}</pre>
    </div></body></html>
    """

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            add_expense_to_csv(
                request.form['date'],
                request.form['category'],
                float(request.form['amount'])
            )
            return redirect(url_for('index'))
        return render_template_string(HTML,
                                      expenses=read_all_expenses(),
                                      advice=generate_rule_based_advice())

    app.run(debug=True)

# --- Entry Point ---
if __name__ == "__main__":
    ensure_csv()
    mode = sys.argv[1] if len(sys.argv) > 1 else "gui"
    if mode == "web":
        run_web()
    else:
        run_gui()
