from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import pickle
from database import db, cursor

app = FastAPI()

# تحميل الموديل
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    model = None

# -----------------------
# Home
# -----------------------
@app.get("/")
def home():
    return {"message": "Sign Language API Running"}

# -----------------------
# Predict API
# -----------------------
@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)

    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    prediction = "A"

    return {
        "letter": prediction,
        "confidence": 0.95
    }

# -----------------------
# Register
# -----------------------
@app.post("/register")
def register(username: str, email: str, password: str):

    query = "INSERT INTO users (username,email,password) VALUES (%s,%s,%s)"
    cursor.execute(query,(username,email,password))
    db.commit()

    return {"message":"User Registered"}

# -----------------------
# Login
# -----------------------
@app.post("/login")
def login(email: str, password: str):

    query = "SELECT * FROM users WHERE email=%s AND password=%s"
    cursor.execute(query,(email,password))

    user = cursor.fetchone()

    if user:
        return {"message":"Login Successful"}
    else:
        return {"message":"Invalid Email or Password"}

# -----------------------
# Save Word
# -----------------------
@app.post("/save-word")
def save_word(word: str, user_id: int):

    query = "INSERT INTO predictions (user_id,predicted_letter,confidence) VALUES (%s,%s,%s)"
    cursor.execute(query,(user_id,word,0.95))
    db.commit()

    return {"status":"saved"}

# -----------------------
# History
# -----------------------
@app.get("/history/{user_id}")
def history(user_id:int):

    query = "SELECT predicted_letter FROM predictions WHERE user_id=%s"
    cursor.execute(query,(user_id,))

    data = cursor.fetchall()

    return {"history":data}