from fastapi import FastAPI, Request
import httpx, os

app = FastAPI()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_IDS = os.environ["CHAT_IDS"].split(",")

@app.post("/webhook")
async def webhook(request: Request):
    message = (await request.body()).decode("utf-8")
    async with httpx.AsyncClient() as client:
        for chat_id in CHAT_IDS:
            await client.post(
                f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                json={"chat_id": chat_id.strip(), "text": message}
            )
    return {"ok": True}
