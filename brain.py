import ollama

def parse_intent(user_text):
    system_prompt = (
        "You are Chiron's Brain. Categorize the user's request.\n"
        "1. If they want to stop, exit, or shutdown, reply ONLY: ACTION:SHUTDOWN\n"
        "2. If they want an Excel sheet, reply ONLY: ACTION:CREATE_EXCEL|[location]\n"
        "3. Otherwise, give a short reply."
    )
    # ... rest of the ollama code remains the same
    # ... rest of the ollama code ...
    
    response = ollama.chat(model='llama3.1', messages=[
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_text},
    ])
    
    return response['message']['content']