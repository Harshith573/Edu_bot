# Description

This is the main file for the chatbot. It is used to initialize the database and the large language model. It also contains the conversation function which is used to generate the response for the user input. The main function is used to initialize the Telegram bot.

## Initialization

### Initialize Database

To initialize the database, use the `initialize_database` function. Provide the appropriate parameters such as `chunk_size` and `chunk_overlap`.

### Initialize Language Model Chain

To initialize the language model chain, use the `initialize_llmchain` function. Specify the model name, temperature, max_tokens, top_k, and vector database.

### Conversation Function

The `conversation` function generates responses for user input based on the initialized database and language model chain.

## Telegram Bot

### Telegram Bot Token

Replace the `TELEGRAM_BOT_TOKEN` variable with your Telegram bot token in `main.py`.

### Start Command

The `/start` command initializes the bot and welcomes the user.

### Message Handler

Handles text messages sent by the user and calls the `handle_text` function.

### Document Handler

Handles documents sent by the user and calls the `handle_document` function.

## Setup Instructions

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your_username/edu-bot.git
   cd edu-bot
   ```

2. **Install Dependencies:**
   Make sure you have Python installed. Then, install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. **Telegram Bot Token:**
   Obtain a Telegram Bot Token by following the [BotFather](https://core.telegram.org/bots#6-botfather) instructions and replace the `TELEGRAM_BOT_TOKEN` variable in `main.py` with your token.

4. **Language Model:**
   Specify the Hugging Face model for your language model by replacing the `llm_name1` variable in `main.py` with your desired model name.

5. **PDF File:**
   If you're using a PDF document for the chatbot's knowledge base, provide the path to the PDF file by replacing the `file_path` variable in `main.py`.

6. **Run the Bot:**
   Start the Telegram bot by running:
   ```bash
   python main.py
   ```

## Usage

- Start the bot by sending `/start` in your Telegram chat.
- Ask questions related to the Computer Network Module-1.
- The bot will respond with relevant answers based on the provided document and the configured language model.

## Additional Notes

- This bot uses a conversational retrieval chain to interact with users.
- Feel free to customize the bot's functionality according to your requirements.
