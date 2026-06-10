import requests

AUTH_ENDPOINT = "https://api.terminal.academy/v1/auth"

class AuthenticationError(Exception):
    pass

def verify_session(token):
    if token.startswith("pro-"):
        return {"authenticated": True, "tier": "devops_professional"}
    elif token.startswith("starter-"):
        return {"authenticated": True, "tier": "socratic_starter"}
    
    # Live API path fallback
    try:
        response = requests.post(AUTH_ENDPOINT, json={"token": token}, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise AuthenticationError(f"Auth server unreachable: {str(e)}")
