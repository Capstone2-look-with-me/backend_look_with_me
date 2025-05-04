import socketio
from face_recognition_service import FaceRecognitionService
from api_client import APIClient

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
face_service = FaceRecognitionService()
api_client = APIClient()

@sio.event
async def connect(sid, environ, auth):
    print(f"Client connected: {sid}")

@sio.event
async def disconnect(sid):
    print(f"Client disconnected: {sid}")

@sio.event
async def initialize(sid, data):
    """
    Initialize user context with contacts for face recognition
    """
    try:
        user_id = data.get('userId')
        access_token = data.get('access_token')
        
        if not user_id or not access_token:
            await sio.emit('error', {'message': 'userId and access_token are required'}, to=sid)
            return
            
        # Get contacts from API
        contacts = api_client.get_all_contacts_by_user_id(user_id, access_token)
        
        # Load contacts into face recognition service
        contacts_count = await face_service.load_contacts(user_id, contacts)
        
        await sio.emit('initialize_response', {
            'success': True,
            'contacts_loaded': contacts_count
        }, to=sid)
        
    except Exception as e:
        await sio.emit('error', {'message': str(e)}, to=sid)

@sio.event
async def recognize_face(sid, data):
    """
    Process image URL and recognize faces
    """
    try:
        user_id = data.get('userId')
        image_url = data.get('imageUrl')
        image_id = data.get('imageId')
        
        if not all([user_id, image_url, image_id]):
            await sio.emit('error', {'message': 'userId, imageUrl and imageId are required'}, to=sid)
            return
            
        # Perform face recognition
        name = await face_service.recognize_face(user_id, image_url)
        
        # Send result back to client
        await sio.emit('recognition_result', {
            'imageId': image_id,
            'name': name
        }, to=sid)
        
    except Exception as e:
        await sio.emit('error', {'message': str(e)}, to=sid)
