import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-3-5-sonnet-20241022",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": "Hello, Claude"
    }]
)

for block in message.content:
    if block.type == "text":
        print(block.text)