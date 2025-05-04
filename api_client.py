import requests
from config import API_URL

class APIClient:
    def __init__(self):
        self.base_url = API_URL

    def get_all_contacts_by_user_id(self, user_id, access_token):
        """
        Fetch all contacts for a specific user from the external API
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(f"{self.base_url}/contacts/{user_id}", headers=headers)
        response.raise_for_status()  # Raise exception for non-200 responses
        return response.json()
