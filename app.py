from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/api/decision")
async def decision(request: Request):
    body = await request.json()

    # --- Handshake ---
    if body.get("handshake", False):
        return JSONResponse({
            "ok": True,
            "student_email": "jaakta@taltech.ee",
            "algorithm_name": "BeerBotSimple",
            "version": "v1.0.0",
            "supports": {"blackbox": True, "glassbox": False},
            "message": "BeerBot ready"
        })

    # --- Simple weekly decision logic ---
    weeks = body.get("weeks", [])
    if not weeks:
        # Default order if no data
        return JSONResponse({
            "orders": {"retailer": 10, "wholesaler": 10, "distributor": 10, "factory": 10}
        })

    last = weeks[-1]
    r = last["roles"]["retailer"]

    # Simple deterministic rule
    order = max(0, r["incoming_orders"] + r["backlog"] - r["inventory"] + 5)
    orders = {
        "retailer": order,
        "wholesaler": order,
        "distributor": order,
        "factory": order
    }

    return JSONResponse({"orders": orders})
