# array_alert

A lightweight webhook server that bridges **TradingView alerts** to **Telegram**. When your TradingView indicator fires an alert, it POSTs the message to this server, which instantly forwards it to one or more Telegram chats.

---

## How It Works

```
TradingView Alert  ──►  POST /webhook  ──►  Telegram Bot  ──►  Your Chat(s)
```

1. Your TradingView indicator/strategy fires an alert.
2. TradingView sends the alert message as a plain-text POST request to your hosted webhook URL.
3. This server receives it and forwards it to every Telegram chat ID you configured.

---

## Requirements

- Python 3.8+
- A [Telegram Bot](https://core.telegram.org/bots#how-do-i-create-a-bot) token
- One or more Telegram chat IDs
- A hosting platform that exposes a public HTTPS URL (e.g. Heroku, Railway, Render)

---

## Environment Variables

| Variable    | Description                                                                 |
|-------------|-----------------------------------------------------------------------------|
| `BOT_TOKEN` | Your Telegram bot token from [@BotFather](https://t.me/BotFather)          |
| `CHAT_IDS`  | Comma-separated list of Telegram chat IDs to forward alerts to (e.g. `123456789,987654321`) |
| `PORT`      | Port the server listens on (set automatically by most hosting platforms)    |

---

## Setup

### 1. Create a Telegram Bot

1. Open Telegram and start a chat with [@BotFather](https://t.me/BotFather).
2. Send `/newbot` and follow the prompts to create your bot.
3. Copy the **API token** — this is your `BOT_TOKEN`.

### 2. Get Your Chat ID

1. Start a conversation with your bot (send it any message).
2. Open this URL in your browser (replace `<BOT_TOKEN>` with yours):
   ```
   https://api.telegram.org/bot<BOT_TOKEN>/getUpdates
   ```
3. Find `"chat": {"id": ...}` in the response — that number is your `CHAT_ID`.

For a group chat: add the bot to the group, send a message, then use the same URL above to find the group's chat ID (it will be a negative number).

### 3. Deploy

#### Heroku

```bash
heroku create your-app-name
heroku config:set BOT_TOKEN=your_bot_token
heroku config:set CHAT_IDS=123456789,987654321
git push heroku main
```

#### Railway / Render

1. Connect your GitHub repository.
2. Set the environment variables `BOT_TOKEN` and `CHAT_IDS` in the platform's dashboard.
3. The `Procfile` handles the start command automatically.

#### Local (for testing)

```bash
pip install -r requirements.txt
export BOT_TOKEN=your_bot_token
export CHAT_IDS=123456789
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

## Connecting TradingView

1. Open your indicator or strategy in TradingView.
2. Click the **Alerts** (clock) icon → **Create Alert**.
3. Under **Notifications**, enable **Webhook URL** and enter your server's URL:
   ```
   https://your-app-name.herokuapp.com/webhook
   ```
4. In the **Message** field, write the alert text you want to receive on Telegram. You can use TradingView's dynamic placeholders:
   - `{{ticker}}` — symbol name (e.g. `BTCUSDT`)
   - `{{close}}` — closing price
   - `{{time}}` — alert trigger time
   - `{{exchange}}` — exchange name

   Example message:
   ```
   🚨 {{ticker}} alert on {{exchange}}
   Price: {{close}}
   Time: {{time}}
   ```

5. Click **Create** — alerts will now arrive in your Telegram chat(s).

---

## API Reference

### `POST /webhook`

Forwards the raw request body as a text message to all configured Telegram chats.

**Request body:** plain text string (the alert message)

**Response:**
```json
{ "ok": true }
```

---

## Project Structure

```
array_alert/
├── main.py           # FastAPI app with the /webhook endpoint
├── requirements.txt  # Python dependencies
├── Procfile          # Process definition for Heroku/Railway/Render
└── README.md
```

---

## Dependencies

| Package   | Purpose                                      |
|-----------|----------------------------------------------|
| `fastapi` | Web framework for the webhook endpoint       |
| `uvicorn` | ASGI server to run the FastAPI app           |
| `httpx`   | Async HTTP client to call the Telegram API   |
