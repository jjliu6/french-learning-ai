def generate_vocab_and_questions(text, difficulty):
    """Generate vocabulary and questions using OpenAI API"""
    if not st.session_state.openai_key:
        return None, None
    
    try:
        client = openai.OpenAI(api_key=st.session_state.openai_key)
        
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
        
        vocab_response = client.chat.completions.create(
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
        
        questions_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": questions_prompt}]
        )
        questions_list = eval(questions_response.choices[0].message.content)
        
        return vocab_list, questions_list
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None, None
