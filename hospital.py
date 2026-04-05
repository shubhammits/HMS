from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import os
import tempfile

class Hospital:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Hospital Management System")

        
        
        # --- WINDOW APP STYLE (Auto-Maximize) ---
        self.root.state('zoomed') 
        self.root.configure(bg="#1e272e")

        # ================= Theme Colors =================
        self.bg_color = "#1e272e"
        self.panel_bg = "#2f3542"
        self.accent_color = "#2ed573"
        self.entry_bg = "#f1f2f6"

        # ================= Variables =================
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
        
        # Search Variables
        self.search_by = StringVar()
        self.search_txt = StringVar()

        # ================= Title =================
        lbltitle = Label(self.root, bd=0, text="HOSPITAL MANAGEMENT SYSTEM",
                         fg=self.accent_color, bg="#2f3542", font=("arial", 35, "bold"), pady=10)
        lbltitle.pack(side=TOP, fill=X)

        # Main Container
        self.Main_Frame = Frame(self.root, bg=self.bg_color)
        self.Main_Frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # ================= Data Entry Frame =================
        Dataframe = Frame(self.Main_Frame, bg=self.bg_color)
        Dataframe.pack(side=TOP, fill=X)

        DataframeLeft = LabelFrame(Dataframe, bd=2, relief=RIDGE, padx=10, bg=self.panel_bg,
                                   fg=self.accent_color, font=("arial", 12, "bold"), text="Patient Information")
        DataframeLeft.pack(side=LEFT, fill=BOTH, expand=True, padx=5)

        DataframeRight = LabelFrame(Dataframe, bd=2, relief=RIDGE, padx=10, bg=self.panel_bg,
                                    fg=self.accent_color, font=("arial", 12, "bold"), text="Prescription / Bill")
        DataframeRight.pack(side=RIGHT, fill=Y, padx=5)

        # Responsive Grid config for Left Frame
        DataframeLeft.columnconfigure(1, weight=1)
        DataframeLeft.columnconfigure(3, weight=1)

        lbl_opts = {"bg": self.panel_bg, "fg": "white", "font": ("arial", 11, "bold")}
        ent_opts = {"font": ("arial", 11), "bg": self.entry_bg}

        # Row 0
        Label(DataframeLeft, text="Name of Tablets", **lbl_opts).grid(row=0, column=0, sticky=W, pady=5)
        Entry(DataframeLeft, textvariable=self.Nameoftablets, **ent_opts).grid(row=0, column=1, sticky="ew", padx=5)
        Label(DataframeLeft, text="NHS Number", **lbl_opts).grid(row=0, column=2, sticky=W, padx=5)
        Entry(DataframeLeft, textvariable=self.nhsNumber, **ent_opts).grid(row=0, column=3, sticky="ew", padx=5)

        # Row 1
        Label(DataframeLeft, text="Reference No", **lbl_opts).grid(row=1, column=0, sticky=W, pady=5)
        Entry(DataframeLeft, textvariable=self.ref, **ent_opts).grid(row=1, column=1, sticky="ew", padx=5)
        Label(DataframeLeft, text="Patient Name", **lbl_opts).grid(row=1, column=2, sticky=W, padx=5)
        Entry(DataframeLeft, textvariable=self.PatientName, **ent_opts).grid(row=1, column=3, sticky="ew", padx=5)

        # Row 2
        Label(DataframeLeft, text="Dose", **lbl_opts).grid(row=2, column=0, sticky=W, pady=5)
        Entry(DataframeLeft, textvariable=self.Dose, **ent_opts).grid(row=2, column=1, sticky="ew", padx=5)
        Label(DataframeLeft, text="DOB", **lbl_opts).grid(row=2, column=2, sticky=W, padx=5)
        Entry(DataframeLeft, textvariable=self.DateOfBirth, **ent_opts).grid(row=2, column=3, sticky="ew", padx=5)

        # Row 3
        Label(DataframeLeft, text="No of Tablets", **lbl_opts).grid(row=3, column=0, sticky=W, pady=5)
        Entry(DataframeLeft, textvariable=self.NumberofTablets, **ent_opts).grid(row=3, column=1, sticky="ew", padx=5)
        Label(DataframeLeft, text="Address", **lbl_opts).grid(row=3, column=2, sticky=W, padx=5)
        Entry(DataframeLeft, textvariable=self.PatientAddress, **ent_opts).grid(row=3, column=3, sticky="ew", padx=5)

        # Row 4
        Label(DataframeLeft, text="Lot", **lbl_opts).grid(row=4, column=0, sticky=W, pady=5)
        Entry(DataframeLeft, textvariable=self.Lot, **ent_opts).grid(row=4, column=1, sticky="ew", padx=5)
        Label(DataframeLeft, text="Issue Date", **lbl_opts).grid(row=4, column=2, sticky=W, padx=5)
        Entry(DataframeLeft, textvariable=self.Issuedate, **ent_opts).grid(row=4, column=3, sticky="ew", padx=5)

        # Row 5
        Label(DataframeLeft, text="Expiry Date", **lbl_opts).grid(row=5, column=0, sticky=W, pady=5)
        Entry(DataframeLeft, textvariable=self.ExpDate, **ent_opts).grid(row=5, column=1, sticky="ew", padx=5)
        Label(DataframeLeft, text="Daily Dose", **lbl_opts).grid(row=5, column=2, sticky=W, padx=5)
        Entry(DataframeLeft, textvariable=self.DailyDose, **ent_opts).grid(row=5, column=3, sticky="ew", padx=5)

        # Row 6
        Label(DataframeLeft, text="Storage Advice", **lbl_opts).grid(row=6, column=0, sticky=W, pady=5)
        Entry(DataframeLeft, textvariable=self.StorageAdvice, **ent_opts).grid(row=6, column=1, sticky="ew", padx=5)

        # Prescription Text Area
        self.txtPrescription = Text(DataframeRight, font=("arial", 11), width=45, height=16, bg="#f1f2f6")
        self.txtPrescription.pack(fill=BOTH, expand=True, pady=5)

        # ================= Buttons Frame =================
        Buttonframe = Frame(self.Main_Frame, bg=self.bg_color, pady=10)
        Buttonframe.pack(side=TOP, fill=X)

        btn_list = [
            ("Prescription", "#16a085", self.generate_prescription),
            ("Bill", "#2980b9", self.generate_bill),
            ("Save", "#27ae60", self.save_data),
            ("Update", "#8e44ad", self.update_data),
            ("Delete", "#c0392b", self.delete_data),
            ("Clear", "#7f8c8d", self.clear_data),
            ("Exit", "#d63031", self.root.destroy)
        ]

        for text, color, cmd in btn_list:
            Button(Buttonframe, text=text, bg=color, fg="white", font=("arial", 10, "bold"), 
                   width=14, height=2, cursor="hand2", command=cmd).pack(side=LEFT, padx=5, expand=True, fill=X)

        # ================= Search Frame =================
        Searchframe = Frame(self.Main_Frame, bg=self.bg_color, pady=5)
        Searchframe.pack(side=TOP, fill=X)

        Label(Searchframe, text="Search By:", bg=self.bg_color, fg="yellow", font=("arial", 11, "bold")).pack(side=LEFT, padx=5)
        self.combo_search = ttk.Combobox(Searchframe, textvariable=self.search_by, width=12, font=("arial", 11), state="readonly")
        self.combo_search['values'] = ("Ref", "Name")
        self.combo_search.pack(side=LEFT, padx=5)
        self.combo_search.set("Ref")

        Entry(Searchframe, textvariable=self.search_txt, width=25, font=("arial", 11)).pack(side=LEFT, padx=5)
        Button(Searchframe, text="Search", bg="#f39c12", fg="white", width=12, font=("arial", 9, "bold"), command=self.search_data).pack(side=LEFT, padx=5)
        Button(Searchframe, text="Show All", bg="#3498db", fg="white", width=12, font=("arial", 9, "bold"), command=self.fetch_data).pack(side=LEFT, padx=5)

        # ================= Table Frame =================
        Detailsframe = Frame(self.Main_Frame, bg="white")
        Detailsframe.pack(side=TOP, fill=BOTH, expand=True)

        scroll_x = ttk.Scrollbar(Detailsframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(Detailsframe, orient=VERTICAL)

        self.hospital_table = ttk.Treeview(Detailsframe, column=(
            "name_of_tablets", "ref", "dose", "no_of_tablets", "lot",
            "issue_date", "exp_date", "daily_dose", "storage",
            "nhs_number", "patient_name", "dob", "address"
        ), xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.hospital_table.xview)
        scroll_y.config(command=self.hospital_table.yview)

        for col in self.hospital_table["columns"]:
            self.hospital_table.heading(col, text=col.replace("_", " ").upper())
            self.hospital_table.column(col, width=120)

        self.hospital_table["show"] = "headings"
        self.hospital_table.pack(fill=BOTH, expand=1)
        self.hospital_table.bind("<ButtonRelease-1>", self.get_cursor)

        self.fetch_data()

    # ================= ALL FUNCTIONS (COMPLETE) =================

    def generate_prescription(self):
        self.txtPrescription.delete("1.0", END)
        prescription = f"""
Patient Name: {self.PatientName.get()}
DOB: {self.DateOfBirth.get()}
Address: {self.PatientAddress.get()}
NHS Number: {self.nhsNumber.get()}

Medicine Name: {self.Nameoftablets.get()}
Reference No: {self.ref.get()}
Dose: {self.Dose.get()}
No of Tablets: {self.NumberofTablets.get()}
Lot: {self.Lot.get()}
Issue Date: {self.Issuedate.get()}
Expiry Date: {self.ExpDate.get()}
Daily Dose: {self.DailyDose.get()}
Storage Advice: {self.StorageAdvice.get()}
------------------------------------------
Take medicines as prescribed by doctor.
        """
        self.txtPrescription.insert(END, prescription)

    def generate_bill(self):
        try:
            qty = int(self.NumberofTablets.get())
            rate = 10
            total = qty * rate
        except:
            total = 0
        bill_text = f"""
Patient Bill
------------------------
Patient Name: {self.PatientName.get()}
Medicine: {self.Nameoftablets.get()}
No of Tablets: {self.NumberofTablets.get()}
Rate per tablet: 10
Total Amount: {total}
------------------------
Thank you for visiting!
        """
        messagebox.showinfo("Bill", bill_text)

    def save_data(self):
        if self.Nameoftablets.get()=="" or self.ref.get()=="":
            messagebox.showerror("Error", "All fields are required")
            return
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO hospital (name_of_tablets, ref, dose, no_of_tablets, lot, issue_date, exp_date, daily_dose, storage, nhs_number, patient_name, dob, address) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                           (self.Nameoftablets.get(), self.ref.get(), self.Dose.get(), self.NumberofTablets.get(), self.Lot.get(),
                            self.Issuedate.get(), self.ExpDate.get(), self.DailyDose.get(), self.StorageAdvice.get(),
                            self.nhsNumber.get(), self.PatientName.get(), self.DateOfBirth.get(), self.PatientAddress.get()))
            conn.commit()
            conn.close()
            self.fetch_data()
            messagebox.showinfo("Success", "Record inserted successfully")
        except Exception as e:
            messagebox.showerror("DB Error", f"Error: {str(e)}")

    def fetch_data(self):
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM hospital")
            rows = cursor.fetchall()
            if len(rows) != 0:
                self.hospital_table.delete(*self.hospital_table.get_children())
                for row in rows:
                    self.hospital_table.insert("", END, values=row)
            conn.close()
        except:
            pass

    def search_data(self):
        if self.search_txt.get() == "":
            messagebox.showerror("Error", "Enter search text")
            return
        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            cursor = conn.cursor()
            col = "patient_name" if self.search_by.get() == "Name" else "ref"
            cursor.execute(f"SELECT * FROM hospital WHERE {col} LIKE '%{self.search_txt.get()}%'")
            rows = cursor.fetchall()
            self.hospital_table.delete(*self.hospital_table.get_children())
            for row in rows:
                self.hospital_table.insert("", END, values=row)
            conn.close()
        except:
            messagebox.showerror("Error", "Search failed")

    def get_cursor(self, event=""):
        cursor_row = self.hospital_table.focus()
        content = self.hospital_table.item(cursor_row)
        row = content["values"]
        if row:
            self.Nameoftablets.set(row[0]); self.ref.set(row[1]); self.Dose.set(row[2])
            self.NumberofTablets.set(row[3]); self.Lot.set(row[4]); self.Issuedate.set(row[5])
            self.ExpDate.set(row[6]); self.DailyDose.set(row[7]); self.StorageAdvice.set(row[8])
            self.nhsNumber.set(row[9]); self.PatientName.set(row[10]); self.DateOfBirth.set(row[11])
            self.PatientAddress.set(row[12])

    def update_data(self):
        if self.ref.get() == "":
            messagebox.showerror("Error", "Select a record to update")
            return
        conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
        cursor = conn.cursor()
        cursor.execute("UPDATE hospital SET name_of_tablets=%s, dose=%s, no_of_tablets=%s, lot=%s, issue_date=%s, exp_date=%s, daily_dose=%s, storage=%s, nhs_number=%s, patient_name=%s, dob=%s, address=%s WHERE ref=%s",
                       (self.Nameoftablets.get(), self.Dose.get(), self.NumberofTablets.get(), self.Lot.get(),
                        self.Issuedate.get(), self.ExpDate.get(), self.DailyDose.get(), self.StorageAdvice.get(),
                        self.nhsNumber.get(), self.PatientName.get(), self.DateOfBirth.get(), self.PatientAddress.get(),
                        self.ref.get()))
        conn.commit()
        conn.close()
        self.fetch_data()
        messagebox.showinfo("Success", "Record updated successfully")

    def delete_data(self):
        if self.ref.get() == "":
            messagebox.showerror("Error", "Select record to delete")
            return
        m = messagebox.askyesno("Confirm", "Do you want to delete this record?")
        if m > 0:
            conn = mysql.connector.connect(host="localhost", user="root", password="12345", database="hospital_db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM hospital WHERE ref=%s", (self.ref.get(),))
            conn.commit()
            conn.close()
            self.fetch_data()
            self.clear_data()

    def clear_data(self):
        self.Nameoftablets.set(""); self.ref.set(""); self.Dose.set(""); self.NumberofTablets.set("")
        self.Lot.set(""); self.Issuedate.set(""); self.ExpDate.set(""); self.DailyDose.set("")
        self.StorageAdvice.set(""); self.nhsNumber.set(""); self.PatientName.set("")
        self.DateOfBirth.set(""); self.PatientAddress.set(""); self.txtPrescription.delete("1.0", END)

if __name__ == "__main__":
    root = Tk()
    app = Hospital(root)
    root.mainloop()