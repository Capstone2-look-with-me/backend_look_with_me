import face_recognition
import numpy as np

class ContactInfo:
    def __init__(self, id, contact_id, name, avatar_encoding):
        self.id = id                      # Contact record ID
        self.contact_id = contact_id      # ID of the contact person
        self.name = name                  # Contact name
        self.avatar_encoding = avatar_encoding  # Pre-computed face encoding

class FaceRecognitionService:
    def __init__(self):
        # Dictionary mapping user_id to list of ContactInfo objects
        self.contacts = {}  

    async def load_contacts(self, user_id, contacts_data):
        """Load contacts for a specific user using pre-computed encodings"""
        self.contacts[user_id] = []
        
        for contact in contacts_data:
            try:
                contact_id = contact.get("_id") or contact.get("id")
                user_id_contact = contact.get("userId") or contact.get("user_id")
                name = contact.get("name")
                avatar_encoding = contact.get("avatarEncoding")
                
                if all([contact_id, user_id_contact, name, avatar_encoding]):
                    # Use the provided face encoding directly
                    encoding = np.array(avatar_encoding[0] if isinstance(avatar_encoding[0], list) else avatar_encoding)
                    
                    contact_info = ContactInfo(
                        id=contact_id,
                        contact_id=user_id_contact,
                        name=name,
                        avatar_encoding=encoding
                    )
                    self.contacts[user_id].append(contact_info)
                        
            except Exception as e:
                print(f"Error processing contact {contact.get('name', 'Unknown')}: {str(e)}")
                
        return len(self.contacts[user_id])

    async def recognize_face(self, user_id, image_encoding):
        """Recognize a face using the provided encoding"""
        if user_id not in self.contacts:
            return None, "Người lạ"  # Unknown person
            
        try:
            # Ensure image_encoding is in the right format
            if isinstance(image_encoding[0], list):
                image_encoding = np.array(image_encoding[0])  # Take the first face if multiple
            else:
                image_encoding = np.array(image_encoding)
            
            # Compare with known faces
            for contact in self.contacts[user_id]:
                # Compare faces with tolerance (lower is stricter)
                match = face_recognition.compare_faces(
                    [contact.avatar_encoding], image_encoding, tolerance=0.6
                )[0]
                
                if match:
                    return contact.contact_id, contact.name
                    
            return None, "Người lạ"  # No matches found
            
        except Exception as e:
            print(f"Error recognizing face: {str(e)}")
            return None, "Người lạ"
