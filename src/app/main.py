from fastapi import FastAPI, Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.db.models import init_db
from app.bot import parsers, handlers
from app.clients.whatsapp import WhatsAppClient

app = FastAPI()
client = WhatsAppClient()

init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/webhook")
async def webhook(request: Request, db: Session = Depends(get_db)):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    messages = []
    if "entry" in data:
        for entry in data.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                if "messages" in value:
                    messages.extend(value["messages"])

    if not messages:
        return {"status": "ignored"}

    for message in messages:
        sender = message.get("from")
        if not sender:
            continue

        if message.get("type") != "text":
            continue

        text_body = message.get("text", {}).get("body", "")
        if not text_body:
            continue

        command = parsers.parse_command(text_body)
        if command:
            response_text = handlers.execute_command(command, db)
        else:
            response_text = "I didn't understand that. Try 'help'."

        client.send_message(to=sender, text=response_text)

    return {"status": "ok"}
