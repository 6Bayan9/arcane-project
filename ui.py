import tkinter as tk
from tkinter import messagebox
import database

def submit_data():
    name = name_entry.get()
    status = status_entry.get()

    if name == "" or status == "":
        messagebox.showerror("خطأ", "الرجاء تعبئة جميع الحقول")
        return

    database.insert_user(name, status)
    messagebox.showinfo("تم", "تم حفظ البيانات بنجاح")

    name_entry.delete(0, tk.END)
    status_entry.delete(0, tk.END)

def create_ui():
    window = tk.Tk()
    window.title("Arcane Project")
    window.geometry("300x250")

    tk.Label(window, text="الاسم").pack()
    global name_entry
    name_entry = tk.Entry(window)
    name_entry.pack()

    tk.Label(window, text="الحالة").pack()
    global status_entry
    status_entry = tk.Entry(window)
    status_entry.pack()

    tk.Button(window, text="حفظ", command=submit_data).pack(pady=10)

    window.mainloop()
