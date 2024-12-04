import uvicorn
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from io import BytesIO
from PIL import Image
import os

app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # Your frontend on port 5500
        "http://127.0.0.1:5001",  # Your frontend on port 5001
        "http://localhost:5500",  # Allow localhost for testing
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Define the absolute path of the model directory
model_path = "../saved_models/3"

# Verify if the model path exists
print(os.path.exists(model_path))
print(os.listdir(model_path))

# Class names corresponding to plant diseases
CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]

@app.get("/ping")
async def ping():
    return {"message": "Hello, I am Live"}

def read_file_as_image(file: bytes) -> np.ndarray:
    """Converts the uploaded byte file to an image and resizes it."""
    image = Image.open(BytesIO(file))
    image = image.resize((256, 256))  # Resize image to the expected input shape
    image = np.array(image)
    return image

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Load the TensorFlow SavedModel
        model = tf.keras.models.load_model(model_path)

        # Read the uploaded file and process it into a usable image
        image_array = read_file_as_image(await file.read())

        # Preprocess the image
        img_batch = np.expand_dims(image_array, axis=0)  # Add batch dimension

        # Perform the prediction
        predictions = model(img_batch)

        # Convert predictions to numpy array and handle it
        predictions = predictions.numpy() if tf.is_tensor(predictions) else predictions

        # Validate the shape of the predictions
        if predictions.ndim == 2 and predictions.shape[1] == len(CLASS_NAMES):
            confidence = 100 * np.max(predictions)
            predicted_class_idx = np.argmax(predictions)
            predicted_class = CLASS_NAMES[predicted_class_idx]
        else:
            raise ValueError(f"Unexpected predictions shape: {predictions.shape}")

        # Return the prediction results
        return {
            "predicted_class": predicted_class,
            "confidence": float(confidence)  # Return confidence as a percentage
        }

    except Exception as e:
        print(f"Prediction error: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5000)
