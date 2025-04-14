import streamlit as st
from  agents import agent  # Import the agent from the agents.py file

st.title("🤖 MatchGrid Result Analysis")

user_query = st.text_input("Enter your query here:", placeholder="e.g., Get the latest job id")

if st.button("Search") and user_query:
    with st.spinner("Thinking..."):
        try:
            response = agent.run(user_query)
            st.success("Response:")
            st.code(response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
