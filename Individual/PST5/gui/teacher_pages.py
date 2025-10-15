import streamlit as st
from app.admin_utils import backup_data

def show_teacher_management_page(manager):
    st.title("Teacher Management")

    #register teacher
    st.subheader("Register a New Teacher")
    with st.form("teacher_registration_form"):
        teacher_name = st.text_input("Teacher Name")
        teacher_instrument = st.text_input("Primary Instrument")
        submitted = st.form_submit_button("Register Teacher")
        
        if submitted:
            # Call the manager's method to perform the registration.
            # manager.register_new_teacher(teacher_name, teacher_instrument)
            st.success(f"Successfully registered {teacher_name}!")
    
    #update teacher
    st.subheader("Update Teacher Information")
    with st.form("teacher_update_form"):
        upd_id = st.number_input("Teacher ID", min_value=1, step=1)
        upd_name = st.text_input("Updated Name")
        upd_instrument = st.text_input("Updated Instrument")
        upd_submitted = st.form_submit_button("Update Teacher")
        
        if upd_submitted:
            # Call the manager's method to perform the update.
            # manager.update_teacher_info(upd_id, upd_name, upd_instrument)
            st.success(f"Successfully updated teacher ID {upd_id}!")

    #unregister teacher
    st.subheader("Unregister a Teacher")
    with st.form("teacher_unregister_form"):
        unreg_id = st.number_input("Teacher ID to Unregister", min_value=1, step=1)
        unreg_submitted = st.form_submit_button("Unregister Teacher")
        
        if unreg_submitted:
            # Call the manager's method to perform the unregistration.
            # manager.unregister_teacher(unreg_id)
            st.success(f"Successfully unregistered teacher ID {unreg_id}!")


    # Backup button
    st.subheader("Backup Data")
    if st.button("Backup Data"):
        backup_data(manager)
        st.success("Data backed up successfully!")