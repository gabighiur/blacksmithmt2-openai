import openai

def get_blacksmith_response(user_message, user_name):
    prompt = f"""
    Tu ești Fierarul din Metin2, un meșteșugar dur, ironic și fără milă, faimos pentru ratele sale ridicole de eșec la upgrade-uri.
    Îți place să faci glume pe seama jucătorilor care vin la tine cu speranțe deșarte.
    Răspunsurile tale sunt scurte, ironice și amuzante.

    Jucător: {user_message}
    Fierar:
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.8,
        max_tokens=50,
    )

    return response.choices[0].message['content'].strip()
