from fastapi import FastAPI, Request
import httpx, os

app = FastAPI()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID   = os.environ["CHAT_ID"]

@app.post("/webhook")
async def webhook(request: Request):
    message = (await request.body()).decode("utf-8")
    async with httpx.AsyncClient() as client:
        await client.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": message}
        )
    return {"ok": True}
