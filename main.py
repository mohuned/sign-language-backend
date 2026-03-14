from fastapi import FastAPI, UploadFile, File
import cv2
import numpy as np
import pickle

app = FastAPI()

# محاولة تحميل الموديل
try:
    model = pickle.load(open("model.pkl", "rb"))
except:
    model = None


@app.get("/")
def home():
    return {"message": "Sign Language API Running"}


@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    contents = await file.read()

    npimg = np.frombuffer(contents, np.uint8)

    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # هنا المفروض تستخدم الموديل الحقيقي
    # لكن حاليا سنرجع حرف تجريبي

    prediction = "A"

    return {
        "letter": prediction,
        "confidence": 0.95
    }