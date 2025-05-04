import face_recognition
import requests
from io import BytesIO
from PIL import Image
import numpy as np

class ContactInfo:
    def __init__(self, user_id, name, face_encoding):
        self.user_id = user_id
        self.name = name
        self.face_encoding = face_encoding

class FaceRecognitionService:
    def __init__(self):
        # Dictionary mapping user_id to list of ContactInfo objects
        self.contacts = {}  

    async def load_contacts(self, user_id, contacts_data):
        """Load contacts for a specific user"""
        self.contacts[user_id] = []
        
        for contact in contacts_data:
            try:
                contact_id = contact["user_id"]
                name = contact["name"]
                avatar_url = contact["avatar"]
                
                # Download the avatar image
                response = requests.get(avatar_url)
                if response.status_code == 200:
                    image = Image.open(BytesIO(response.content))
                    image_np = np.array(image)
                    
                    # Find face encodings
                    face_encodings = face_recognition.face_encodings(image_np)
                    
                    if face_encodings:
                        # Use the first face found in the avatar
                        contact_info = ContactInfo(contact_id, name, face_encodings[0])
                        self.contacts[user_id].append(contact_info)
                        
            except Exception as e:
                print(f"Error processing contact {contact.get('name', 'Unknown')}: {str(e)}")
                
        return len(self.contacts[user_id])

    async def recognize_face(self, user_id, image_url):
        """Recognize a face in the given image URL"""
        if user_id not in self.contacts:
            return "Người lạ"  # Unknown person
            
        try:
            # Download the image
            response = requests.get(image_url)
            if response.status_code != 200:
                return "Người lạ"
                
            image = Image.open(BytesIO(response.content))
            image_np = np.array(image)
            
            # Find face locations and encodings
            face_locations = face_recognition.face_locations(image_np)
            face_encodings = face_recognition.face_encodings(image_np, face_locations)
            
            if not face_encodings:
                return "Người lạ"  # No faces found
                
            # Compare with known faces
            for face_encoding in face_encodings:
                for contact in self.contacts[user_id]:
                    # Compare faces with tolerance (lower is stricter)
                    match = face_recognition.compare_faces(
                        [contact.face_encoding], face_encoding, tolerance=0.6
                    )[0]
                    
                    if match:
                        return contact.name
                        
            return "Người lạ"  # No matches found
            
        except Exception as e:
            print(f"Error recognizing face: {str(e)}")
            return "Người lạ"
