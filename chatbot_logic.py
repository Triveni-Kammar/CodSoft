from datetime import datetime

def chatbot_response(user_input):
    text = user_input.lower()
    if "hello" in text or "hi" in text:
        return "Hello! How can I help you today?"
    elif "how are you" in text:
        return "I'm just a bot, but I'm doing great! Thanks for asking."
    elif "your name" in text:
        return "I'm ChatBot, your simple assistant."
    elif "help" in text:
        return "You can ask me about the weather, time, or just say hi."
    elif "weather" in text:
        return "I can't check the weather right now, but I hope it's nice where you are!"
    elif "time" in text:
        now = datetime.now().strftime("%H:%M:%S")
        return f"The current time is {now}."
    elif "bye" in text or "exit" in text:
        return "Goodbye! Have a nice day!"
    else:
        return "Sorry, I didn't understand that. Can you rephrase?"
