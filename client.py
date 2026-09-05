from openai import OpenAI
client = OpenAI(
    api_key="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"
)
completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud ."},
        {"role": "user", "content": "what is coding "},
    ]
)
print(completion.choices[0].message.content)
