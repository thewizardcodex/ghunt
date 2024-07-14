from fastapi import FastAPI, Path, HTTPException
from fastapi.responses import JSONResponse
import subprocess
import json
import os
import requests
import re
import httpx

app = FastAPI()

@app.get("/api/{email}")
async def email_api(email: str = Path(...)):
    try:
        process = subprocess.Popen(['python3','main.py', 'email', '--json', f'{email}.json', email], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.wait() 
        if os.path.exists(f'{email}.json'):
            with open(f'{email}.json', 'r') as file:
                email_data = json.load(file)
                os.remove(f'{email}.json')
            return email_data
        else:
            raise HTTPException(status_code=404, detail="Email data not found")
    except subprocess.CalledProcessError:
        raise HTTPException(status_code=500, detail="Failed to execute command")

