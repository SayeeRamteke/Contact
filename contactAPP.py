import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


class ContactApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Contact Manager")
        self.contacts = {}  # Dictionary to store contacts
        self.favorites = set()  # Set to store favorite contacts

        # Aesthetic UI styling
        self.root.geometry("500x500")
        self.root.config(bg="#f7f7f7")

        # Title Label
        title_label = tk.Label(self.root, text="Contact Manager", font=("Helvetica", 20, "bold"), bg="#f7f7f7", fg="#333")
        title_label.pack(pady=10)

        # Frame for Contact List
        list_frame = tk.Frame(self.root, bg="#f7f7f7")
        list_frame.pack(fill="both", expand=True, pady=10)

        # Contact List
        self.contact_list = ttk.Treeview(list_frame, columns=("Name", "Phone", "Favorite"), show="headings", height=15)
        self.contact_list.heading("Name", text="Name")
        self.contact_list.heading("Phone", text="Phone")
        self.contact_list.heading("Favorite", text="Favorite")
        self.contact_list.column("Name", anchor="center")
        self.contact_list.column("Phone", anchor="center")
        self.contact_list.column("Favorite", anchor="center")
        self.contact_list.pack(fill="both", expand=True)

        # Add Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.contact_list.yview)
        self.contact_list.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Buttons
        button_frame = tk.Frame(self.root, bg="#f7f7f7")
        button_frame.pack(pady=10)

        add_btn = tk.Button(button_frame, text="Add Contact", command=self.add_contact, bg="#4caf50", fg="white", font=("Helvetica", 12))
        add_btn.grid(row=0, column=0, padx=10)

        fav_btn = tk.Button(button_frame, text="Mark as Favorite", command=self.mark_as_favorite, bg="#2196f3", fg="white", font=("Helvetica", 12))
        fav_btn.grid(row=0, column=1, padx=10)

        dup_btn = tk.Button(button_frame, text="Check Duplicates", command=self.check_duplicates, bg="#ff9800", fg="white", font=("Helvetica", 12))
        dup_btn.grid(row=0, column=2, padx=10)

    def add_contact(self):
        """Adds a new contact to the application."""
        name = simpledialog.askstring("Add Contact", "Enter Contact Name:")
        if not name:
            messagebox.showwarning("Warning", "Name cannot be empty!")
            return

        phone = simpledialog.askstring("Add Contact", "Enter Contact Phone:")
        if not phone:
            messagebox.showwarning("Warning", "Phone number cannot be empty!")
            return

        # Check for duplicates before adding
        if name in self.contacts:
            messagebox.showerror("Error", f"Contact '{name}' already exists.")
            return

        self.contacts[name] = phone
        self.update_contact_list()
        messagebox.showinfo("Success", f"Contact '{name}' added successfully!")

    def mark_as_favorite(self):
        """Marks a selected contact as a favorite."""
        selected = self.contact_list.selection()
        if not selected:
            messagebox.showwarning("Warning", "No contact selected!")
            return

        # Get contact name from selection
        name = self.contact_list.item(selected[0], "values")[0]
        if name not in self.contacts:
            messagebox.showerror("Error", "Contact not found!")
            return

        self.favorites.add(name)
        self.update_contact_list()
        messagebox.showinfo("Success", f"Contact '{name}' marked as favorite!")

    def check_duplicates(self):
        """Checks for duplicate phone numbers in the contact list."""
        phone_numbers = {}
        duplicates = []

        for name, phone in self.contacts.items():
            if phone in phone_numbers:
                duplicates.append(f"{name} ({phone})")
            else:
                phone_numbers[phone] = name

        if duplicates:
            duplicate_msg = "Duplicate Contacts Found:\n" + "\n".join(duplicates)
            messagebox.showwarning("Duplicates", duplicate_msg)
        else:
            messagebox.showinfo("No Duplicates", "No duplicate contacts found!")

    def update_contact_list(self):
        """Updates the contact list display."""
        for row in self.contact_list.get_children():
            self.contact_list.delete(row)

        for name, phone in self.contacts.items():
            favorite_status = "Yes" if name in self.favorites else "No"
            self.contact_list.insert("", "end", values=(name, phone, favorite_status))


if __name__ == "__main__":
    root = tk.Tk()
    app = ContactApp(root)
    root.mainloop()
