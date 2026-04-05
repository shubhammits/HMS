from tkinter import *
from tkinter import ttk, messagebox
import mysql.connector
from tkcalendar import DateEntry

# ================= DATABASE SETTINGS =================
# Yahan apni details ek baar change kar lo, poore app mein update ho jayegi
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "12345",
    "database": "hospital_db"
}

# ================= LOGIN CLASS =================
class LoginSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Login")
        self.root.geometry("400x500+550+150")
        self.root.configure(bg="#2f3640")

        self.username = StringVar()
        self.password = StringVar()

        # UI Design
        Label(self.root, text="ADMIN LOGIN", font=("arial", 22, "bold"), bg="#2f3640", fg="#fbc531").pack(pady=40)
        
        frame = Frame(self.root, bg="white", bd=2, relief=RIDGE, padx=20, pady=20)
        frame.place(x=50, y=120, width=300, height=300)

        Label(frame, text="Username", font=("arial", 12, "bold"), bg="white").pack(pady=5)
        Entry(frame, textvariable=self.username, font=("arial", 12), width=25, bd=2).pack(pady=5)

        Label(frame, text="Password", font=("arial", 12, "bold"), bg="white").pack(pady=5)
        Entry(frame, textvariable=self.password, font=("arial", 12), width=25, bd=2, show="*").pack(pady=5)

        Button(frame, text="LOGIN", command=self.login_action, bg="#44bd32", fg="white", 
               font=("arial", 12, "bold"), width=15, cursor="hand2").pack(pady=30)

    def login_action(self):
        # Default credentials (You can also fetch these from a 'users' table)
        if self.username.get() == "admin" and self.password.get() == "12345":
            self.root.destroy() # Login window band karo
            main_root = Tk()
            MedicineInventory(main_root) # Inventory kholo
            main_root.mainloop()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

# ================= MAIN INVENTORY CLASS =================
class MedicineInventory:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy Inventory System")
        self.root.state('zoomed')
        self.root.configure(bg="#f5f6fa")

        # --- Variables ---
        self.med_id = StringVar()
        self.med_name = StringVar()
        self.company_name = StringVar()
        self.category = StringVar()
        self.hsn_code = StringVar()
        self.rack_number = StringVar()
        self.batch_no = StringVar()
        self.expiry_date = StringVar()
        self.mrp = DoubleVar()
        self.price_per_unit = DoubleVar()
        self.tax_percent = IntVar(value=12)
        self.stock_qty = IntVar()
        self.min_stock_level = IntVar(value=10)
        self.search_by = StringVar()
        self.search_txt = StringVar()

        # Title
        Label(self.root, text="MEDICINE STOCK MANAGEMENT", font=("times new roman", 30, "bold"), 
              bg="#2f3640", fg="#fbc531", pady=10).pack(side=TOP, fill=X)

        # Main Frame
        Main_Frame = Frame(self.root, bg="#f5f6fa")
        Main_Frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Left Side: Entry Form
        Entry_Frame = LabelFrame(Main_Frame, text="Medicine Details", font=("arial", 12, "bold"), 
                                 bg="white", fg="#2f3640", bd=2, relief=RIDGE)
        Entry_Frame.place(x=0, y=0, width=450, height=650)

        labels = ["Medicine Name", "Company", "Category", "HSN Code", "Rack No", "Batch No", 
                  "Expiry Date", "MRP", "Price/Unit", "Tax (%)", "Stock Qty", "Min Stock"]
        vars = [self.med_name, self.company_name, self.category, self.hsn_code, self.rack_number, 
                self.batch_no, self.expiry_date, self.mrp, self.price_per_unit, self.tax_percent, 
                self.stock_qty, self.min_stock_level]

        for i, label in enumerate(labels):
            Label(Entry_Frame, text=label, font=("arial", 11, "bold"), bg="white").grid(row=i, column=0, padx=10, pady=8, sticky=W)
            if label == "Expiry Date":
                DateEntry(Entry_Frame, textvariable=vars[i], width=20, font=("arial", 11), date_pattern='yyyy-mm-dd').grid(row=i, column=1, padx=10, pady=8)
            else:
                Entry(Entry_Frame, textvariable=vars[i], font=("arial", 11), width=22, bd=2, relief=GROOVE).grid(row=i, column=1, padx=10, pady=8)

        Btn_Frame = Frame(Entry_Frame, bg="white")
        Btn_Frame.place(x=10, y=550, width=420, height=80)

        Button(Btn_Frame, text="Add Stock", command=self.add_medicine, bg="#44bd32", fg="white", font=("arial", 11, "bold"), width=9).grid(row=0, column=0, padx=5)
        Button(Btn_Frame, text="Update", command=self.update_medicine, bg="#0097e6", fg="white", font=("arial", 11, "bold"), width=9).grid(row=0, column=1, padx=5)
        Button(Btn_Frame, text="Delete", command=self.delete_medicine, bg="#e84118", fg="white", font=("arial", 11, "bold"), width=9).grid(row=0, column=2, padx=5)
        Button(Btn_Frame, text="Clear", command=self.clear_form, bg="#718093", fg="white", font=("arial", 11, "bold"), width=9).grid(row=0, column=3, padx=5)

        # Right Side Table Area
        Table_Frame = Frame(Main_Frame, bg="white", bd=2, relief=RIDGE)
        Table_Frame.place(x=470, y=0, width=880, height=650)

        Search_Bar = Frame(Table_Frame, bg="#dcdde1")
        Search_Bar.pack(side=TOP, fill=X)
        
        self.search_combo = ttk.Combobox(Search_Bar, textvariable=self.search_by, values=("med_name", "batch_no", "rack_number"), state="readonly", width=15)
        self.search_combo.grid(row=0, column=1, padx=5, pady=10)
        Entry(Search_Bar, textvariable=self.search_txt, font=("arial", 11), width=20).grid(row=0, column=2, padx=5)
        Button(Search_Bar, text="Search", command=self.search_data, bg="#8c7ae6", fg="white", width=10).grid(row=0, column=3, padx=5)
        Button(Search_Bar, text="Show All", command=self.fetch_data, bg="#7f8c8d", fg="white", width=10).grid(row=0, column=4, padx=5)

        scroll_x = Scrollbar(Table_Frame, orient=HORIZONTAL)
        scroll_y = Scrollbar(Table_Frame, orient=VERTICAL)
        columns = ("id", "name", "company", "cat", "hsn", "rack", "batch", "exp", "mrp", "price", "tax", "stock", "min")
        self.med_table = ttk.Treeview(Table_Frame, columns=columns, xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X); scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.med_table.xview); scroll_y.config(command=self.med_table.yview)

        headings = ["ID", "Name", "Company", "Category", "HSN", "Rack", "Batch", "Expiry", "MRP", "Price", "Tax%", "Stock", "Min"]
        for i, col in enumerate(columns):
            self.med_table.heading(col, text=headings[i])
            self.med_table.column(col, width=80)

        self.med_table['show'] = 'headings'
        self.med_table.pack(fill=BOTH, expand=1)
        self.med_table.bind("<ButtonRelease-1>", self.get_cursor)
        
        self.fetch_data()

    # --- Functions with Centralized Credentials ---
    def get_connection(self):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except Exception as e:
            messagebox.showerror("Database Error", f"Connection Failed: {e}")
            return None

    def add_medicine(self):
        if self.med_name.get() == "":
            messagebox.showerror("Error", "Medicine Name is required!")
            return
        conn = self.get_connection()
        if conn:
            curr = conn.cursor()
            curr.execute("INSERT INTO medicines (med_name, company_name, category, hsn_code, rack_number, batch_no, expiry_date, mrp, price_per_unit, tax_percent, stock_qty, min_stock_level) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                self.med_name.get(), self.company_name.get(), self.category.get(), self.hsn_code.get(),
                self.rack_number.get(), self.batch_no.get(), self.expiry_date.get(), self.mrp.get(),
                self.price_per_unit.get(), self.tax_percent.get(), self.stock_qty.get(), self.min_stock_level.get()
            ))
            conn.commit(); self.fetch_data(); self.clear_form(); conn.close()
            messagebox.showinfo("Success", "Added Successfully")

    def fetch_data(self):
        conn = self.get_connection()
        if conn:
            curr = conn.cursor()
            curr.execute("SELECT * FROM medicines")
            rows = curr.fetchall()
            self.med_table.delete(*self.med_table.get_children())
            for row in rows:
                self.med_table.insert('', END, values=row)
            conn.close()

    def get_cursor(self, ev):
        cursor_row = self.med_table.focus()
        content = self.med_table.item(cursor_row)
        row = content['values']
        if row:
            self.med_id.set(row[0]); self.med_name.set(row[1]); self.company_name.set(row[2])
            self.category.set(row[3]); self.hsn_code.set(row[4]); self.rack_number.set(row[5])
            self.batch_no.set(row[6]); self.expiry_date.set(row[7]); self.mrp.set(row[8])
            self.price_per_unit.set(row[9]); self.tax_percent.set(row[10])
            self.stock_qty.set(row[11]); self.min_stock_level.set(row[12])

    def update_medicine(self):
        conn = self.get_connection()
        if conn:
            curr = conn.cursor()
            curr.execute("UPDATE medicines SET med_name=%s, company_name=%s, category=%s, hsn_code=%s, rack_number=%s, batch_no=%s, expiry_date=%s, mrp=%s, price_per_unit=%s, tax_percent=%s, stock_qty=%s, min_stock_level=%s WHERE med_id=%s", (
                self.med_name.get(), self.company_name.get(), self.category.get(), self.hsn_code.get(),
                self.rack_number.get(), self.batch_no.get(), self.expiry_date.get(), self.mrp.get(),
                self.price_per_unit.get(), self.tax_percent.get(), self.stock_qty.get(), self.min_stock_level.get(),
                self.med_id.get()
            ))
            conn.commit(); self.fetch_data(); conn.close()
            messagebox.showinfo("Success", "Updated Successfully")

    def delete_medicine(self):
        if self.med_id.get() == "": return
        if messagebox.askyesno("Confirm", "Delete this medicine?"):
            conn = self.get_connection()
            if conn:
                curr = conn.cursor()
                curr.execute("DELETE FROM medicines WHERE med_id=%s", (self.med_id.get(),))
                conn.commit(); conn.close(); self.fetch_data(); self.clear_form()

    def search_data(self):
        conn = self.get_connection()
        if conn:
            curr = conn.cursor()
            curr.execute(f"SELECT * FROM medicines WHERE {self.search_by.get()} LIKE '%{self.search_txt.get()}%'")
            rows = curr.fetchall()
            self.med_table.delete(*self.med_table.get_children())
            for row in rows: self.med_table.insert('', END, values=row)
            conn.close()

    def clear_form(self):
        self.med_id.set(""); self.med_name.set(""); self.company_name.set("")
        self.category.set(""); self.hsn_code.set(""); self.rack_number.set("")
        self.batch_no.set(""); self.mrp.set(0.0); self.price_per_unit.set(0.0)
        self.tax_percent.set(12); self.stock_qty.set(0); self.min_stock_level.set(10)

# --- App Start ---
if __name__ == "__main__":
    root = Tk()
    login = LoginSystem(root)
    root.mainloop()