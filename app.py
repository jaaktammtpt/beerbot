from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from typing import Dict, List
from math import ceil
import statistics

app = FastAPI()

# --- Handshake vastus ---
@app.post("/api/decision")
async def beerbot_decision(request: Request):
    body = await request.json()

    # 🖐️ HANDSHAKE samm
    if body.get("handshake", False):
        return {
            "ok": True,
            "student_email": "jaakta@taltech.ee",  # <-- muuda enda email
            "algorithm_name": "BullwhipBreaker",
            "version": "v1.0.0",
            "supports": {"blackbox": True, "glassbox": False},
            "message": "BeerBot ready"
        }

    # 🧠 WEEKLY SIMULATION samm
    weeks = body.get("weeks", [])
    if not weeks:
        return {"orders": {"retailer": 10, "wholesaler": 10, "distributor": 10, "factory": 10}}

    last = weeks[-1]  # viimase nädala seis
    roles = last["roles"]

    # --- Otsustusalgoritm (blackbox) ---
    def compute_order(role_name: str):
        role_data = roles[role_name]

        # viimase 3 nädala keskmine nõudlus
        demands = []
        for w in weeks[-3:]:
            try:
                demands.append(w["roles"][role_name]["incoming_orders"])
            except KeyError:
                pass

        avg_demand = sum(demands) / len(demands) if demands else 10
        target_inventory = int(1.5 * avg_demand)

        inventory = role_data["inventory"]
        backlog = role_data["backlog"]

        order = max(0, target_inventory + backlog - inventory)
        return int(order)

    # arvuta iga rolli tellimus
    orders = {
        "retailer": compute_order("retailer"),
        "wholesaler": compute_order("wholesaler"),
        "distributor": compute_order("distributor"),
        "factory": compute_order("factory")
    }

    return {"orders": orders}
