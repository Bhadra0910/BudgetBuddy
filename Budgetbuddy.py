import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from groq import Groq
import os
from dotenv import load_dotenv

# -------------------------
# Load Groq API Key
# -------------------------
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

# -------------------------
# Theme Colors
# -------------------------
PRIMARY_COLOR = "#008080"   # Teal
HOVER_COLOR   = "#006666"   # Dark teal
ACCENT_COLOR  = "#FFD700"   # Gold

# -------------------------
# App Setup
# -------------------------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
app = ctk.CTk()
app.title("BudgetBuddy")
app.geometry("1920x1280")

# -------------------------
# Variables
# -------------------------
income_var = ctk.StringVar(value="0")
expenses_var = ctk.StringVar(value="0")
balance_var = ctk.StringVar(value="0")
goals = []

# -------------------------
# Utility Functions
# -------------------------
def update_balance():
    try:
        inc = float(income_var.get())
        exp = float(expenses_var.get())
        bal = inc - exp
        balance_var.set(str(bal))
    except:
        balance_var.set("0")

def create_popup(field, var_to_update):
    popup = ctk.CTkToplevel(app)
    popup.geometry("450x250")
    popup.title(f"Edit {field}")
    popup.configure(fg_color="#2b2b2b")
    popup.grab_set()

    ctk.CTkLabel(popup, text=f"Enter new {field} amount:", font=("Arial", 20, "bold")).pack(pady=20)
    entry = ctk.CTkEntry(popup, placeholder_text="Amount", width=280, font=("Arial", 18))
    entry.pack(pady=10)

    def save_value(event=None):
        value = entry.get()
        if value.isdigit():
            var_to_update.set(value)
            update_balance()
            update_goals_display()
            popup.destroy()
        else:
            messagebox.showerror("Invalid Input", "Please enter a valid number!")

    entry.bind("<Return>", save_value)
    ctk.CTkButton(
        popup, text="Save", command=save_value,
        width=150, fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 16, "bold")
    ).pack(pady=20)

def add_expense_popup():
    popup = ctk.CTkToplevel(app)
    popup.geometry("450x350")
    popup.title("Add Expense")
    popup.configure(fg_color="#2b2b2b")
    popup.grab_set()

    ctk.CTkLabel(popup, text="Expense Name:", font=("Arial", 18, "bold")).pack(pady=(20,5))
    name_entry = ctk.CTkEntry(popup, placeholder_text="e.g. Groceries", width=280, font=("Arial", 16))
    name_entry.pack(pady=5)

    ctk.CTkLabel(popup, text="Expense Amount:", font=("Arial", 18, "bold")).pack(pady=(20,5))
    amount_entry = ctk.CTkEntry(popup, placeholder_text="Amount", width=280, font=("Arial", 16))
    amount_entry.pack(pady=5)

    def save_expense(event=None):
        name = name_entry.get()
        amount = amount_entry.get()
        if not name or not amount.isdigit():
            messagebox.showerror("Invalid Input", "Please enter valid details!")
            return
        new_total = float(expenses_var.get()) + float(amount)
        expenses_var.set(str(new_total))
        update_balance()
        add_expense_to_history(f"{name} - ₹{amount}")
        popup.destroy()

    name_entry.bind("<Return>", save_expense)
    amount_entry.bind("<Return>", save_expense)

    ctk.CTkButton(
        popup, text="Add Expense", command=save_expense,
        width=150, fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 16, "bold")
    ).pack(pady=20)

def create_info_box(parent, label_text, var, edit_command=None, add_command=None):
    box = ctk.CTkFrame(parent, corner_radius=20, width=300, height=200, fg_color="#333333")
    box.pack(side="left", padx=50, pady=20)
    box.pack_propagate(False)

    ctk.CTkLabel(box, text=label_text, font=("Arial", 22, "bold")).pack(pady=(15,5))
    value = ctk.CTkLabel(box, textvariable=var, font=("Arial", 26, "bold"), text_color=ACCENT_COLOR)
    value.pack(pady=5)

    if edit_command:
        ctk.CTkButton(
            box, text=f"Edit {label_text}", width=180, command=edit_command,
            fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 14, "bold")
        ).pack(pady=(10,5))

    if add_command:
        ctk.CTkButton(
            box, text=f"Add {label_text}", width=180, command=add_command,
            fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 14, "bold")
        ).pack(pady=(10,5))
    return box

# -------------------------
# Expense History (Textbox)
# -------------------------
def add_expense_to_history(text):
    expense_listbox.configure(state="normal")
    expense_listbox.insert("end", text + "\n")
    expense_listbox.configure(state="disabled")
    expense_listbox.see("end")

# -------------------------
# Goals with Scrollable Frame
# -------------------------
def open_goal_popup():
    popup = ctk.CTkToplevel(app)
    popup.geometry("450x300")
    popup.title("Set a Goal")
    popup.configure(fg_color="#2b2b2b")
    popup.grab_set()

    ctk.CTkLabel(popup, text="Goal Name:", font=("Arial", 18, "bold")).pack(pady=(20,5))
    name_entry = ctk.CTkEntry(popup, placeholder_text="e.g. New Bike", width=280, font=("Arial", 16))
    name_entry.pack(pady=5)

    ctk.CTkLabel(popup, text="Target Amount:", font=("Arial", 18, "bold")).pack(pady=(20,5))
    amount_entry = ctk.CTkEntry(popup, placeholder_text="Amount", width=280, font=("Arial", 16))
    amount_entry.pack(pady=5)

    def save_goal(event=None):
        name = name_entry.get()
        amount = amount_entry.get()
        if not name or not amount.isdigit():
            messagebox.showerror("Invalid Input", "Please enter valid goal details!")
            return
        goals.append({"name": name, "target": float(amount), "remaining": float(amount)})
        update_goals_display()
        popup.destroy()

    name_entry.bind("<Return>", save_goal)
    amount_entry.bind("<Return>", save_goal)

    ctk.CTkButton(
        popup, text="Save Goal", command=save_goal,
        width=150, fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 16, "bold")
    ).pack(pady=20)

def add_money_to_goal(goal_index):
    popup = ctk.CTkToplevel(app)
    popup.geometry("450x250")
    popup.title("Add Money to Goal")
    popup.configure(fg_color="#2b2b2b")
    popup.grab_set()

    g = goals[goal_index]
    ctk.CTkLabel(popup, text=f"Add money to {g['name']}", font=("Arial", 18, "bold")).pack(pady=20)
    amount_entry = ctk.CTkEntry(popup, placeholder_text="Amount", width=280, font=("Arial", 16))
    amount_entry.pack(pady=10)

    def save_amount(event=None):
        amt_str = amount_entry.get()
        if not amt_str.isdigit():
            messagebox.showerror("Invalid Input", "Please enter a valid amount!")
            return
        amt = float(amt_str)
        bal = float(balance_var.get())
        exp = float(expenses_var.get())

        if amt > bal:
            messagebox.showerror("Insufficient Balance", "Not enough balance to add this amount!")
            return

        # Update goal
        goals[goal_index]["remaining"] -= amt

        # Update expenses (balance auto-adjusts)
        expenses_var.set(str(exp + amt))

        # Log in history
        add_expense_to_history(f"Goal: {g['name']} - ₹{amt}")

        update_balance()
        update_goals_display()
        popup.destroy()

    amount_entry.bind("<Return>", save_amount)

    ctk.CTkButton(
        popup, text="Add", command=save_amount,
        width=150, fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 16, "bold")
    ).pack(pady=20)

def update_goals_display():
    for widget in goals_scroll_frame.winfo_children():
        widget.destroy()

    ctk.CTkLabel(goals_scroll_frame, text="Goals", font=("Arial", 26, "bold")).pack(pady=15)

    for i, g in enumerate(goals):
        frame = ctk.CTkFrame(goals_scroll_frame, corner_radius=15, fg_color="#444444")
        frame.pack(fill="x", padx=15, pady=10)

        status = "✅ Completed" if g["remaining"] <= 0 else f"Remaining: ₹{g['remaining']}"
        goal_text = f"{g['name']} - Target: ₹{g['target']} ({status})"

        ctk.CTkLabel(
            frame, 
            text=goal_text, 
            font=("Arial", 18, "bold"), 
            wraplength=350,   
            justify="left",   
            anchor="w"
        ).pack(anchor="w", padx=10, pady=(10,5))

        funded = g["target"] - g["remaining"]
        percent = max(0, min(1, funded / g["target"]))

        bar_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bar_frame.pack(pady=5, padx=10, fill="x")

        progress = ctk.CTkProgressBar(bar_frame, width=300)
        progress.set(percent)
        progress.pack(side="left", padx=(0,10))

        percent_label = ctk.CTkLabel(bar_frame, text=f"{int(percent*100)}%", font=("Arial", 14))
        percent_label.pack(side="left")

        if g["remaining"] > 0:
            ctk.CTkButton(
                frame, text="Add Money", width=120,
                command=lambda idx=i: add_money_to_goal(idx),
                fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 14, "bold")
            ).pack(padx=10, pady=(5,10))

# -------------------------
# Chatbot
# -------------------------
def open_chatbot():
    popup = ctk.CTkToplevel(app)
    popup.geometry("700x700")
    popup.title("BudgetBuddy Chatbot")
    popup.configure(fg_color="#1e1e1e")
    popup.grab_set()

    ctk.CTkLabel(popup, text="🤖 Budget Assistant", font=("Arial", 22, "bold")).pack(pady=10)
    chat_box = ctk.CTkTextbox(popup, width=650, height=500, font=("Arial", 14), corner_radius=10)
    chat_box.pack(pady=10)
    chat_box.configure(state="disabled")

    input_frame = ctk.CTkFrame(popup, fg_color="#2b2b2b", corner_radius=10)
    input_frame.pack(pady=10, fill="x", padx=15)

    user_entry = ctk.CTkEntry(input_frame, placeholder_text="Type your question here...", width=500, font=("Arial", 14))
    user_entry.pack(side="left", padx=10, pady=10)

    def send_message(event=None):
        user_msg = user_entry.get().strip()
        if not user_msg:
            return
        user_entry.delete(0, "end")
        chat_box.configure(state="normal")
        chat_box.insert("end", f"You: {user_msg}\n")
        chat_box.configure(state="disabled")
        chat_box.see("end")

        inc = float(income_var.get())
        exp = float(expenses_var.get())
        bal = float(balance_var.get())
        history = expense_listbox.get("1.0", "end").strip()

        prompt = f"""
        I have a budgeting app.
        Current income: ₹{inc}
        Current expenses: ₹{exp}
        Current balance: ₹{bal}
        Expense history: {history}
        My goals: {goals}

        Question: {user_msg}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
            )
            bot_reply = response.choices[0].message.content
        except Exception as e:
            bot_reply = f"⚠ Error: {e}"

        chat_box.configure(state="normal")
        chat_box.insert("end", f"Bot: {bot_reply}\n\n")
        chat_box.configure(state="disabled")
        chat_box.see("end")

    user_entry.bind("<Return>", send_message)

    ctk.CTkButton(
        input_frame, text="Send", command=send_message,
        fg_color=PRIMARY_COLOR, hover_color=HOVER_COLOR, font=("Arial", 14, "bold"), width=100
    ).pack(side="right", padx=10, pady=10)

# -------------------------
# Header
# -------------------------
header_frame = ctk.CTkFrame(app, fg_color="transparent")
header_frame.pack(fill="x", pady=20, padx=30)
left_header = ctk.CTkFrame(header_frame, fg_color="transparent")
left_header.pack(side="left")

try:
    logo_img = Image.open("logo.png").resize((70, 70))
    logo = ctk.CTkImage(light_image=logo_img, dark_image=logo_img, size=(70,70))
    ctk.CTkLabel(left_header, image=logo, text="").pack(side="left", padx=15)
except:
    ctk.CTkLabel(left_header, text="🪙", font=("Arial", 50)).pack(side="left", padx=15)

ctk.CTkLabel(left_header, text="BudgetBuddy", font=("Arial", 40, "bold")).pack(side="left")

ctk.CTkButton(
    header_frame, text="🎯 Goals", width=140, fg_color=PRIMARY_COLOR,
    hover_color=HOVER_COLOR, font=("Arial", 16, "bold"), command=open_goal_popup
).pack(side="right", padx=20)

ctk.CTkButton(
    header_frame, text="🤖 Chatbot", width=140, fg_color=PRIMARY_COLOR,
    hover_color=HOVER_COLOR, font=("Arial", 16, "bold"), command=open_chatbot
).pack(side="right", padx=20)

# -------------------------
# Info Section
# -------------------------
info_frame = ctk.CTkFrame(app, fg_color="transparent")
info_frame.pack(anchor="center", pady=(0,10))
create_info_box(info_frame, "Income", income_var, edit_command=lambda: create_popup("Income", income_var))
create_info_box(info_frame, "Expenses", expenses_var, add_command=add_expense_popup)
create_info_box(info_frame, "Balance", balance_var)

# -------------------------
# Expense & Goals Sections
# -------------------------
list_frame = ctk.CTkFrame(app, fg_color="transparent")
list_frame.pack(pady=20, padx=50, fill="both", expand=True)

# Expense History
expense_frame = ctk.CTkScrollableFrame(list_frame, corner_radius=20, fg_color="#2b2b2b", width=800, height=600)
expense_frame.pack(side="left", padx=20, fill="both", expand=True)
ctk.CTkLabel(expense_frame, text="Expense History", font=("Arial", 26, "bold")).pack(pady=15)

expense_listbox = ctk.CTkTextbox(expense_frame, width=750, height=500, font=("Arial", 16))
expense_listbox.pack(pady=10)
expense_listbox.configure(state="disabled")

# Goals
goals_scroll_frame = ctk.CTkScrollableFrame(list_frame, corner_radius=20, fg_color="#2b2b2b", width=800, height=600)
goals_scroll_frame.pack(side="left", padx=20, fill="both", expand=True)
update_goals_display()

# -------------------------
# Run App
# -------------------------
app.mainloop()