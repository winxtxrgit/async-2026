# light_api.py
# 💡 Smart Lab Lighting System - API Server
# Implements the spec in Readme.md: HTTP REST control + real-time WebSocket broadcast.
# Run: uvicorn light_api:app --port 8000

import asyncio
from time import ctime

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

app = FastAPI(title="💡 Smart Lab Lighting System API")


# --- Light hardware definition (name + simulated delay in seconds) ---
LIGHT_CONFIG = {
    "light_1": {"name": "ไฟหน้าประตู (Light 1)", "delay": 0.5},
    "light_2": {"name": "ไฟโต๊ะปฏิบัติการ A (Light 2)", "delay": 1.2},
    "light_3": {"name": "ไฟโต๊ะปฏิบัติการ B (Light 3)", "delay": 2.0},
    "light_4": {"name": "ไฟกระดานหน้าห้อง (Light 4)", "delay": 0.8},
}


class StatusModel(BaseModel):
    status: str


# --- Per-student state: student_id -> {light_id: {"name","status","delay"}} ---
students_state: dict[str, dict] = {}

# --- Active WebSocket connections: student_id -> list[WebSocket] ---
connections: dict[str, list[WebSocket]] = {}


def get_lights(student_id: str) -> dict:
    """Return this student's lights, creating a fresh all-OFF set on first access."""
    if student_id not in students_state:
        students_state[student_id] = {
            light_id: {"name": cfg["name"], "status": "OFF", "delay": cfg["delay"]}
            for light_id, cfg in LIGHT_CONFIG.items()
        }
    return students_state[student_id]


async def broadcast(student_id: str):
    """Push the full lights payload to every connected dashboard for this student."""
    payload = get_lights(student_id)
    dead = []
    for ws in connections.get(student_id, []):
        try:
            await ws.send_json(payload)
        except Exception:
            dead.append(ws)
    # Drop connections that failed to receive (cleanup).
    for ws in dead:
        connections[student_id].remove(ws)


# ============================ HTTP REST API ============================

@app.get("/api/{student_id}/lights")
async def get_all_lights(student_id: str):
    """1. Get the status of all 4 lights for a student."""
    return get_lights(student_id)


@app.post("/api/{student_id}/lights/{light_id}")
async def control_light(student_id: str, light_id: str, body: StatusModel):
    """2. Turn a light ON/OFF after the simulated hardware delay, then broadcast."""
    lights = get_lights(student_id)

    if light_id not in lights:
        raise HTTPException(status_code=404, detail="ไม่พบหลอดไฟที่ระบุ")

    new_status = body.status.strip().upper()
    if new_status not in ("ON", "OFF"):
        raise HTTPException(status_code=400, detail="สถานะต้องเป็น ON หรือ OFF เท่านั้น")

    delay = lights[light_id]["delay"]
    print(f"{ctime()} | [Student {student_id}] Switching {light_id} -> {new_status} (delay {delay}s)...")
    await asyncio.sleep(delay)  # Simulate physical I/O latency

    lights[light_id]["status"] = new_status
    print(f"{ctime()} | [Student {student_id}] {light_id} is now {new_status}")

    await broadcast(student_id)
    return {
        "student_id": student_id,
        "light_id": light_id,
        "current_status": new_status,
    }


@app.delete("/api/{student_id}/lights/reset")
async def reset_lights(student_id: str):
    """3. Instantly reset all lights back to OFF, then broadcast."""
    lights = get_lights(student_id)
    for light_id in lights:
        lights[light_id]["status"] = "OFF"

    print(f"{ctime()} | [Student {student_id}] All lights reset to OFF")
    await broadcast(student_id)
    return {"message": f"รีเซ็ตไฟทุกดวงของนักเรียน {student_id} เป็น OFF เรียบร้อยแล้ว"}


# ============================ WebSocket Channel ============================

@app.websocket("/ws/{student_id}")
async def lights_ws(websocket: WebSocket, student_id: str):
    """Persistent channel: send current state on connect, then live broadcasts."""
    await websocket.accept()
    connections.setdefault(student_id, []).append(websocket)
    print(f"{ctime()} | [WS] Dashboard connected for student {student_id}")

    # Push the current snapshot immediately upon connection.
    await websocket.send_json(get_lights(student_id))

    try:
        # Keep the connection alive; we only push, but must keep receiving to detect disconnect.
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        connections[student_id].remove(websocket)
        print(f"{ctime()} | [WS] Dashboard disconnected for student {student_id}")


# How to run the server: uvicorn light_api:app --port 8000
