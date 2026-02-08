import streamlit as st
from config import get_admins
from data_manager import (
    load_data,
    save_data,
    issue_equipment,
    return_equipment,
    add_equipment,
    add_student,
    remove_student
)
from mailer import send_issue_email
from analytics import equipment_usage_stats, issued_metrics

st.set_page_config(page_title="Lab Equipment Scheduler", layout="wide")
st.title("🔬 Lab Equipment Scheduler")

equipment, issued, students = load_data()
admins = get_admins()

mode = st.sidebar.selectbox("Mode", ["Student", "Admin"])

# ======================= STUDENT =========================
if mode == "Student":
    st.header("📘 Student Portal")

    if "verified" not in st.session_state:
        st.session_state.verified = False
        st.session_state.student = None

    # -------- STUDENT VERIFICATION --------
    with st.expander("🧑‍🎓 Student Verification", expanded=True):
        roll_no = st.text_input("Roll / Enrollment Number")

        if st.button("Verify Student"):
            match = students[students["roll_no"] == roll_no]

            if match.empty:
                st.error("❌ Unauthorized student. Contact admin.")
                st.session_state.verified = False
            else:
                st.session_state.verified = True
                st.session_state.student = match.iloc[0]
                st.success("✅ Student verified")

    if not st.session_state.verified:
        st.stop()

    student = st.session_state.student
    st.info(
        f"👤 {student['student_name']} | "
        f"{student['student_email']} | "
        f"Semester {student['semester']}"
    )

    # -------- ISSUE EQUIPMENT --------
    st.divider()
    st.subheader("📦 Issue Equipment")

    if equipment.empty:
        st.warning("No equipment available")
        st.stop()

    item = st.selectbox(
        "Select Equipment",
        equipment["equipment_name"].unique()
    )

    row = equipment[equipment["equipment_name"] == item].iloc[0]

    if str(row.get("image_url", "")).strip():
        st.image(row["image_url"], width=250)

    st.subheader("📄 Description")
    st.write(row.get("description", "No description provided."))

    st.info(f"Available Quantity: {int(row['available_quantity'])}")

    qty = st.number_input(
        "Quantity",
        min_value=1,
        max_value=int(row["available_quantity"]),
        step=1
    )

    if st.button("📦 Issue Equipment"):
        equipment, issued = issue_equipment(
            equipment,
            issued,
            student["roll_no"],
            student["student_name"],
            student["student_email"],
            student["semester"],
            item,
            qty
        )
        save_data(equipment, issued, students)

        try:
            send_issue_email(
                student["student_name"],
                student["student_email"],
                student["semester"],
                item,
                qty
            )
        except Exception:
            st.warning("Email service not configured")

        st.success("✅ Equipment issued successfully")

# ======================== ADMIN ==========================
if mode == "Admin":
    st.header("🛠️ Admin Login")

    admin_email = st.text_input("Admin Email")
    admin_password = st.text_input("Password", type="password")

    if admin_email not in admins or admins[admin_email] != admin_password:
        st.warning("Invalid admin credentials")
        st.stop()

    st.success(f"Welcome {admin_email}")

    # -------- DASHBOARD --------
    with st.expander("📊 Dashboard", expanded=True):
        metrics = issued_metrics(issued)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Issued", metrics["total_issued"])
        c2.metric("Active", metrics["active"])
        c3.metric("Returned", metrics["returned"])

        st.bar_chart(equipment_usage_stats(issued))

    # -------- INVENTORY --------
    with st.expander("📦 Equipment Inventory"):
        st.dataframe(
            equipment[
                ["equipment_name", "total_quantity", "available_quantity"]
            ],
            use_container_width=True
        )

    # -------- ADD / UPDATE EQUIPMENT --------
    with st.expander("➕ Add / Update Equipment"):
        with st.form("equipment_form"):
            name = st.text_input("Equipment Name")
            desc = st.text_area("Description")
            qty = st.number_input("Quantity to Add", min_value=1, step=1)
            img = st.text_input("Image URL (optional)")

            if st.form_submit_button("Save"):
                equipment = add_equipment(
                    equipment,
                    name,
                    desc,
                    qty,
                    img
                )
                save_data(equipment, issued, students)
                st.success("Equipment saved")
                st.rerun()

    # -------- STUDENT MANAGEMENT --------
    with st.expander("🎓 Student Management"):
        with st.form("add_student"):
            roll = st.text_input("Roll / Enrollment No")
            name = st.text_input("Student Name")
            email = st.text_input("Student Email")
            sem = st.selectbox("Semester", ["1","2","3","4","5","6","7","8","9","10"])

            if st.form_submit_button("Add Student"):
                students = add_student(
                    students,
                    roll,
                    name,
                    email,
                    sem
                )
                save_data(equipment, issued, students)
                st.success("Student added")
                st.rerun()

        st.divider()

        roll_remove = st.selectbox(
            "Remove Student",
            students["roll_no"]
        )
        if st.button("Remove Student"):
            students = remove_student(students, roll_remove)
            save_data(equipment, issued, students)
            st.success("Student removed")
            st.rerun()

    # -------- ISSUED EQUIPMENT --------
    with st.expander("📦 Issued Equipment"):
        active = issued[issued["status"] == "issued"]
        st.dataframe(active, use_container_width=True)

        if not active.empty:
            idx = st.selectbox("Select issue", active.index)
            if st.button("Mark Returned"):
                equipment, issued = return_equipment(
                    equipment, issued, idx
                )
                save_data(equipment, issued, students)
                st.success("Returned")

    # -------- STUDENTS BY SEMESTER --------
    with st.expander("🎓 Students by Semester"):
        sem = st.selectbox(
            "Semester",
            sorted(students["semester"].astype(str).unique())
        )
        st.dataframe(
            students[students["semester"].astype(str) == sem],
            use_container_width=True
        )
