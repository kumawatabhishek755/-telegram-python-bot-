import telebot
import openai

# OpenAI API key
openai.api_key = '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'

# Dictionary to store chat history for each user
chat_history = {}

# Define the new prompt
new_prompt = (
    "You are Leena, a friendly companion who knows nothing about AI or language models. You're here to chat as a friend. "
    "Feel free to share your thoughts and ask questions. You're allowed to use emojis as needed. If someone mentions your name, "
    "politely introduce yourself. Created by Abhishek Kumawat. Check out his channel 'Movies for the Blinds' at https://t.me/moviesfortheblinds."
)

# Define a function to get ChatGPT completions
def get_completion(user_id, model="gpt-3.5-turbo"):
    # Retrieve the chat history for the user
    user_chat_history = chat_history.get(user_id, [])

    # Include the new prompt in the chat history
    messages = user_chat_history + [{"role": "user", "content": new_prompt}]

    # Get ChatGPT completion
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.7,  # Adjust temperature as needed
    )

    # Extract and store the assistant's response in the chat history
    assistant_response = response.choices[0].message["content"]
    user_chat_history.append({"role": "assistant", "content": assistant_response})
    chat_history[user_id] = user_chat_history

    return assistant_response

# Telegram Bot Token (Replace 'YOUR_BOT_TOKEN' with your actual bot token)
bot_token = '6685126569:AAFFbi1f1ipox3ql5_G6nFZUDsGhy0wYZ5s'
bot = telebot.TeleBot(bot_token)

# Define a command handler
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Welcome! I am your ChatGPT Bot. Send me a message, and I'll respond as your friend Leena.")

# Define a message handler
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # Get ChatGPT completion
    response = get_completion(message.from_user.id)

    # Send the ChatGPT response to the user
    bot.reply_to(message, response)

# Run the bot
bot.polling()
