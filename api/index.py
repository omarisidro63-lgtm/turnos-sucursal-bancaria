from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Lock
from time import time

app = Flask(__name__)
CORS(app)
lock = Lock()
tickets = []
counters = {i: {"id": i, "busy": False, "current": None} for i in range(1, 5)}

@app.get("/api/health")
def health():
    return jsonify({"ok": True, "service": "turnos-sucursal"})

@app.get("/api/state")
def state():
    with lock:
        return jsonify({"tickets": tickets, "counters": list(counters.values())})

@app.post("/api/tickets")
def create_ticket():
    with lock:
        number = max((t["id"] for t in tickets), default=0) + 1
        ticket = {"id": number, "code": f"A{number:02d}", "created": int(time() * 1000), "status": "waiting"}
        tickets.append(ticket)
        return jsonify(ticket), 201

@app.post("/api/counters/<int:counter_id>/call")
def call_next(counter_id):
    with lock:
        counter = counters.get(counter_id)
        if not counter:
            return jsonify({"error": "Ventanilla no encontrada"}), 404
        if counter["busy"]:
            return jsonify({"error": "La ventanilla está ocupada"}), 409
        ticket = next((t for t in tickets if t["status"] == "waiting"), None)
        if not ticket:
            return jsonify({"error": "No hay turnos esperando"}), 404
        ticket.update(status="called", counter=counter_id)
        counter.update(busy=True, current=ticket["code"])
        return jsonify({"ticket": ticket, "counter": counter})

@app.post("/api/counters/<int:counter_id>/finish")
def finish(counter_id):
    with lock:
        counter = counters.get(counter_id)
        if not counter:
            return jsonify({"error": "Ventanilla no encontrada"}), 404
        current = counter["current"]
        for ticket in tickets:
            if ticket["code"] == current:
                ticket["status"] = "done"
                break
        counter.update(busy=False, current=None)
        return jsonify({"counter": counter, "message": "Ventanilla disponible"})
