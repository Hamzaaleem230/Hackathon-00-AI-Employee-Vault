from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
import os
import json
import shutil

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Folder list define kar di hai taake file preview sab jagah dhoond sake
BASE_DIRS = ["Pending_Approval", "Approved", "Rejected", "Done"]

def get_ai_details():
    """decisions.json se data nikaal kar dictionary banata hai"""
    details = {}
    if os.path.exists("Logs/decisions.json"):
        with open("Logs/decisions.json", "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    # File name ko key bana rahe hain taake dashboard pe asani se mil jaye
                    details[data['file']] = data
                except:
                    continue
    return details

def update_json_status(filename, new_status):
    """decisions.json mein file ki status update karta hai taake dashboard refresh ho sake"""
    lines = []
    json_path = "Logs/decisions.json"
    
    if os.path.exists(json_path):
        # 1. Purani file read karke data update karna
        with open(json_path, "r") as f:
            for line in f:
                try:
                    data = json.loads(line)
                    if data['file'] == filename:
                        data['decision'] = new_status
                        data['reasoning'] = f"Manually {new_status} by Admin."
                    lines.append(json.dumps(data))
                except:
                    continue
        
        # 2. Updated data wapas file mein likhna
        with open(json_path, "w") as f:
            for line in lines:
                f.write(line + "\n")

@app.get("/")
async def dashboard(request: Request):
    ai_info = get_ai_details()
    
    # folders list check
    folders = {
        "pending": os.listdir("Pending_Approval") if os.path.exists("Pending_Approval") else [],
        "approved": os.listdir("Approved") if os.path.exists("Approved") else [],
        "rejected": os.listdir("Rejected") if os.path.exists("Rejected") else [],
        "done": os.listdir("Done") if os.path.exists("Done") else []
    }
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "folders": folders,
        "ai_info": ai_info
    })

@app.get("/get-file-content/{filename}")
async def get_file_content(filename: str):
    """File ka content kisi bhi folder se nikaal kar bhejta hai"""
    for folder in BASE_DIRS:
        file_path = os.path.join(folder, filename)
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                return {"content": content}
            except Exception as e:
                return {"content": f"Error reading file: {str(e)}"}
    return {"content": "File not found!"}

@app.post("/manual-action")
async def manual_action(request: Request):
    data = await request.json()
    filename = data['filename']
    new_status = data['action'] # 'Approved' ya 'Rejected'
    
    # Check current potential locations (Kahan se file uthani hai)
    sources = ["Pending_Approval", "Approved", "Rejected", "Done"]
    current_path = None
    
    for src in sources:
        temp_path = os.path.join(src, filename)
        if os.path.exists(temp_path):
            current_path = temp_path
            break
        
    target_path = os.path.join(new_status, filename)

    try:
        if current_path:
            # 1. File ko physically move karein
            shutil.move(current_path, target_path)
            
            # 2. JSON file mein record update karein taake dashboard badal jaye
            update_json_status(filename, new_status)
            
            return {"message": f"File {filename} moved to {new_status} and updated in Logs!"}
        else:
            return {"message": "File not found in any folder!", "status": "error"}
            
    except Exception as e:
        return {"message": str(e), "status": "error"}