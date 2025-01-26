import streamlit as st
import openai
from datetime import datetime

# Initialize session state
if 'content_database' not in st.session_state:
    st.session_state.content_database = []

st.title("French Learning AI")

# Simple navigation
page = st.sidebar.selectbox("Choose a feature", ["Add Content", "My Knowledge Base", "Learn"])

if page == "Add Content":
    st.header("Add New Content")
    content = st.text_area("Enter text in any language:", height=150)
    source_language = st.selectbox("Content Language", ["English", "Chinese", "French", "Other"])
    
    if st.button("Save Content"):
        if content:
            new_entry = {
                "content": content,
                "language": source_language,
                "date_added": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.content_database.append(new_entry)
            st.success("Content saved successfully!")
        else:
            st.error("Please enter some content")

elif page == "My Knowledge Base":
    st.header("My Saved Content")
    
    if not st.session_state.content_database:
        st.info("No content saved yet. Add some content to get started!")
    
    for item in st.session_state.content_database:
        with st.expander(f"Content in {item['language']}"):
            st.write(f"**Content:** {item['content']}")
            st.write(f"**Added:** {item['date_added']}")

else:  # Learn
    st.header("Learning Zone")
    st.info("AI features coming soon!")
