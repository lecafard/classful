import os

ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "https://classful.tomn.me")

def send_response(data):
    return {"data": data}, 200, {"access-control-allow-origin": ALLOWED_ORIGIN}

def send_error(error, code=400):
    return {"error": error},  code, {"access-control-allow-origin": ALLOWED_ORIGIN}