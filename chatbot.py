import json
import random
import urllib.parse
import urllib.request
from datetime import datetime


def search_wikipedia(question):
    """Look up the question on Wikipedia and return a short answer."""
    text = question.lower().strip().rstrip("?").strip()
    fillers = ("can you tell me", "could you tell me", "please tell me",
               "tell me about", "tell me", "what is the", "what is a",
               "what is an", "what is", "what are", "what was", "who is",
               "who was", "who are", "where is", "when was", "when is",
               "how does", "how do", "why is", "why do", "explain",
               "define", "please", "i want to know about", "i want to know")
    for start in fillers:
        if text.startswith(start + " "):
            text = text[len(start):].strip()
            break

    url = ("https://en.wikipedia.org/w/api.php?action=query&format=json"
           "&generator=search&gsrlimit=1&prop=extracts&exintro=1"
           "&explaintext=1&exsentences=3&gsrsearch="
           + urllib.parse.quote(text))
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "CodeAlphaChatbot/1.0"})
        with urllib.request.urlopen(request, timeout=8) as response:
            data = json.loads(response.read().decode("utf-8"))
        pages = data["query"]["pages"]
        page = list(pages.values())[0]
        return page["extract"].strip()
    except Exception:
        return None


def get_response(user_input):
    """Return a reply based on what the user typed."""
    user_input = user_input.lower().strip()
    words = user_input.replace("?", "").replace("!", "").replace(",", "").replace(".", "").split()

    if "bye" in words or "goodbye" in words or "exit" in words:
        return "Goodbye!"
    elif "how are you" in user_input:
        return "I'm fine, thanks! How about you?"
    elif "about you" in user_input or "yourself" in words or "your name" in user_input or "who are you" in user_input:
        return "I am a simple chatbot created with Python for the CodeAlpha internship. Ask me anything!"
    elif "help" in words:
        return ("Sure, I'm here to help! Try: what is python, who is Albert Einstein, "
                "tell me a joke, what is the time, or say bye.")
    elif "time" in words:
        return "The time now is " + datetime.now().strftime("%I:%M %p")
    elif "date" in words or "today" in words:
        return "Today's date is " + datetime.now().strftime("%d %B %Y")
    elif "joke" in words:
        jokes = [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "Why did the Python programmer wear glasses? Because he couldn't C!",
            "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
        ]
        return random.choice(jokes)
    elif "thanks" in words or "thank" in words:
        return "You're welcome!"
    elif words and words[0] in ("hello", "hi", "hey"):
        return "Hi! How can I help you today?"
    elif "fine" in words or "good" in words:
        return "Great to hear that!"

    # Everything else: search for the answer on Wikipedia
    answer = search_wikipedia(user_input)
    if answer:
        return answer
    return ("Sorry, I couldn't find an answer for that. Check your internet "
            "connection or try asking in a different way.")


def main():
    print("===== BASIC CHATBOT =====")
    print("Ask me anything. Type 'bye' to end the chat.\n")

    while True:
        user_input = input("You: ")

        if user_input.strip() == "":
            print("Bot: Please type something.")
            continue

        reply = get_response(user_input)
        print("Bot:", reply)
        print()

        if reply == "Goodbye!":
            break


main()
