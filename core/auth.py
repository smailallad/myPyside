class AuthManager:
    def __init__(self):
        self.current_user = None

    def login(self, username, role):
        self.current_user = {
            "username": username,
            "role": role
        }

    def has_role(self, required_roles):
        if not self.current_user:
            return False
        return self.current_user["role"] in required_roles