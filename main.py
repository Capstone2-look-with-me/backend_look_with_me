from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from socketio.asgi import ASGIApp
from socket_manager import sio
import face_recognition
import numpy as np
from PIL import Image
from io import BytesIO

app = FastAPI(title="Look With Me API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO integration
socket_app = ASGIApp(sio)
app.mount("/socket.io", socket_app)


# Helper function to create ApiResponse
def api_response(status_code: int, message: str, data=None, error=None):
    return {
        "statusCode": status_code,
        "message": message,
        "error": error,
        "data": data,
    }


@app.get("/")
async def root():
    return api_response(200, "Welcome to Look With Me Face Recognition API", {"info": "Root endpoint"})


@app.get("/hello/{name}")
async def say_hello(name: str):
    return api_response(200, f"Hello {name}", {"greeting": f"Hello {name}"})


@app.get("/health")
async def health_check():
    return api_response(200, "Healthy", {"status": "healthy"})


@app.post("/face_encodings")
async def extract_face_encodings(file: UploadFile = File(...)):
    """
    Extract face encodings from an uploaded image.
    """
    try:
        # Read image file
        contents = await file.read()
        image = Image.open(BytesIO(contents))

        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert to numpy array
        image_np = np.array(image)

        # Find face locations and encodings
        face_locations = face_recognition.face_locations(image_np)
        face_encodings = face_recognition.face_encodings(image_np, face_locations)

        # Convert numpy arrays to lists for JSON serialization
        encodings_list = [encoding.tolist() for encoding in face_encodings]

        return api_response(200, "Face encodings extracted successfully", {
            "face_count": len(face_encodings),
            "encodings": encodings_list,
            "locations": [
                {"top": top, "right": right, "bottom": bottom, "left": left}
                for top, right, bottom, left in face_locations
            ]
        })

    except Exception as e:
        return api_response(500, "Failed to extract face encodings", error=str(e))


if __name__ == '__main__':
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
