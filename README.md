# Telegram ChatBot for Fun

Welcome to the Telegram ChatBot for Fun repository! This is a simple Telegram chatbot designed for a single Telegram group of friends to have fun. The bot uses the OpenAI GPT-3.5 Turbo model to generate creative and context-aware responses. This README provides information on setting up and using the bot.

## Features

- **Contextual Responses**: The bot generates responses based on the context of the conversation within the group, creating engaging and relevant replies.

- **Mention Detection**: Mention the bot in the group chat, and it will respond with witty and fun replies.

- **Database Integration**: Messages are stored in a PostgreSQL database to maintain a history of the conversation.

## Prerequisites

Before running the bot, you need to set up the following environment variables:

- `DB_CONNECTION_STRING`: The connection string for your PostgreSQL database.
- `GROUP_ID`: The ID of the Telegram group where the bot will be active.
- `BOT_TOKEN`: The Telegram bot token.
- `CHAT_GPT_API_KEY`: Your OpenAI API key.

## Getting Started

Follow these steps to set up and run the bot:

1. Clone the repository:

   ```shell
   git clone [https://github.com/your-username/telegram-chat-bot.git](https://github.com/nazarii-piontko/bazinga-chat-bot.git)
   ```

2. Install the required dependencies:

   ```shell
   pip3 install -r requirements.txt
   ```

3. Set up the required environment variables in your environment or a `.env` file (an example of a `.env` file is here [`.env.local`](.env.local)).

4. Run the `main.py` script to start the bot:

   ```shell
   python3 main.py
   ```

## Usage

Here's how to interact with the bot in your Telegram group:

- Mention the bot's username in the group chat to trigger a response from the bot.
- The bot will generate creative and context-aware responses based on the previous messages in the conversation.

## Database Integration

The bot uses a PostgreSQL database to store and manage messages. The `messages` table in the database stores the following information:

- `id`: Message ID
- `msg_timestamp`: Timestamp of the message
- `user_name`: Name of the user who sent the message
- `text`: Message text

## Customization

You can customize the bot's behavior and responses by modifying the code in `main.py`. Feel free to adjust the context length, add new response rules, or change the bot's behavior to suit your group's preferences.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

This project makes use of the OpenAI GPT-3.5 Turbo model for generating creative responses.

## Disclaimer

Please use this bot responsibly and for entertainment purposes only. Do not engage in any malicious or harmful activities. Ensure that your usage complies with Telegram's terms of service.

**Note**: When making your code public, take precautions to handle sensitive data and API keys securely.
