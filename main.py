#!/usr/bin/env python3
import datetime
import logging
import os

import openai
import psycopg2
import telegram.ext.filters
from telegram import Update, Message
from telegram._bot import BT
from telegram.ext import MessageHandler, CallbackContext, ApplicationBuilder


# Read environment variables
DB_CONNECTION_STRING = os.environ['DB_CONNECTION_STRING']
GROUP_ID = int(os.environ['GROUP_ID'])
BOT_TOKEN = os.environ['BOT_TOKEN']
CHAT_GPT_API_KEY = os.environ['CHAT_GPT_API_KEY']

CONTEXT_LEN = 20

# Configure OpenAI
openai.api_key = CHAT_GPT_API_KEY

# Connect to the database
conn = psycopg2.connect(DB_CONNECTION_STRING)
conn.autocommit = True
cursor = conn.cursor()


def create_table_if_not_exists():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id BIGINT PRIMARY KEY,
            msg_timestamp TIMESTAMP WITHOUT TIME ZONE,
            user_name TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)


def save_message_to_db(msg_id: int, msg_timestamp: datetime.datetime, user_name: str, text: str):
    cursor.execute("""
        INSERT INTO messages (id, msg_timestamp, user_name, text)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE SET text = EXCLUDED.text;

        DELETE FROM messages
        WHERE id < (
            SELECT MIN(top.id)
            FROM (
                SELECT id
                FROM messages
                ORDER BY id DESC
                LIMIT %s
            ) AS top);
    """, (msg_id, msg_timestamp, user_name, text, CONTEXT_LEN))


def get_context_messages():
    cursor.execute("""
        SELECT msg_timestamp, user_name, text
        FROM messages
        ORDER BY id DESC
        LIMIT %s
    """, (CONTEXT_LEN,))

    last_messages = [(row[0], row[1], row[2]) for row in cursor.fetchall()]
    last_messages.reverse()

    return last_messages


def generate_response(context_messages):
    messages = [
        {"role": "system", "content": "Ти бот жартівник у чат кімнаті із групою друзів. Не починай свої повідомлення з 'Повідомлення від ...'"}
    ]

    for m in context_messages[:-1]:
        messages.append({"role": "assistant", "content": f"Повідомлення від {m[1]} ({m[0]}). {m[2]}"})

    last_message = context_messages[-1]
    messages.append({"role": "user", "content": f"{last_message[2]}"})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    return response.choices[0].message.content


def is_bot_mentioned(message: Message, bot: BT):
    if message.reply_to_message is not None and \
       message.reply_to_message.from_user.is_bot and \
       message.reply_to_message.from_user.id == bot.id:
        return True

    if message.entities is not None:
        for entity in message.entities:
            if entity.type == "mention":
                mention_text = message.text[entity.offset:entity.offset + entity.length]
                if mention_text == bot.name:
                    return True
            elif entity.type == "text_mention":
                if entity.user.id == bot.id:
                    return True

    return False


async def handle_message(update: Update, context: CallbackContext):
    try:
        message = update.message or update.edited_message

        if message is None:
            return

        if message.chat_id != GROUP_ID:
            return

        save_message_to_db(message.message_id, message.date or message.edit_date, message.from_user.full_name, message.text)

        if is_bot_mentioned(message, context.bot):
            last_messages = get_context_messages()
            response = generate_response(last_messages)

            reply_message = await message.reply_text(response)

            save_message_to_db(reply_message.message_id, reply_message.date or reply_message.edit_date, reply_message.from_user.full_name, reply_message.text)
    except Exception as e:
        logging.error('Handle Telegram message error: %s', e, exc_info=e)


def main():
    logging.basicConfig(level=logging.INFO)

    create_table_if_not_exists()

    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = MessageHandler(telegram.ext.filters.TEXT, handle_message)
    application.add_handler(start_handler)

    application.run_polling()


if __name__ == '__main__':
    main()
