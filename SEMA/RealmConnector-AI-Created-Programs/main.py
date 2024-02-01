import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import smtplib
from email.message import EmailMessage
import urllib.request
import json
import time
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from retry import retry

class ExpenseManager:
    def __init__(self):
        self.transactions = []
        self.expense_categories = {'Food': 0, 'Transportation': 0, 'Housing': 0,
                                   'Utilities': 0, 'Entertainment': 0, 'Healthcare': 0, 'Education': 0, 'Others': 0}
        self.user_income = 0.0
        self.budget = {}

    def analyze_transactions(self, transaction_data):
        self.transactions = self.extract_transactions(transaction_data)
        self.categorize_expenses()
        self.generate_visual_reports()

    def extract_transactions(self, transaction_data):
        transactions = [{'amount': transaction['amount'], 'category': transaction['category'],
                         'date': transaction['date']} for transaction in transaction_data]
        return transactions

    def categorize_expenses(self):
        for transaction in self.transactions:
            category = transaction['category']
            self.expense_categories[category] += transaction['amount']

    def generate_visual_reports(self):
        plt.bar(self.expense_categories.keys(),
                self.expense_categories.values())
        plt.xlabel('Expense Category')
        plt.ylabel('Total Amount')
        plt.title('Expense Distribution')
        plt.show()

    def generate_budget_plan(self, income):
        budget = {'Food': 0.2 * income, 'Transportation': 0.1 * income, 'Housing': 0.3 * income, 'Utilities': 0.1 * income,
                  'Entertainment': 0.1 * income, 'Healthcare': 0.1 * income, 'Education': 0.05 * income, 'Savings': 0.05 * income, 'Others': 0.1 * income}
        return budget

    def optimize_budget(self):
        expense_df = pd.DataFrame.from_dict(
            self.expense_categories, orient='index', columns=['Amount'])
        expense_df_sorted = expense_df.sort_values(
            by='Amount', ascending=False)
        highest_expense_category = expense_df_sorted.index[0]
        budget_plan = self.generate_budget_plan(self.user_income)
        if self.expense_categories[highest_expense_category] > budget_plan[highest_expense_category]:
            return f"You are spending more than budgeted on {highest_expense_category}. Reduce your expenses in this category."
        else:
            return "Your budget is well-optimized. Keep up the good work!"

    def monitor_expenses(self):
        for category, amount in self.expense_categories.items():
            if amount >= 0.8 * self.budget[category]:
                self.send_alert(category)

    def send_alert(self, category):
        msg = EmailMessage()
        msg['Subject'] = f"Expense Alert: {category}"
        msg['From'] = 'expensemanager@gmail.com'
        msg['To'] = self.user_email
        msg.set_content(
            f"You have exceeded your budget limit for {category} expenses. Please review your spending.")
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login('expensemanager@gmail.com', 'password')
            smtp.send_message(msg)

    def make_purchase_recommendations(self, user_preferences):
        purchase_recommendations = []
        return purchase_recommendations

    @retry(tries=3, delay=1)
    def fetch_bills(self):
        bills = []
        return bills

    def suggest_savings_investment(self, financial_goals, risk_tolerance):
        savings_investment_recommendations = []
        return savings_investment_recommendations

    def optimize_expenses(self):
        expense_optimization = {}
        return expense_optimization

    def track_financial_goals(self, financial_goals):
        progress = {}
        return progress

    def execute_program(self):
        root = Tk()
        root.title("Expense Manager")

        def select_file():
            file_path = filedialog.askopenfilename()
            transaction_data = self.fetch_transactions(file_path)
            self.analyze_transactions(transaction_data)

        def enter_income():
            self.user_income = float(income_entry.get())
            self.budget = self.generate_budget_plan(self.user_income)
            optimization_result = self.optimize_budget()
            optimization_label.config(text=optimization_result)

        def monitor_expenses_func():
            self.monitor_expenses()
            messagebox.showinfo(
                "Expense Monitoring", "Expense monitoring activated. You will receive alerts if any category exceeds 80% of budget.")

        def purchase_recommendations_func():
            user_preferences = self.get_user_preferences()
            purchase_recommendations = self.make_purchase_recommendations(
                user_preferences)
            recommendation_list.insert(
                END, "\n".join(purchase_recommendations))

        def fetch_bills_func():
            bills = self.fetch_bills()
            bill_list.insert(END, "\n".join(bills))

        def suggest_savings_investment_func():
            financial_goals = self.get_financial_goals()
            risk_tolerance = self.get_risk_tolerance()
            savings_investment_recommendations = self.suggest_savings_investment(
                financial_goals, risk_tolerance)
            suggestion_list.insert(END, "\n".join(
                savings_investment_recommendations))

        def optimize_expenses_func():
            expense_optimization = self.optimize_expenses()
            optimization_list.insert(END, "\n".join(expense_optimization))

        def track_financial_goals_func():
            financial_goals = self.get_financial_goals()
            progress = self.track_financial_goals(financial_goals)
            progress_list.insert(END, "\n".join(progress))

        Label(root, text="Expense Manager", font=("Helvetica", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=10)

        Button(root, text="Select Transaction File", command=select_file).grid(
            row=1, column=0, padx=10, pady=5)
        transaction_label = Label(root, text="Analyzing Transactions...")
        transaction_label.grid(row=1, column=1, padx=10, pady=5)

        income_frame = Frame(root)
        income_frame.grid(row=2, column=0, padx=10, pady=5)
        Label(income_frame, text="Enter Monthly Income:").grid(row=0, column=0)
        income_entry = Entry(income_frame)
        income_entry.grid(row=0, column=1)
        income_button = Button(
            income_frame, text="Submit", command=enter_income)
        income_button.grid(row=0, column=2)
        optimization_label = Label(income_frame, text="")
        optimization_label.grid(row=1, column=0, columnspan=3)

        Button(root, text="Monitor Expenses", command=monitor_expenses_func).grid(
            row=3, column=0, padx=10, pady=5)

        recommendation_frame = Frame(root)
        recommendation_frame.grid(row=4, column=0, padx=10, pady=5)
        Label(recommendation_frame, text="Purchase Recommendations:").grid(
            row=0, column=0)
        recommendation_list = Listbox(recommendation_frame, width=50)
        recommendation_list.grid(row=1, column=0)
        recommendation_button = Button(
            recommendation_frame, text="Get Recommendations", command=purchase_recommendations_func)
        recommendation_button.grid(row=2, column=0)

        bills_frame = Frame(root)
        bills_frame.grid(row=4, column=1, padx=10, pady=5)
        Label(bills_frame, text="Bills:").grid(row=0, column=0)
        bill_list = Listbox(bills_frame, width=50)
        bill_list.grid(row=1, column=0)
        bill_button = Button(
            bills_frame, text="Fetch Bills", command=fetch_bills_func)
        bill_button.grid(row=2, column=0)

        suggestion_frame = Frame(root)
        suggestion_frame.grid(row=5, column=0, padx=10, pady=5)
        Label(suggestion_frame, text="Savings and Investment Suggestions:").grid(
            row=0, column=0)
        suggestion_list = Listbox(suggestion_frame, width=50)
        suggestion_list.grid(row=1, column=0)
        suggestion_button = Button(
            suggestion_frame, text="Get Suggestions", command=suggest_savings_investment_func)
        suggestion_button.grid(row=2, column=0)

        optimization_frame = Frame(root)
        optimization_frame.grid(row=5, column=1, padx=10, pady=5)
        Label(optimization_frame, text="Expense Optimization:").grid(
            row=0, column=0)
        optimization_list =