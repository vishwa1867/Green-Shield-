import uvicorn
import numpy as np
import tensorflow as tf
from fastapi import FastAPI, UploadFile, File
from io import BytesIO
from PIL import Image
import os

app = FastAPI()

# Define the absolute path of the model directory
model_path = "../saved_models/3"

# Verify if the model path exists
print(os.path.exists(model_path))
print(os.listdir(model_path))

CLASS_NAMES = ["Early Blight", "Late Blight", "Healthy"]


@app.get("/ping")
async def ping():
    return {"message": "Hello, I am Live"}


def read_file_as_image(file: bytes) -> np.ndarray:
    image = Image.open(BytesIO(file))
    image = image.resize((256, 256))  # Resize image to the expected input shape
    image = np.array(image)
    return image


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    try:
        # Load the TensorFlow SavedModel as an inference-only layer
        loaded_layer = tf.keras.layers.TFSMLayer(model_path, call_endpoint='serving_default')

        # Wrap the TFSMLayer within a Keras Model
        input_shape = (256, 256, 3)  # Adjust input shape according to the model's expected input shape
        inputs = tf.keras.Input(shape=input_shape)
        outputs = loaded_layer(inputs)
        MODEL = tf.keras.Model(inputs, outputs)

        # Read the uploaded file
        image_array = read_file_as_image(await file.read())

        # Preprocess the image
        img_batch = np.expand_dims(image_array, axis=0)

        # Perform the prediction
        predictions = MODEL(img_batch, training=False)

        # Debugging: Print predictions to understand its structure
        print("Predictions:", predictions)

        # Assuming the dictionary contains a single named output
        # Adjust the key to match your model's output name
        output_name = 'output_0'  # Change this to the correct output name
        if output_name in predictions:
            predictions = predictions[output_name]
        else:
            raise ValueError(f"Expected output key '{output_name}' not found in predictions.")

        # Validate and convert predictions output to numpy array
        if tf.is_tensor(predictions):
            predictions = predictions.numpy()

        # Ensure predictions have the expected shape
        if predictions.ndim == 2 and predictions.shape[1] == len(CLASS_NAMES):
            confidence = 100 * np.max(predictions)
            predicted_class_idx = np.argmax(predictions)
            predicted_class = CLASS_NAMES[predicted_class_idx]
        else:
            raise ValueError(f"Unexpected predictions shape: {predictions.shape}")

        # Return the prediction results
        return {
            "predicted_class": predicted_class,
            "confidence": float(confidence) # Format as a string with 2 decimal places and "%" suffix
        }

    except Exception as e:
        print(f"Prediction error: {e}")
        return {"error": str(e)}


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=5500)