import ollama
response = ollama.chat(
    model="llama3.2:3b",
    messages=[
        {"role": "user",
         "content": "Defination of AI in 2 lines,and 3 main types of ai in bullet points"
         " "
         }
    ])
print(response["message"]["content"])
