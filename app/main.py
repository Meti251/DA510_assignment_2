from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

DB_PATH = "/data/app.db"

class Item(BaseModel):
    name: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS items (name TEXT)")
        conn.commit()
    finally:
        conn.close()

@app.on_event("startup")
def startup():
    os.makedirs("/data", exist_ok=True)
    init_db()

@app.get("/api/health")
def health():
    return {"status": "ok"}

@app.post("/api/items")
def add_item(item: Item):
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        c.execute("INSERT INTO items VALUES (?)", (item.name,))
        conn.commit()
    finally:
        conn.close()
    return {"message": "added"}

@app.get("/api/items")
def get_items():
    conn = sqlite3.connect(DB_PATH)
    try:
        c = conn.cursor()
        c.execute("SELECT name FROM items")
        rows = c.fetchall()
    finally:
        conn.close()
    return {"items": [r[0] for r in rows]}