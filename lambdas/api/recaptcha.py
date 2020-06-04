import requests
import os

# Test key for default
SECRET = os.getenv("RECAPTCHA_SECRET", "6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe")
def verify(response, ip):
    if SECRET == "": return True
    
    try:
        res = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
            "secret": SECRET,
            "response": response,
            "ip": ip
        }).json()
        return res["success"]
    except:
        return False