from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import re

@app.get("/execute")
async def execute(q: str):
    if "status of ticket" in q:
        match = re.search(r"ticket (\d+)", q)
        if match:
            ticket_id = int(match.group(1))
            return {
                "name": "get_ticket_status",
                "arguments": json.dumps({"ticket_id": ticket_id}),
            }
    return {"name": "not_implemented", "arguments": "{}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
