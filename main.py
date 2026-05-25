from fastapi import FastAPI, Request, Response
import httpx, os

app = FastAPI()

BOT_TOKEN = os.environ["BOT_TOKEN"]
CHAT_IDS = os.environ["CHAT_IDS"].split(",")

@app.api_route("/health", methods=["GET", "HEAD"])
async def health():
    return {"status": "ok"}

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
