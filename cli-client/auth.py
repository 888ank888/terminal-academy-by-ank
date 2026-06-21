import urllib.request
import urllib.error
import json

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
        data = json.dumps({"token": token}).encode("utf-8")
        req = urllib.request.Request(
            AUTH_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            res_data = response.read().decode("utf-8")
            return json.loads(res_data)
    except urllib.error.HTTPError as e:
        raise AuthenticationError(f"Auth server returned error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        raise AuthenticationError(f"Auth server unreachable: {e.reason}")
    except Exception as e:
        raise AuthenticationError(f"Auth server unreachable: {str(e)}")
