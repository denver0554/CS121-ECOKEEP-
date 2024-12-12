import tkinter as tk
from tkinter import messagebox
from datetime import datetime


class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to ecoKeep: Food Inventory Management System")

        #main window frame
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.root.configure(bg="dark gray")

        #inventory list
        self.inventory = []

        
        #input fields
        main_frame = tk.Frame(root, width=600, height=200)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        main_frame.configure(bg="beige")


        tk.Label(main_frame, text="ecoKeep: Food Inventory System", font=("Arial", 16)).pack(pady=10)

        #name input
        tk.Label(main_frame, text="Name:").pack()
        self.name_entry = tk.Entry(main_frame, width=40)
        self.name_entry.pack()

        #expiration date input
        tk.Label(main_frame, text="Expiration Date (YYYY-MM-DD):").pack()
        self.expiration_entry = tk.Entry(main_frame, width=40)
        self.expiration_entry.pack()

        #quantity input
        tk.Label(main_frame, text="Quantity:").pack()
        self.quantity_entry = tk.Entry(main_frame, width=40)
        self.quantity_entry.pack()

        #category input
        tk.Label(main_frame, text="Category (P for Perishable, N for Non-Perishable):").pack()
        self.category_entry = tk.Entry(main_frame, width=40)
        self.category_entry.pack()

        #store input
        tk.Label(main_frame, text="Store Name:").pack()
        self.store_entry = tk.Entry(main_frame, width=40)
        self.store_entry.pack()

        #buttons
        tk.Button(main_frame, text="Add Item", command=self.add_item).pack(pady=5)
        tk.Button(main_frame, text="Show Inventory", command=self.show_inventory).pack(pady=5)
        tk.Button(main_frame, text="Clear Expired Items", command=self.clear_expired_items).pack(pady=5)
        tk.Button(main_frame, text="Delete Item", command=self.delete_item).pack(pady=5)

        #inventory display
        self.output_box = tk.Text(main_frame, height=10, width=80)
        self.output_box.pack(pady=10)

    def add_item(self):
        name = self.name_entry.get()
        expiration = self.expiration_entry.get()
        quantity = self.quantity_entry.get()
        category_input = self.category_entry.get().strip().upper()
        store = self.store_entry.get()

        if not name or not expiration or not quantity or not category_input or not store:
            messagebox.showerror("Error", "All fields are required!")
            return

        #determine the category type
        if category_input == "P":
            category = "Perishable"
        elif category_input == "N":
            category = "Non-Perishable"
        else:
            messagebox.showerror("Error", "Invalid category! Use 'P' for Perishable or 'N' for Non-Perishable.")
            return

        try:
            expiration_date = datetime.strptime(expiration, "%Y-%m-%d").date()
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Error", "Invalid date or quantity format!")
            return

        #add item to inventory
        self.inventory.append({
            "name": name,
            "expiration_date": expiration_date,
            "quantity": quantity,
            "category": category,
            "store": store
        })

        messagebox.showinfo("Success", f"Added '{name}' to inventory!")
        self.clear_inputs()

    def show_inventory(self):
        self.output_box.delete("1.0", tk.END)

        if not self.inventory:
            self.output_box.insert(tk.END, "No items in inventory.\n")
            return

        for item in self.inventory:
            name = item["name"]
            expiration_date = item["expiration_date"]
            quantity = item["quantity"]
            category = item["category"]
            store = item["store"]
            days_to_expire = (expiration_date - datetime.now().date()).days
            if days_to_expire <= 0:
                status = "Warning the item has Expired"
            elif days_to_expire <= 5:
                status = f"Warning this item is Expiring in {days_to_expire} days, consider using it soon"
            else:
                status = f"This item is not expiring soon, {days_to_expire} days remaining"

            self.output_box.insert(
            tk.END,
            f"Name: {name}\nCategory: {category}\nStore: {store}\nQuantity: {quantity}\n"
            f"Expiration Date: {expiration_date}\nStatus: {status}\n\n"
        )
               
    def clear_expired_items(self):
        #remove expired items from inventory
        today = datetime.now().date()
        print(f"Today's Date: {today}")
        initial_count = len(self.inventory)
        self.inventory = [item for item in self.inventory if item["expiration_date"] > today]
    
        print(f"Remaining Items: {self.inventory}")
    
        cleared_count = initial_count - len(self.inventory)

        #show message info
        messagebox.showinfo("Info:", f"Cleared {cleared_count} expired items!")
    
        #display the updated inventory
        self.show_inventory()


    def delete_item(self):
        name = self.name_entry.get()
        if not name:
            messagebox.showerror("Error:", "Enter the name of the item to delete.")
            return

    #confirmation before deleting
        confirmation = messagebox.askyesno("Delete Confirmation", f"Are you sure you want to delete this from the inventory?")
        if confirmation:
        #DELETE ITEMS
            initial_count = len(self.inventory)
            self.inventory = [item for item in self.inventory if item["name"] != name]
            deleted_count = initial_count - len(self.inventory)

            if deleted_count == 0:
                messagebox.showerror("Error:", f"Item '{name}' not found in inventory.")
            else:
                messagebox.showinfo("Success:", f"Deleted {deleted_count} item(s) named '{name}' from inventory.")
            self.show_inventory()


    def clear_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.expiration_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.store_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
