import csv
import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk


csv_file = 'ap.csv'
plati_file = 'plati.csv'

class ApartamentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Apartament Management System")
        self.root.configure(bg="#f0f0f0")
        self.create_main_menu()

    def create_main_menu(self):
        self.clear_frame()
        tk.Label(self.root, text="==== MENIU PRINCIPAL ====", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

        ttk.Button(self.root, text="Creeaza cont", command=self.sign_up).pack(pady=10, padx=20, fill='x')
        ttk.Button(self.root, text="Intra in cont", command=self.log_in).pack(pady=10, padx=20, fill='x')
        ttk.Button(self.root, text="Iesire", command=self.root.quit).pack(pady=10, padx=20, fill='x')

    def sign_up(self):
        self.clear_frame()
        tk.Label(self.root, text="==== CREEAZA CONT ====", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

        tk.Label(self.root, text="Email:", bg="#f0f0f0").pack()
        email_entry = ttk.Entry(self.root)
        email_entry.pack(pady=5)

        tk.Label(self.root, text="Parola:", bg="#f0f0f0").pack()
        password_entry = ttk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        tk.Label(self.root, text="Numar apartament:", bg="#f0f0f0").pack()
        ap_entry = ttk.Entry(self.root)
        ap_entry.pack(pady=5)

        def submit_signup():
            email = email_entry.get()
            password = password_entry.get()
            ap_number = ap_entry.get()

            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "Email invalid")
                return
            if not any(char.isupper() for char in password):
                messagebox.showerror("Error", "Parola trebuie sa contina cel putin o majuscula")
                return

            with open(csv_file, mode='r', newline='') as file:
                reader = list(csv.DictReader(file))

            apartament_gasit = False
            for row in reader:
                if row['numar'] == ap_number:
                    row['email'] = email
                    row['parola'] = password
                    apartament_gasit = True
                    break

            if apartament_gasit:
                with open(csv_file, mode='w', newline='') as file:
                    fieldnames = reader[0].keys()
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    writer.writerows(reader)
                messagebox.showinfo("Success", "Cont creat.")
                self.create_main_menu()
            else:
                messagebox.showerror("Error", f"Apartamentul {ap_number} nu a fost gasit")

        ttk.Button(self.root, text="Trimite", command=submit_signup).pack(pady=10)

    def log_in(self):
        self.clear_frame()
        tk.Label(self.root, text="==== INTRA IN CONT ====", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

        tk.Label(self.root, text="Email:", bg="#f0f0f0").pack()
        email_entry = ttk.Entry(self.root)
        email_entry.pack(pady=5)

        tk.Label(self.root, text="Parola:", bg="#f0f0f0").pack()
        password_entry = ttk.Entry(self.root, show="*")
        password_entry.pack(pady=5)

        def submit_login():
            login_email = email_entry.get()
            login_password = password_entry.get()

            if login_email == "admin@gmail.com" and login_password == "Admin": #aici trebuie modificata contul administratorului
                messagebox.showinfo("Admin Login", "Ai intrat in contul de administrator")
                with open(csv_file, mode='r', newline='') as file:
                    reader = list(csv.DictReader(file))
                self.admin_menu(reader)
                return

            with open(csv_file, mode='r', newline='') as file:
                reader = list(csv.DictReader(file))
                found = False
                for row in reader:
                    if row['email'] == login_email and row['parola'] == login_password:
                        found = True
                        messagebox.showinfo("Login", f"Logat pentru apartmentul {row['numar']}")
                        self.apartament_menu(row, reader)
                        break

                if not found:
                    messagebox.showerror("Error", "Parola/email incorect")

        ttk.Button(self.root, text="Trimite", command=submit_login).pack(pady=10)

    def apartament_menu(self, apartament_row, reader):
        self.clear_frame()
        tk.Label(self.root, text="=== Meniu apartament ===", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

        def update_apa():
            try:
                apa_noua = simpledialog.askinteger("Citire Apa", "Metri cubi consumati:")
                if apa_noua is not None:
                    apartament_row['apa'] = str(apa_noua)
                    with open(csv_file, mode='w', newline='') as file:
                        fieldnames = reader[0].keys()
                        writer = csv.DictWriter(file, fieldnames=fieldnames)
                        writer.writeheader()
                        writer.writerows(reader)
                    messagebox.showinfo("Success", "Apa citita")
            except ValueError:
                messagebox.showerror("Error", "Introdu un numar")

        ttk.Button(self.root, text="Citire Apa", command=update_apa).pack(pady=5)
        ttk.Button(self.root, text="Log Out", command=self.create_main_menu).pack(pady=5)

    def admin_menu(self, reader):
        self.clear_frame()
        tk.Label(self.root, text="=== Meniu Administrator ===", font=("Helvetica", 16), bg="#f0f0f0").pack(pady=20)

        def show_payments():
            self.calculate_payments(reader)
            messagebox.showinfo("Plati", "Platile au fost trimise in plati.csv.")

        ttk.Button(self.root, text="Trimite plati", command=show_payments).pack(pady=5)
        ttk.Button(self.root, text="Log Out", command=self.create_main_menu).pack(pady=5)

    def calculate_payments(self, reader):
        with open(plati_file, mode='w', newline='') as file:
            fieldnames = ['apartament', 'pret']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

            for row in reader:
                persoane = int(row['persoane'])
                apa = int(row['apa'])
                pret = 32 * persoane + 40 + apa * 15 #formula pretului poate fi modificata aici dupa cerintele fiecarui administrator
                writer.writerow({'apartament': row['numar'], 'pret': pret})

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = tk.Tk()
app = ApartamentApp(root)
root.geometry("400x400")
root.mainloop()
