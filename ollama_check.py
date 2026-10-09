import ollama

response = ollama.generate(
    model='llama3.2',
    prompt="why is sky blue?"
)

print(response["response"])
