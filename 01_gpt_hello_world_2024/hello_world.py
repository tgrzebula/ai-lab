from openai import OpenAI
client = OpenAI()

# Call the openai chat.completions endpoint, with gpt-3.5-turbo
response = client.chat.completions.create(model='gpt-3.5-turbo',
    messages=[
      {'role': 'user', 'content': 'Hello World!'}
  ])

# Extract the response
print(response.choices[0].message.content)