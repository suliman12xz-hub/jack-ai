from openai import OpenAI
import os
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def open_app(app_name):
    os.system(f'open -a "{app_name}"')

while True:
    user = input("Jack> ")

    if user.lower() == "exit":
        break

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are Jack AI on Mo's Mac.
Decide if the user wants to open an app.

Reply ONLY with one of these:
OPEN_CHROME
OPEN_SAFARI
OPEN_CALCULATOR
OPEN_TERMINAL
CHAT

If the user wants YouTube, Google, internet, browser, or website, choose OPEN_CHROME.
If the user wants math/calculation, choose OPEN_CALCULATOR.
"""
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )

    action = response.choices[0].message.content.strip()

    if action == "OPEN_CHROME":
        print("Opening YouTube...")
        os.system('open "https://youtube.com"')

    elif action == "OPEN_SAFARI":
        print("Opening Safari...")
        open_app("Safari")

    elif action == "OPEN_CALCULATOR":
        print("Opening Calculator...")
        open_app("Calculator")

    elif action == "OPEN_TERMINAL":
        print("Opening Terminal...")
        open_app("Terminal")

    else:
        print("I can chat later. For now I can open apps.")
