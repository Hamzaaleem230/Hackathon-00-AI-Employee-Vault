from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import json
import shutil
import psycopg2 # Neon/PostgreSQL ke liye
from psycopg2.extras import RealDictCursor

# .env load karna zaroori hai local error fix karne ke liye
load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

BASE_DIRS = ["Pending_Approval", "Approved", "Rejected", "Done", "Tasks/Completed", "Tasks/Failed"]
DATABASE_URL = os.getenv("NEON_DB_URL") 

def get_db_connection():
    # SSL mode require zaroori hai Neon ke liye
    return psycopg2.connect(DATABASE_URL)

def init_db():
    """Neon mein table banata hai agar na ho"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS decisions (
                id SERIAL PRIMARY KEY,
                filename TEXT UNIQUE,
                decision TEXT,
                confidence FLOAT,
                reasoning TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database Init Error: {e}")

# App start hote hi table check karega
@app.on_event("startup")
def startup_event():
    init_db()

def get_ai_details():
    """Neon se data nikaal kar dictionary banata hai"""
    details = {}
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM decisions")
        rows = cur.fetchall()
        for row in rows:
            details[row['filename']] = {
                "file": row['filename'],
                "decision": row['decision'],
                "confidence": row['confidence'],
                "reasoning": row['reasoning']
            }
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Fetch Error: {e}")
    return details

def update_db_status(filename, new_status, confidence=0.0, reasoning=""):
    """Neon mein record insert ya update (UPSERT) karta hai"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO decisions (filename, decision, confidence, reasoning)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (filename) DO UPDATE SET
            decision = EXCLUDED.decision,
            reasoning = EXCLUDED.reasoning,
            confidence = EXCLUDED.confidence
        ''', (filename, new_status, confidence, reasoning))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        print(f"DB Update Error: {e}")

@app.get("/")
async def dashboard(request: Request):
    ai_info = get_ai_details()
    # Folder counting logic
    folders = {
        "pending": os.listdir("Pending_Approval") if os.path.exists("Pending_Approval") else [],
        "approved": os.listdir("Approved") if os.path.exists("Approved") else [],
        "rejected": os.listdir("Rejected") if os.path.exists("Rejected") else [],
        "done": os.listdir("Done") if os.path.exists("Done") else []
    }
    return templates.TemplateResponse("index.html", {
        "request": request, "folders": folders, "ai_info": ai_info
    })

@app.get("/history")
async def view_history(request: Request):
    """Sari purani decisions ki history dikhane ke liye"""
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    # Latest decisions sab se upar dikhane ke liye order by timestamp
    cur.execute("SELECT * FROM decisions ORDER BY timestamp DESC")
    history = cur.fetchall()
    cur.close()
    conn.close()
    
    return templates.TemplateResponse("history.html", {
        "request": request, 
        "history": history
    })
    
@app.post("/delete-history/{filename}")
async def delete_single_history(filename: str):
    """Ek single file ka record database se delete karne ke liye"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM decisions WHERE filename = %s", (filename,))
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": f"{filename} deleted!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.post("/clear-all-history")
async def clear_all_history():
    """Poori history saaf karne ke liye"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM decisions")
        conn.commit()
        cur.close()
        conn.close()
        return {"status": "success", "message": "All history cleared!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/get-file-content/{filename}")
async def get_file_content(filename: str):
    """File preview ke liye content read karta hai"""
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
    """Admin manual buttons ke liye logic"""
    data = await request.json()
    filename, new_status = data['filename'], data['action']
    
    current_path = None
    for src in BASE_DIRS:
        temp_path = os.path.join(src, filename)
        if os.path.exists(temp_path):
            current_path = temp_path
            break
        
    if current_path:
        try:
            target_path = os.path.join(new_status, filename)
            if os.path.exists(target_path):
                os.remove(target_path)
            shutil.move(current_path, target_path)
            
            # Neon Database mein status update karein
            update_db_status(filename, new_status, 1.0, f"Manually {new_status} by Admin.")
            return {"message": f"File {filename} moved to {new_status} and Neon DB updated!"}
        except Exception as e:
            return {"message": str(e), "status": "error"}
    return {"message": "File not found!", "status": "error"}