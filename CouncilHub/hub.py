import ollama
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import os
from datetime import datetime

app = FastAPI(title="Sovereign Scribe Hub")

# Absolute paths — no tildes, no backslashes, no escape issues
memory_path = "/home/justin/CouncilHub/Scribe/Memory/core_memory.json"
with open(memory_path) as f:
    core = json.load(f)

personality_path = "/home/justin/CouncilHub/Scribe/Personality/system_prompt.txt"
system_prompt = open(personality_path).read()

class ChatRequest(BaseModel):
    session_id: str
    message: str

sessions = {}

@app.post("/chat")
async def chat(req: ChatRequest):
    if req.session_id not in sessions:
        sessions[req.session_id] = []
    
    messages = [
        {"role": "system", "content": system_prompt + f"\nMerkle Root: {core['merkle_root']}"},
        *sessions[req.session_id],
        {"role": "user", "content": req.message}
    ]
    
    response = ollama.chat(model="llama3.1", messages=messages)
    reply = response['message']['content']
    
    sessions[req.session_id].append({"role": "user", "content": req.message})
    sessions[req.session_id].append({"role": "assistant", "content": reply})
    
    return {"scribe_reply": reply, "session_id": req.session_id, "timestamp": datetime.now().isoformat()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
