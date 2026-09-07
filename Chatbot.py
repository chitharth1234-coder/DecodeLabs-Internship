responses = {
    "hi": "Hello there! How can I help you?",
    "hello": "Hello there! How can I help you?",
    "hey": "Hello there! How can I help you?",
    "how are you": "I'm just a bot, but I'm doing great!",
    "your name": "I'm ChatBot 1.0, nice to meet you!",
    "who are you": "I'm ChatBot 1.0, nice to meet you!"
}

exit_commands = {"bye", "exit", "quit"}

def main():
    print("Bot: Hi! I'm a simple chatbot. Type 'bye' to exit.")
    while True:
        raw_input_text = input("You: ")
        clean_input = raw_input_text.strip().lower()

        if clean_input in exit_commands:
            print("Bot: Goodbye! Have a great day!")
            break

        reply = responses.get(clean_input, "Sorry, I didn't understand that. Try again?")
        print(f"Bot: {reply}")

if __name__ == "__main__":
    main()