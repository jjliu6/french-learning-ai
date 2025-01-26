import streamlit as st
from datetime import datetime
import openai
import random

# Initialize session state for storing content and OpenAI key
if 'content_database' not in st.session_state:
    st.session_state.content_database = []
if 'openai_key' not in st.session_state:
    st.session_state.openai_key = None

st.title("French Learning AI")
st.markdown("Your personalized French learning companion")

# Sidebar for navigation and API key
page = st.sidebar.selectbox(
    "Choose a feature",
    ["Add Content", "My Knowledge Base", "Learn"]
)

# OpenAI API key input in sidebar
api_key = st.sidebar.text_input("Enter OpenAI API Key:", type="password")
if api_key:
    st.session_state.openai_key = api_key
    openai.api_key = api_key

def generate_vocab_and_questions(text, difficulty):
    """Generate vocabulary and questions using OpenAI API"""
    if not st.session_state.openai_key:
        return None, None
    
    try:
        # Prompt for vocabulary
        vocab_prompt = f"""
        From this text: "{text}"
        Extract 5 key French words or phrases (if difficulty is {difficulty}/5, adjust complexity accordingly).
        For each word/phrase provide:
        1. The word/phrase in French
        2. Its English translation
        3. A simple example sentence in French
        Format as a list of dictionaries with keys: word, translation, example
        """
        
        vocab_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": vocab_prompt}]
        )
        vocab_list = eval(vocab_response.choices[0].message.content)
        
        # Prompt for comprehension questions
        questions_prompt = f"""
        From this text: "{text}"
        Create 3 comprehension questions in French (adjust for difficulty level {difficulty}/5).
        For each question provide:
        1. The question in French
        2. The correct answer in French
        Format as a list of dictionaries with keys: question, answer
        """
        
        questions_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": questions_prompt}]
        )
        questions_list = eval(questions_response.choices[0].message.content)
        
        return vocab_list, questions_list
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None, None

# Your existing Add Content and Knowledge Base code here...
[previous code for these sections remains the same]

else:  # Learn
    st.header("Learning Zone")
    
    if not st.session_state.openai_key:
        st.warning("Please enter your OpenAI API key in the sidebar to enable AI features")
    
    if st.session_state.content_database:
        # Select content to learn from
        content_titles = [f"{item['content'][:50]}... ({item['language']})" 
                         for item in st.session_state.content_database]
        selected_content_index = st.selectbox(
            "Choose content to learn from:",
            range(len(content_titles)),
            format_func=lambda x: content_titles[x]
        )
        
        selected_content = st.session_state.content_database[selected_content_index]
        
        # Display selected content
        with st.expander("View Full Content"):
            st.write(selected_content['content'])
        
        # Difficulty setting
        difficulty = st.slider("Difficulty Level", 1, 5, 2)
        
        if st.button("Generate Learning Materials"):
            if st.session_state.openai_key:
                with st.spinner("Generating vocabulary and questions..."):
                    vocab_list, questions_list = generate_vocab_and_questions(
                        selected_content['content'], 
                        difficulty
                    )
                    
                    if vocab_list and questions_list:
                        # Vocabulary Section
                        st.subheader("📚 Key Vocabulary")
                        for i, vocab in enumerate(vocab_list, 1):
                            with st.expander(f"{i}. {vocab['word']}"):
                                st.write(f"**Translation:** {vocab['translation']}")
                                st.write(f"**Example:** {vocab['example']}")
                                
                                # Simple quiz
                                if st.button(f"Test yourself on '{vocab['word']}'", key=f"vocab_{i}"):
                                    st.write("Complete this sentence:")
                                    st.write(vocab['example'].replace(vocab['word'], "____"))
                                    user_answer = st.text_input("Your answer:", key=f"vocab_answer_{i}")
                                    check = st.button("Check", key=f"check_{i}")
                                    if check and user_answer:
                                        if user_answer.lower() == vocab['word'].lower():
                                            st.success("Correct! 🎉")
                                        else:
                                            st.error(f"Not quite. The word was: {vocab['word']}")
                        
                        # Comprehension Questions
                        st.subheader("📝 Comprehension Questions")
                        for i, question in enumerate(questions_list, 1):
                            with st.expander(f"Question {i}"):
                                st.write(f"**{question['question']}**")
                                user_answer = st.text_input("Your answer (in French):", key=f"q_{i}")
                                if st.button("Check Answer", key=f"check_q_{i}"):
                                    # Simple string matching for now
                                    if user_answer.lower() == question['answer'].lower():
                                        st.success("Correct! 🎉")
                                    else:
                                        st.warning(f"Here's the answer: {question['answer']}")
                                        st.info("Compare your answer with the correct one. Were you close?")
            else:
                st.warning("Please enter your OpenAI API key in the sidebar")
    else:
        st.warning("Add some content in 'Add Content' to start learning!")
