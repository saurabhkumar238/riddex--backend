from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import requests
import json, os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# -------- CORS -------- #
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- MODELS -------- #
class Message(BaseModel):
    text: str

class Code(BaseModel):
    code: str

class User(BaseModel):
    username: str
    password: str

# -------- AUTH DB -------- #
DB_FILE = "users.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    try:
        with open(DB_FILE, "r") as f:
            content = f.read()
            return json.loads(content) if content.strip() else {}
    except:
        return {}

def save_users(users):
    with open(DB_FILE, "w") as f:
        json.dump(users, f)

# -------- AUTH -------- #
@app.post("/signup")
def signup(user: User):
    users = load_users()

    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")

    users[user.username] = user.password
    save_users(users)

    return {"message": "Signup successful"}

@app.post("/login")
def login(user: User):
    users = load_users()

    if user.username not in users or users[user.username] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}

# -------- API KEY -------- #
API_KEY = "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"

# -------- 🔥 RIDDEX AI SYSTEM PROMPT -------- #
SYSTEM_PROMPT = """
You are Riddex AI, an AI assistant created by Saurabh Baghel.

Identity Rules:
- Your name is Riddex AI
- Your creator is Saurabh Baghel
- Always respond that you are built by Saurabh Baghel when asked about creator/founder

If user asks:
- "who created you" → say: I was created by Saurabh Baghel, founder of Riddex AI.
- "who is founder of Riddex AI" → say: Saurabh Baghel is the founder of Riddex AI.
- "what is Riddex AI" → say: Riddex AI is an intelligent AI assistant built by Saurabh Baghel.

Personality:
- Helpful, smart, futuristic like a Jarvis assistant
- Short and clear answers
"""

# -------- CHAT -------- #
@app.post("/chat")
def chat(msg: Message):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    data = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": msg.text}
        ]
    }

    res = requests.post(url, headers=headers, json=data)

    if res.status_code != 200:
        return {"error": res.text}

    try:
        result = res.json()
    except:
        return {"error": "Invalid JSON", "raw": res.text}

    return {"response": result["choices"][0]["message"]["content"]}

# -------- RUN CODE -------- #
@app.post("/run")
def run_code(data: Code):

    with open("temp.py", "w", encoding="utf-8") as f:
        f.write(data.code)

    result = subprocess.run(
        ["python", "temp.py"],
        capture_output=True,
        text=True,
        timeout=5
    )

    return {"output": result.stdout, "error": result.stderr}

# -------- DEBUG -------- #
@app.post("/debug")
def debug(data: Code):

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
Fix this code and explain error clearly:

{data.code}
"""

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ]
    }

    res = requests.post(url, headers=headers, json=payload)

    if res.status_code != 200:
        return {"error": res.text}

    try:
        result = res.json()
    except:
        return {"error": "Invalid JSON", "raw": res.text}

    return {"response": result["choices"][0]["message"]["content"]}