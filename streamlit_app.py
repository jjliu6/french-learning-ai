import streamlit as st
from datetime import datetime

# Initialize session state for storing content
if 'content_database' not in st.session_state:
    st.session_state.content_database = []

st.title("French Learning AI")
st.markdown("Your personalized French learning companion")

# Sidebar for navigation
page = st.sidebar.selectbox(
    "Choose a feature",
    ["Add Content", "My Knowledge Base", "Learn"]
)

if page == "Add Content":
    st.header("Add New Content")
    
    content = st.text_area("Enter text in any language:", height=150)
    source_language = st.selectbox("Content Language", ["English", "Chinese", "French", "Other"])
    tags = st.text_input("Add tags (comma-separated):")
    
    if st.button("Save Content"):
        if content:
            new_entry = {
                "id": len(st.session_state.content_database),
                "content": content,
                "language": source_language,
                "tags": [tag.strip() for tag in tags.split(",") if tag],
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
        with st.expander(f"{item['content'][:50]}... ({item['language']})"):
            st.write(f"**Full Content:** {item['content']}")
            st.write(f"**Language:** {item['language']}")
            st.write(f"**Tags:** {', '.join(item['tags'])}")
            st.write(f"**Added:** {item['date_added']}")

else:  # Learn
    st.header("Learning Zone")
    
    difficulty = st.slider("Difficulty Level", 1, 5, 2)
    
    if st.session_state.content_database:
        st.subheader("Practice Exercise")
        st.info("Here's a phrase from your content:")
        
        # Just showing the first saved content as an example
        example = st.session_state.content_database[0]['content']
        st.write(example)
        
        if st.button("Show Translation"):
            st.success("Translation will be added soon!")
            
        # Feedback buttons
        col1, col2, col3 = st.columns(3)
        with col1:
            st.button("😊 Got it!")
        with col2:
            st.button("😐 Almost")
        with col3:
            st.button("😕 Need Practice")
    else:
        st.warning("Add some content in 'Add Content' to start learning!")
