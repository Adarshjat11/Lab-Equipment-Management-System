import pandas as pd
import os
from datetime import datetime

EXCEL_FILE = "equipment.xlsx"

def initialize_excel():
    if not os.path.exists(EXCEL_FILE):
        equipment = pd.DataFrame(columns=[
            "equipment_name",
            "description",
            "total_quantity",
            "available_quantity",
            "image_url"
        ])

        issued = pd.DataFrame(columns=[
            "student_name",
            "student_email",
            "semester",
            "equipment_name",
            "quantity",
            "issued_time",
            "status"
        ])

        students = pd.DataFrame(columns=[
            "student_name",
            "student_email",
            "semester"
        ])

        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl") as writer:
            equipment.to_excel(writer, sheet_name="equipment", index=False)
            issued.to_excel(writer, sheet_name="issued_items", index=False)
            students.to_excel(writer, sheet_name="students", index=False)


def load_data():
    initialize_excel()
    equipment = pd.read_excel(EXCEL_FILE, sheet_name="equipment")
    issued = pd.read_excel(EXCEL_FILE, sheet_name="issued_items")
    students = pd.read_excel(EXCEL_FILE, sheet_name="students")
    return equipment, issued, students


def save_data(equipment, issued, students):
    with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="w") as writer:
        equipment.to_excel(writer, sheet_name="equipment", index=False)
        issued.to_excel(writer, sheet_name="issued_items", index=False)
        students.to_excel(writer, sheet_name="students", index=False)

def add_student(students, name, email, semester):
    if email in students["student_email"].values:
        return students, False

    new = {
        "student_name": name,
        "student_email": email,
        "semester": semester
    }
    students = pd.concat(
        [students, pd.DataFrame([new])],
        ignore_index=True
    )
    return students, True

def remove_student(students, email):
    if email not in students["student_email"].values:
        return students, False

    students = students[students["student_email"] != email]
    return students, True

def add_equipment(equipment, name, desc, qty, img):
    if name in equipment["equipment_name"].values:
        idx = equipment[equipment["equipment_name"] == name].index[0]

        equipment.loc[idx, "total_quantity"] += qty
        equipment.loc[idx, "available_quantity"] += qty

        if desc:
            equipment.loc[idx, "description"] = desc
        if img:
            equipment.loc[idx, "image_url"] = img
    else:
        new = {
            "equipment_name": name,
            "description": desc,
            "total_quantity": qty,
            "available_quantity": qty,
            "image_url": img
        }
        equipment = pd.concat(
            [equipment, pd.DataFrame([new])],
            ignore_index=True
        )

    return equipment



def issue_equipment(equipment, issued, student, email, semester, item, qty):
    equipment.loc[equipment["equipment_name"] == item, "available_quantity"] -= qty
    issued = pd.concat([issued, pd.DataFrame([{
        "student_name": student,
        "student_email": email,
        "semester": semester,
        "equipment_name": item,
        "quantity": qty,
        "issued_time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "status": "issued"
    }])], ignore_index=True)
    return equipment, issued

def return_equipment(equipment, issued, index):
    row = issued.loc[index]
    equipment.loc[
        equipment["equipment_name"] == row["equipment_name"],
        "available_quantity"
    ] += row["quantity"]
    issued.loc[index, "status"] = "returned"
    return equipment, issued
