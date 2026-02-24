from fastapi import FastAPI, Request
from datetime import datetime

app = FastAPI()


@app.get("/")
def health():
    return {"status": "running"}


@app.post("/status-webhook")
async def status_webhook(request: Request):
    payload = await request.json()

    meta = payload.get("meta", {})
    event_type = meta.get("type", "unknown")

    # We only care about incident lifecycle events
    if not event_type.startswith("incident"):
        return {"ignored": True}

    incident = payload.get("data", {}).get("incident", {})

    product = incident.get("name", "Unknown Product")

    updates = incident.get("incident_updates", [])
    latest_update = updates[-1] if updates else {}

    message = latest_update.get("body", "No status message")
    timestamp = latest_update.get(
        "created_at",
        datetime.utcnow().isoformat()
    )

    print("\n==============================")
    print(f"[{timestamp}]")
    print(f"Product: {product}")
    print(f"Status: {message}")
    print("==============================\n")

    return {"received": True}