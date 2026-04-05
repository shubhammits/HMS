from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
import tempfile
from tkcalendar import DateEntry

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Pharmacy & HMS Login")
        self.root.geometry("400x500+550+150")
        self.root.configure(bg="#1e272e")
        self.user = StringVar()
        self.pswd = StringVar()

        Label(self.root, text="ADMIN LOGIN", font=("arial", 22, "bold"), bg="#1e272e", fg="#2ed573").pack(pady=40)
        frame = Frame(self.root, bg="#2f3542", bd=2, relief=RIDGE, padx=20, pady=20)
        frame.place(x=50, y=120, width=300, height=320)

        Label(frame, text="Username", font=("arial", 12), bg="#2f3542", fg="white").pack(pady=5)
        Entry(frame, textvariable=self.user, font=("arial", 12), width=25).pack(pady=5)
        Label(frame, text="Password", font=("arial", 12), bg="#2f3542", fg="white").pack(pady=5)
        Entry(frame, textvariable=self.pswd, font=("arial", 12), width=25, show="*").pack(pady=5)

        Button(frame, text="LOGIN", command=self.login_action, bg="#2ed573", fg="white", font=("arial", 12, "bold"), width=15, cursor="hand2").pack(pady=20)
        Button(frame, text="REGISTER", command=self.register_action, bg="#57606f", fg="white", cursor="hand2").pack()

    def register_action(self):
        if self.user.get() == "" or self.pswd.get() == "":
            messagebox.showerror("Error", "All fields required")
            return
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            curr = conn.cursor()
            curr.execute("CREATE TABLE IF NOT EXISTS users (username VARCHAR(50) PRIMARY KEY, password VARCHAR(50))")
            curr.execute("INSERT INTO users VALUES(%s,%s)", (self.user.get(), self.pswd.get()))
            conn.commit(); conn.close()
            messagebox.showinfo("Success", "Registered! Now Login.")
        except: messagebox.showerror("Error", "User exists")

    def login_action(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            curr = conn.cursor()
            curr.execute("SELECT * FROM users WHERE username=%s AND password=%s", (self.user.get(), self.pswd.get()))
            if curr.fetchone():
                self.root.destroy()
                main_win = Tk()
                Hospital(main_win)
                main_win.mainloop()
            else: messagebox.showerror("Error", "Invalid Login")
            conn.close()
        except: messagebox.showerror("Error", "DB Fail")

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Hospital Management System")
        self.root.state('zoomed') 
        self.root.configure(bg="#1e272e")

        # Variables
        self.Nameoftablets = StringVar()
        self.ref = StringVar()
        self.Dose = StringVar()
        self.NumberofTablets = StringVar()
        self.Lot = StringVar()
        self.Issuedate = StringVar()
        self.ExpDate = StringVar()
        self.DailyDose = StringVar()
        self.StorageAdvice = StringVar()
        self.nhsNumber = StringVar()
        self.PatientName = StringVar()
        self.DateOfBirth = StringVar()
        self.PatientAddress = StringVar()
        self.unit_price = 10.0

        lbltitle = Label(self.root, text="HOSPITAL MANAGEMENT & PHARMACY SYSTEM",
                         fg="#2ed573", bg="#2f3542", font=("arial", 35, "bold"), pady=10)
        lbltitle.pack(side=TOP, fill=X)

        Main_Frame = Frame(self.root, bg="#1e272e")
        Main_Frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        Dataframe = Frame(Main_Frame, bg="#1e272e")
        Dataframe.pack(side=TOP, fill=X)

        # UI Layout Adjustment
        DataframeLeft = LabelFrame(Dataframe, bd=2, relief=RIDGE, padx=20, pady=10, bg="#2f3542",
                                   fg="#2ed573", font=("arial", 12, "bold"), text="Entry Form")
        DataframeLeft.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        DataframeRight = LabelFrame(Dataframe, bd=2, relief=RIDGE, padx=10, bg="#2f3542",
                                    fg="#2ed573", font=("arial", 12, "bold"), text="Prescription / Bill")
        DataframeRight.pack(side=RIGHT, fill=Y, padx=5)

        lbl_opts = {"bg": "#2f3542", "fg": "white", "font": ("arial", 11, "bold")}
        cmb_opts = {"font": ("arial", 11), "width": 25}

        # Row 0
        Label(DataframeLeft, text="Medicine Name", **lbl_opts).grid(row=0, column=0, sticky=W, pady=8)
        self.combo_med = ttk.Combobox(DataframeLeft, textvariable=self.Nameoftablets, **cmb_opts)
        self.combo_med.grid(row=0, column=1, padx=10)
        self.combo_med.bind("<<ComboboxSelected>>", self.get_med_details)

        Label(DataframeLeft, text="Reference No", **lbl_opts).grid(row=0, column=2, sticky=W, padx=10)
        Entry(DataframeLeft, textvariable=self.ref, font=("arial", 11), width=27, state='readonly').grid(row=0, column=3)

        # Row 1
        Label(DataframeLeft, text="Dose Options", **lbl_opts).grid(row=1, column=0, sticky=W, pady=8)
        self.combo_dose = ttk.Combobox(DataframeLeft, textvariable=self.Dose, **cmb_opts, state="readonly")
        self.combo_dose['values'] = ("1 Tablet", "2 Tablets", "3 Tablets", "4 Tablets", "As Needed")
        self.combo_dose.grid(row=1, column=1, padx=10)

        Label(DataframeLeft, text="NHS Number", **lbl_opts).grid(row=1, column=2, sticky=W, padx=10)
        Entry(DataframeLeft, textvariable=self.nhsNumber, font=("arial", 11), width=27, state='readonly').grid(row=1, column=3)

        # Row 2
        Label(DataframeLeft, text="No. of Tablets", **lbl_opts).grid(row=2, column=0, sticky=W, pady=8)
        self.combo_qty = ttk.Combobox(DataframeLeft, textvariable=self.NumberofTablets, **cmb_opts)
        self.combo_qty['values'] = [str(i) for i in range(1, 31)]
        self.combo_qty.grid(row=2, column=1, padx=10)

        Label(DataframeLeft, text="Patient Name", **lbl_opts).grid(row=2, column=2, sticky=W, padx=10)
        Entry(DataframeLeft, textvariable=self.PatientName, font=("arial", 11), width=27).grid(row=2, column=3)

        # Row 3
        Label(DataframeLeft, text="Lot Number", **lbl_opts).grid(row=3, column=0, sticky=W, pady=8)
        self.combo_lot = ttk.Combobox(DataframeLeft, textvariable=self.Lot, **cmb_opts)
        self.combo_lot['values'] = ("LOT-101", "LOT-202", "LOT-303")
        self.combo_lot.grid(row=3, column=1, padx=10)

        Label(DataframeLeft, text="Date of Birth", **lbl_opts).grid(row=3, column=2, sticky=W, padx=10)
        DateEntry(DataframeLeft, textvariable=self.DateOfBirth, font=("arial", 11), width=25, date_pattern='dd/mm/yyyy').grid(row=3, column=3)

        # Row 4
        Label(DataframeLeft, text="Daily Dose", **lbl_opts).grid(row=4, column=0, sticky=W, pady=8)
        self.combo_daily = ttk.Combobox(DataframeLeft, textvariable=self.DailyDose, **cmb_opts)
        self.combo_daily['values'] = ("Once a day", "Twice a day", "Thrice a day")
        self.combo_daily.grid(row=4, column=1, padx=10)

        Label(DataframeLeft, text="Issue Date", **lbl_opts).grid(row=4, column=2, sticky=W, padx=10)
        DateEntry(DataframeLeft, textvariable=self.Issuedate, font=("arial", 11), width=25, date_pattern='dd/mm/yyyy').grid(row=4, column=3)

        # Row 5
        Label(DataframeLeft, text="Rack/Storage", **lbl_opts).grid(row=5, column=0, sticky=W, pady=8)
        Entry(DataframeLeft, textvariable=self.StorageAdvice, font=("arial", 11), width=27).grid(row=5, column=1)

        Label(DataframeLeft, text="Expiry Date", **lbl_opts).grid(row=5, column=2, sticky=W, padx=10)
        Entry(DataframeLeft, textvariable=self.ExpDate, font=("arial", 11), width=27).grid(row=5, column=3)

        # Row 6 (Full Span)
        Label(DataframeLeft, text="Address", **lbl_opts).grid(row=6, column=0, sticky=W, pady=8)
        Entry(DataframeLeft, textvariable=self.PatientAddress, font=("arial", 11), width=68).grid(row=6, column=1, columnspan=3, sticky=W, padx=10)

        # Text Area
        self.txtPrescription = Text(DataframeRight, font=("arial", 10), width=45, height=18, bg="#f1f2f6")
        self.txtPrescription.pack(fill=BOTH, expand=True, pady=5)

        # Buttons
        Buttonframe = Frame(Main_Frame, bg="#1e272e", pady=10)
        Buttonframe.pack(side=TOP, fill=X)
        btns = [("Bill", "#2980b9", self.generate_bill), ("Save", "#27ae60", self.save_data), ("Update", "#8e44ad", self.update_data), ("Print", "#f39c12", self.print_bill), ("Delete", "#c0392b", self.delete_data), ("Clear", "#7f8c8d", self.clear_data)]
        for t, c, m in btns:
            Button(Buttonframe, text=t, bg=c, fg="white", font=("arial", 10, "bold"), width=13, height=2, command=m).pack(side=LEFT, padx=4, expand=True, fill=X)

        # Table
        Tableframe = Frame(Main_Frame, bg="white", bd=2, relief=RIDGE)
        Tableframe.pack(side=TOP, fill=BOTH, expand=True)
        self.hospital_table = ttk.Treeview(Tableframe, columns=("med", "ref", "dose", "qty", "lot", "issue", "exp", "daily", "storage", "nhs", "pname", "dob", "address"))
        for col in self.hospital_table["columns"]: self.hospital_table.heading(col, text=col.upper()); self.hospital_table.column(col, width=100)
        self.hospital_table['show'] = 'headings'; self.hospital_table.pack(fill=BOTH, expand=1)
        self.hospital_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_med_names()
        self.auto_gen_numbers()
        self.fetch_data()

    def auto_gen_numbers(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            curr = conn.cursor()
            curr.execute("SELECT MAX(CAST(ref AS UNSIGNED)), MAX(CAST(nhs_number AS UNSIGNED)) FROM hospital")
            row = curr.fetchone()
            new_ref = (row[0] if row[0] else 1000) + 1
            new_nhs = (row[1] if row[1] else 5000) + 1
            self.ref.set(str(new_ref))
            self.nhsNumber.set(str(new_nhs))
            conn.close()
        except: self.ref.set("1001"); self.nhsNumber.set("5001")

    def fetch_med_names(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            curr = conn.cursor(); curr.execute("SELECT med_name FROM medicines")
            self.combo_med['values'] = [r[0] for r in curr.fetchall()]; conn.close()
        except: pass

    def get_med_details(self, event=""):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            curr = conn.cursor(); curr.execute("SELECT price_per_unit, rack_number, expiry_date FROM medicines WHERE med_name=%s", (self.Nameoftablets.get(),))
            row = curr.fetchone()
            if row: self.unit_price=float(row[0]); self.StorageAdvice.set(row[1]); self.ExpDate.set(row[2])
            conn.close()
        except: pass

    def save_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            curr = conn.cursor()
            curr.execute("INSERT INTO hospital VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (
                self.Nameoftablets.get(), self.ref.get(), self.Dose.get(), self.NumberofTablets.get(),
                self.Lot.get(), self.Issuedate.get(), self.ExpDate.get(), self.DailyDose.get(),
                self.StorageAdvice.get(), self.nhsNumber.get(), self.PatientName.get(),
                self.DateOfBirth.get(), self.PatientAddress.get()
            ))
            conn.commit(); conn.close(); self.fetch_data(); self.auto_gen_numbers(); messagebox.showinfo("Success", "Record Saved")
        except Exception as e: messagebox.showerror("Error", str(e))

    def fetch_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
        curr = conn.cursor(); curr.execute("SELECT * FROM hospital"); rows = curr.fetchall()
        self.hospital_table.delete(*self.hospital_table.get_children())
        for r in rows: self.hospital_table.insert("", END, values=r)
        conn.close()

    def get_cursor(self, event=""):
        row = self.hospital_table.item(self.hospital_table.focus())['values']
        if row:
            self.Nameoftablets.set(row[0]); self.ref.set(row[1]); self.Dose.set(row[2])
            self.NumberofTablets.set(row[3]); self.Lot.set(row[4]); self.Issuedate.set(row[5])
            self.ExpDate.set(row[6]); self.DailyDose.set(row[7]); self.StorageAdvice.set(row[8])
            self.nhsNumber.set(row[9]); self.PatientName.set(row[10]); self.DateOfBirth.set(row[11])
            self.PatientAddress.set(row[12])

    def update_data(self):
        conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
        curr = conn.cursor()
        curr.execute("UPDATE hospital SET name_of_tablets=%s, dose=%s, no_of_tablets=%s, lot=%s, issue_date=%s, exp_date=%s, daily_dose=%s, storage=%s, nhs_number=%s, patient_name=%s, dob=%s, address=%s WHERE ref=%s", (
            self.Nameoftablets.get(), self.Dose.get(), self.NumberofTablets.get(), self.Lot.get(), self.Issuedate.get(), self.ExpDate.get(), self.DailyDose.get(), self.StorageAdvice.get(), self.nhsNumber.get(), self.PatientName.get(), self.DateOfBirth.get(), self.PatientAddress.get(), self.ref.get()
        ))
        conn.commit(); conn.close(); self.fetch_data(); messagebox.showinfo("Success", "Updated")

    def delete_data(self):
        if messagebox.askyesno("Confirm", "Delete record?"):
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            curr = conn.cursor(); curr.execute("DELETE FROM hospital WHERE ref=%s", (self.ref.get(),))
            conn.commit(); conn.close(); self.fetch_data(); self.clear_data(); self.auto_gen_numbers()

    def generate_bill(self):
        qty = int(self.NumberofTablets.get() if self.NumberofTablets.get() else 0)
        total = qty * self.unit_price
        self.txtPrescription.delete("1.0", END)
        self.txtPrescription.insert(END, f"Patient: {self.PatientName.get()}\nMedicine: {self.Nameoftablets.get()}\nQty: {qty}\nTotal: Rs.{total}")

    def print_bill(self):
        content = self.txtPrescription.get("1.0", END)
        if len(content) > 5:
            f = tempfile.mktemp(".txt"); open(f, "w").write(content); os.startfile(f, "print")

    def clear_data(self):
        self.Nameoftablets.set(""); self.Dose.set(""); self.NumberofTablets.set(""); self.PatientName.set(""); self.PatientAddress.set(""); self.txtPrescription.delete("1.0", END); self.auto_gen_numbers()

if __name__ == "__main__":
    root = Tk(); Login(root); root.mainloop()