# gui/student_pages.py
import streamlit as st
from app.admin_utils import backup_data
from app.schedule import ScheduleManager

def show_student_management_page(manager):
    """Renders all components for the student management page."""
    st.header("Student Management")

    # --- Section 1: Search for a Student ---
    st.subheader("Find a Student")
    search_name = st.text_input("Enter student name to search")
    #return the student names, id, and instruments
    if st.button("Search"):
        results = [s for s in manager.students if search_name.lower() in s.name.lower()]
        if results:
            for student in results:
                st.write(f"ID: {student.id}, Name: {student.name}, Instrument: {student.instrument}")
        else:
            st.info("No students found with that name.")
    

    # --- Section 2: Register a New Student ---
    st.subheader("Register a New Student")
    with st.form("registration_form"):
        reg_name = st.text_input("New Student Name")
        reg_instrument = st.text_input("First Instrument")
        submitted = st.form_submit_button("Register Student")
        
        if submitted:
            # Call the manager's method to perform the registration.
            manager.register_new_student(reg_name, reg_instrument)
            st.success(f"Successfully registered {reg_name}!")

    # --- Section 3: Update Student Information ---
    st.subheader("Update Student Information")
    with st.form("update_form"):
        upd_id = st.number_input("Student ID", min_value=1, step=1)
        upd_name = st.text_input("Updated Name")
        upd_instrument = st.text_input("Updated Instrument")
        upd_submitted = st.form_submit_button("Update Student")
        
        if upd_submitted:
            # Call the manager's method to perform the update.
            manager.update_student(upd_id, upd_name, upd_instrument)
            st.success(f"Successfully updated student ID {upd_id}!")

    # --- Section 4: Unregister a Student ---
    st.subheader("Unregister a Student")
    with st.form("unregister_form"):
        unreg_id = st.number_input("Student ID to Unregister", min_value=1, step=1)
        unreg_submitted = st.form_submit_button("Unregister Student")
        
        if unreg_submitted:
            # Call the manager's method to perform the unregistration.
            manager.unregister_student(unreg_id)
            # manager.unregister_student(unreg_id)
            st.success(f"Successfully unregistered student ID {unreg_id}!")

    #backup button
    st.subheader("Backup Data")
    if st.button("Backup Data Now"):
        backup_data(manager)
        st.success("Backup completed successfully.")
