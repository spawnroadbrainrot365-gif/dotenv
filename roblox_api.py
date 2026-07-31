import requests
import json
import time
import os
from config import get_roblox_cookie

ROBLOX_API_BASE = "https://publish.roblox.com/v1/assets"

def get_csrf_token(cookie):
    """يسترجع رمز CSRF الضروري للعمليات الأمنية في روبلوكس."""
    headers = {"Cookie": f".ROBLOSECURITY={cookie}"}
    try:
        # محاولة تسجيل خروج وهمية للحصول على الرمز من الرأس 403
        response = requests.post("https://auth.roblox.com/v2/logout", headers=headers)
        if response.status_code == 403 and "X-CSRF-TOKEN" in response.headers:
            return response.headers["X-CSRF-TOKEN"]
        return None
    except Exception as e:
        print(f"Error fetching CSRF: {e}")
        return None

def upload_asset(cookie, file_path, asset_type, name, description):
    """يرفع الملف إلى روبلوكس باستخدام الـ API الرسمي."""
    token = get_csrf_token(cookie)
    if not token:
        return False, "فشل في الحصول على رمز الأمان (CSRF Token)."

    headers = {
        "Cookie": f".ROBLOSECURITY={cookie}",
        "X-CSRF-TOKEN": token
    }

    payload = {
        "assetType": asset_type,
        "name": name,
        "description": description
    }

    try:
        with open(file_path, "rb") as f:
            files = {
                "request": (None, json.dumps(payload), "application/json"),
                "fileContent": (os.path.basename(file_path), f, "application/octet-stream")
            }
            response = requests.post(ROBLOX_API_BASE, headers=headers, files=files)
            
            if response.status_code == 200:
                return True, response.json()
            else:
                return False, f"خطأ {response.status_code}: {response.text}"
    except Exception as e:
        return False, str(e)
