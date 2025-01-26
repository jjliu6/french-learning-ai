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
        Return the response in this exact format:
        [
            {{"word": "french_word1", "translation": "english1", "example": "french_example1"}},
            {{"word": "french_word2", "translation": "english2", "example": "french_example2"}},
            ...
        ]
        """
        
        vocab_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": vocab_prompt}],
            temperature=0.7
        )
        
        try:
            vocab_list = eval(vocab_response.choices[0].message.content.strip())
        except:
            st.error("Error parsing vocabulary response")
            vocab_list = [
                {"word": "example", "translation": "exemple", "example": "C'est un exemple."}
            ]
        
        # Prompt for comprehension questions
        questions_prompt = f"""
        From this text: "{text}"
        Create 3 comprehension questions in French (adjust for difficulty level {difficulty}/5).
        For each question provide:
        1. The question in French
        2. The correct answer in French
        Return the response in this exact format:
        [
            {{"question": "french_question1", "answer": "french_answer1"}},
            {{"question": "french_question2", "answer": "french_answer2"}},
            {{"question": "french_question3", "answer": "french_answer3"}}
        ]
        """
        
        questions_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": questions_prompt}],
            temperature=0.7
        )
        
        try:
            questions_list = eval(questions_response.choices[0].message.content.strip())
        except:
            st.error("Error parsing questions response")
            questions_list = [
                {"question": "Comment allez-vous?", "answer": "Je vais bien."}
            ]
        
        return vocab_list, questions_list
    except Exception as e:
        st.error(f"Error generating content: {str(e)}")
        return None, None
