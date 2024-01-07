import streamlit as st
import time

# Create placeholders for the spinner and the expander


# Create a button to start the process
if st.button('Start Process'):
    spinner_placeholder = st.empty()
    expander_placeholder = st.empty()
    # Use the spinner_placeholder to create a container with a border and a spinner
    with spinner_placeholder.container(border=True):
        with st.spinner('Thinking...'):
            time.sleep(5)  # Simulate a time-consuming process

    # Clear the spinner placeholder after the process is complete
    spinner_placeholder.empty()

    # Use the expander_placeholder to show the process completion
    with expander_placeholder.expander("✔️ Complete ", expanded=False):
        st.write("Process finished successfully!")
