"""
Author:  Maxine Staser-Miller
Date written: 5/10/2025
Assignment: Module 08 Final Project
Description: POS system / cash register for a gas station. Must include the ability to add custom items, manage gas-pumps, handle age-verification for tobacco and lottery purchases, calculate the total and change due, and print a receipt. It also needs to keep a running total of sales for the day and print a report at the end of the day. 

"""

import datetime
import tkinter as tk
import tkinter.messagebox

class POSSystem:
    def __init__(self): # Initialize the POS system
        self.initializeSale()
        self.initializeGUI()
        self.gasPricePerGallon = 3.00 # Default gas price 
        self.totalSales = 0.0 # Total sales for the day
    def initializeGUI(self): # Create the main window
        self.root = tk.Tk()
        self.root.title("POS System")
        self.root.resizable(False, False)

        # Create buttons for different actions
        button_labels = [
            "Pump 1", "Pump 2", "Pump 3", "Pump 4",
            "Tobacco", "Lottery", "Soda", "Lunch",
            "Gas Prices", "Print Receipt", "Delete Last Item", "Add Item",
            "End Day", "Cancel Sale", "Cash", "Credit"
        ]
        button_commands = [
            lambda: self.addGasWindow(1), lambda: self.addGasWindow(2), lambda: self.addGasWindow(3), lambda: self.addGasWindow(4),
            self.addTobacco, self.addLottery, self.addSoda, self.addLunchWindow,
            self.gasSettings, self.printReceipt, self.deleteLastItem, self.addItem,
            self.endOfDayReport, self.cancelSale, self.payWithCash, self.payWithCard
        ]

        for i, label in enumerate(button_labels):
            button = tk.Button(self.root, text=label, width=10, height=2, command=button_commands[i])
            button.grid(row=i // 4, column=i % 4, padx=5, pady=5)

        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.root)
        button_frame.grid(row=0, column=1, padx=10, pady=10, sticky="n")

        # Create a frame to display items in the current sale
        sale_frame = tk.Frame(self.root)
        sale_frame.grid(row=0, column=4, padx=10, pady=10, rowspan=4, sticky="n")

        # Add a label for the sale frame
        sale_label = tk.Label(sale_frame, text="Current Sale", font=("Arial", 14))
        sale_label.pack(pady=5)

        # Create a listbox to display the items
        self.sale_listbox = tk.Listbox(sale_frame, width=30, height=15)
        self.sale_listbox.pack(padx=5, pady=5)

        # Add a label to display the running total
        self.total_label = tk.Label(sale_frame, text="Total: $0.00", font=("Arial", 12))
        self.total_label.pack(pady=5)
    def initializeSale(self): # Initialize a new sale
        self.items = [] # List to hold items in the current sale
        self.total = 0.0 # Total amount for the current sale
        self.ageVerified = False # Age verification status for tobacco and lottery purchases
    def updateTotal(self): # Updates the total amount for the current sale and refreshes the listbox.
        self.total = sum(item[1] for item in self.items)
        self.sale_listbox.delete(0, tk.END)
        for item in self.items:
            self.sale_listbox.insert(tk.END, f" {item[0]:<20}{item[1]:>30}")
        self.total_label.config(text=f"Total: ${self.total}")

################ PAYMENT FUNCTIONS #################

    def payWithCard(self): # Process payment with a credit card and reinitialize the sale.
        if self.total > 0:
            self.totalSales += self.total
            self.printReceipt()
            self.initializeSale()
            self.updateTotal()
            tk.messagebox.showinfo("Payment", "Payment successful. Thank you!")
        else:
            tk.messagebox.showwarning("No Items", "No items to pay for.")
    def payWithCash(self): # Process payment with cash and reinitialize the sale.
        if self.total > 0:
            cash_window = tk.Toplevel(self.root)
            cash_window.title("Cash Payment")
            cash_window.geometry("300x200")
            cash_window.resizable(False, False)

            tk.Label(cash_window, text="Enter Cash Amount:").pack(pady=5)
            cash_entry = tk.Entry(cash_window)
            cash_entry.pack(pady=5)

            def process_cash_payment(): # Logic to process the cash payment. It checks if the cash amount is sufficient and calculates the change due.
                try: 
                    cash_amount = float(cash_entry.get())
                    if cash_amount >= self.total:
                        change = cash_amount - self.total
                        tk.messagebox.showinfo("Change Due", f"Payment successful. Change due: ${change:.2f}")
                        self.totalSales += self.total
                        self.printReceipt()
                        self.initializeSale()
                        self.updateTotal()
                        cash_window.destroy()
                    else:
                        tk.messagebox.showerror("Insufficient Cash", "The cash amount is less than the total.")
                        cash_entry.delete(0, tk.END)
                except ValueError:
                    tk.messagebox.showerror("Invalid Input", "Please enter a valid number for the cash amount.")
                    cash_entry.delete(0, tk.END)

            tk.Button(cash_window, text="Submit", command=process_cash_payment).pack(pady=10)
        else:
            tk.messagebox.showwarning("No Items", "No items to pay for.")
    def cancelSale(self): # Cancels the current sale.
        self.initializeSale()
        self.updateTotal()
        tk.messagebox.showinfo("Sale Cancelled", "Sale has been cancelled.")

################ RECEIPT AND REPORT FUNCTIONS #################

    def printReceipt(self): # Prints a receipt for the current sale.
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title("Receipt")
        receipt_window.resizable(False, False)

        receipt_text = tk.Text(receipt_window, width=40, height=20)
        receipt_text.pack(padx=10, pady=10)

        receipt_text.insert(tk.END, "Receipt\n")
        receipt_text.insert(tk.END, "-" * 30 + "\n")
        for item in self.items:
            receipt_text.insert(tk.END, f"{item[0]:<20} ${item[1]:.2f}\n")
        receipt_text.insert(tk.END, "-" * 30 + "\n")
        receipt_text.insert(tk.END, f"Total: ${self.total:.2f}\n")

        receipt_text.config(state=tk.DISABLED)

        close_button = tk.Button(receipt_window, text="Close", command=receipt_window.destroy)
        close_button.pack(pady=5)        
    def endOfDayReport(self): # Prints a report of the total sales for the day and sets total sales to zero.
        report_window = tk.Toplevel(self.root)
        report_window.title("End of Day Report")
        report_window.resizable(False, False)

        report_text = tk.Text(report_window, width=40, height=20)
        report_text.pack(padx=10, pady=10)

        report_text.insert(tk.END, "End of Day Report\n")
        report_text.insert(tk.END, "-" * 30 + "\n")
        report_text.insert(tk.END, f"Total Sales: ${self.totalSales:.2f}\n")
        report_text.insert(tk.END, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report_text.insert(tk.END, "-" * 30 + "\n")

        report_text.config(state=tk.DISABLED)

        close_button = tk.Button(report_window, text="Close", command=report_window.destroy)
        close_button.pack(pady=5)
        self.totalSales = 0.0


################# GAS PUMP FUNCTIONS #################
 
    def addGasWindow(self, pump_number): # Create a new window where you can enter the amount of gas purchased by either gallons or dollars. 
        self.gas_window = tk.Toplevel(self.root)
        self.gas_window.title(f"Pump {pump_number} - Gas Sale")
        self.gas_window.geometry("300x200")
        self.gas_window.resizable(False, False)
        self.gas_label = tk.Label(self.gas_window, text="Enter Gallons or Dollars:")
        self.gas_label.pack(pady=5)
        self.gas_entry = tk.Entry(self.gas_window)
        self.gas_entry.pack(pady=5)
        self.gas_type = tk.StringVar(value="gallons")
        self.gas_type_frame = tk.Frame(self.gas_window)
        self.gas_type_frame.pack(pady=5)
        self.gas_type_gallons = tk.Radiobutton(self.gas_type_frame, text="Gallons", variable=self.gas_type, value="gallons")
        self.gas_type_gallons.pack(side=tk.LEFT)
        self.gas_type_dollars = tk.Radiobutton(self.gas_type_frame, text="Dollars", variable=self.gas_type, value="dollars")
        self.gas_type_dollars.pack(side=tk.LEFT)
        self.gas_button = tk.Button(self.gas_window, text="Add Gas", command=lambda: self.processGas(pump_number))
        self.gas_button.pack(pady=5)
    def processGas(self, pump_number): # Process the gas sale based on the input from the user. If the user enters gallons, the sale price is calculated by multiplying the gallons by the price per gallon. If the user enters dollars, the gallons are calculated by dividing the dollars by the price per gallon.
        try:
            amount = float(self.gas_entry.get())
            if amount <= 0:
                tk.messagebox.showerror("Invalid Input", "Please enter a positive number for gallons or dollars.")
                self.gas_entry.delete(0, tk.END)
                return
            if self.gas_type.get() == "gallons":
                price = amount * self.gasPricePerGallon
                self.items.append((f"Pump {pump_number} {amount} Gallons", price))
            else:
                self.items.append((f"Pump {pump_number} Gas", amount))
            self.updateTotal()
            self.gas_window.destroy()
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid number for gallons or dollars.")
            self.gas_entry.delete(0, tk.END)
    def gasSettings(self): # Create a new window where you can set the price of gas.
        self.gas_window = tk.Toplevel(self.root)
        self.gas_window.title("Gas Settings")
        self.gas_window.geometry("300x200")
        self.gas_window.resizable(False, False)
        self.gas_price_label = tk.Label(self.gas_window, text="Enter Gas Price:")
        self.gas_price_label.pack(pady=5)
        self.gas_price_entry = tk.Entry(self.gas_window)
        self.gas_price_entry.pack(pady=5)
        self.gas_price_button = tk.Button(self.gas_window, text="Set Price", command=self.setGasPrice)
        self.gas_price_button.pack(pady=5)
    def setGasPrice(self): # Sets the price of gas
        try:
            new_price = float(self.gas_price_entry.get())
            if new_price > 0:
                self.gasPricePerGallon = new_price
                tk.messagebox.showinfo("Success", f"Gas price updated to ${new_price:.2f} per gallon.")
                self.gas_window.destroy()
            else:
                tk.messagebox.showerror("Invalid Input", "Please enter a positive number for the gas price.")
                self.gas_price_entry.delete(0, tk.END)
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid number for the gas price.")
            self.gas_price_entry.delete(0, tk.END)

################# TOBACCO AND LOTTERY FUNCTIONS #################

    def ageVerification(self): # Create a new window for age verification. Appears when the user tries to add tobacco or lottery items to the sale but hasn't verified their age yet. The ageVerified variable is reset only upon sale completion -- it's part of initializeSale() -- meaning you can add multiple tobacco or lottery items to the sale without having to verify your age each time.
        self.age_verification_window = tk.Toplevel(self.root)
        self.age_verification_window.title("Age Verification")
        self.age_verification_window.geometry("300x200")
        self.age_verification_window.resizable(False, False)

        tk.Label(self.age_verification_window, text="Enter Birth Year (YYYY):").pack(pady=5)
        year_entry = tk.Entry(self.age_verification_window)
        year_entry.pack(pady=5)

        tk.Label(self.age_verification_window, text="Enter Birth Month and Day (MM-DD):").pack(pady=5)
        month_day_entry = tk.Entry(self.age_verification_window)
        month_day_entry.pack(pady=5)

        def verify_age(): # Verify the age based on the input from the user. The user must enter their birth year and month-day in the format YYYY and MM-DD. The program will calculate the age and check if it's 21 or older.
            try:
                birth_year = int(year_entry.get())
                birth_month_day = month_day_entry.get()
                birth_date = datetime.datetime.strptime(f"{birth_year}-{birth_month_day}", "%Y-%m-%d")
                today = datetime.datetime.now()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                if age >= 21:
                    tk.messagebox.showinfo("Age Verification", "Age verified: Over 21.")
                    self.age_verification_window.destroy()
                    self.ageVerified = True
                else:
                    tk.messagebox.showerror("Age Verification", "Age verification failed: Under 21.")
                    self.ageVerified = False
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please enter a valid date in the format YYYY and MM-DD.")
                self.ageVerified = False

        verify_button = tk.Button(self.age_verification_window, text="Verify", command=lambda: verify_age())
        verify_button.pack(pady=10)
    def addTobacco(self): # Adds tobacco to the sale if age is verified. If not, it calls the age verification function.
        if self.ageVerified:
            self.items.append(("Cigarettes", 8.00))
            self.updateTotal()
        else:
            self.ageVerification()
    def addLottery(self): # Adds a lottery ticket to the sale if age is verified.
        if self.ageVerified:
            self.items.append(("Lottery Ticket", 2.00))
            self.updateTotal()
        else:
            self.ageVerification()

################ QUICK ADD FUNCTIONS #################

    def addSoda(self): # Quickly add a fountain drink to the sale.
        self.items.append(("Fountain Drink", 1.25))
        self.updateTotal()
    def addLunchWindow(self): # Creates a window where you can add common lunch items to the sale.
        self.lunch_window = tk.Toplevel(self.root)
        self.lunch_window.title("Lunch Menu")

        def add_lunch_item(item_name, price):
            self.items.append((item_name, price))
            self.updateTotal()
            self.lunch_window.destroy()

        # Create buttons for lunch items
        lunch_items = [
            ("Hamburger", 5.00),
            ("Combo Meal", 7.50),
            ("French Fries", 2.50),
            ("BLT Sandwich", 4.00)
        ]

        for item_name, price in lunch_items:
            button = tk.Button(self.lunch_window, text=item_name, width=15, height=2,
                       command=lambda name=item_name, cost=price: add_lunch_item(name, cost))
            button.pack(pady=5)

############### CUSTOM ITEM FUNCTIONS #################

    def addItem(self): # Create a new window where you can add a custom item to the sale.
        self.custom_item_window = tk.Toplevel(self.root)
        self.custom_item_window.title("Add Custom Item")
        self.custom_item_window.geometry("300x200")
        self.custom_item_window.resizable(False, False)

        # Create labels and entry fields for item name and price
        item_name_label = tk.Label(self.custom_item_window, text="Item Name:")
        item_name_label.pack(pady=5)
        item_name_entry = tk.Entry(self.custom_item_window)
        item_name_entry.pack(pady=5)

        item_price_label = tk.Label(self.custom_item_window, text="Item Price:")
        item_price_label.pack(pady=5)
        item_price_entry = tk.Entry(self.custom_item_window)
        item_price_entry.pack(pady=5)

        # Function to add the custom item
        def add_custom_item():
            try:
                item_name = item_name_entry.get()
                item_price = float(item_price_entry.get())
                if item_name and item_price >= 0:
                    self.items.append((item_name, item_price))
                    self.updateTotal()
                    self.custom_item_window.destroy()
                else:
                    tk.messagebox.showerror("Invalid Input", "Please enter a valid item name and a non-negative price.")
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please enter a valid number for the price.")
                item_price_entry.delete(0, tk.END)

        # Add a button to confirm the addition of the custom item
        add_button = tk.Button(self.custom_item_window, text="Add Item", command=add_custom_item)
        add_button.pack(pady=10)
    def deleteLastItem(self): # Deletes the last item added to the sale.
        if self.items:
            self.items.pop()
            self.updateTotal()
        else:
            tk.messagebox.showwarning("No Items", "No items to delete.")

def main():
    POSSystem().root.mainloop()

if __name__ == "__main__":
    main()

