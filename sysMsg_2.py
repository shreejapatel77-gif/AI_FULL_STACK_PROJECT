import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {
            "role": "system",
            "content": "teaching you are 5 year old child,give 2-3 lines answer."},
        {
            "role": "user",
            "content": "Explain ML"
        }
    ])
print(response["message"]["content"])
