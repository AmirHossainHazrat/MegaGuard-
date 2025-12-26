import hashlib
import json
import os

DB_FILE = "whitelist.json"

def calculate_sha256(file_path):
    """محاسبه هش بهینه برای فایل‌های حجیم (Head-Tail Hashing)"""
    try:
        file_size = os.path.getsize(file_path)
        sha256_hash = hashlib.sha256()
        
        # بهینه‌سازی: اگر فایل کوچک بود، کلش؛ اگر بزرگ بود، فقط تکه‌های حساس
        if file_size < 50 * 1024 * 1024:
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
        else:
            with open(file_path, "rb") as f:
                sha256_hash.update(f.read(1024 * 1024)) # ۱ مگابایت اول
                f.seek(file_size // 2)
                sha256_hash.update(f.read(1024 * 1024)) # ۱ مگابایت وسط
                f.seek(file_size - (1024 * 1024))
                sha256_hash.update(f.read(1024 * 1024)) # ۱ مگابایت آخر
        return sha256_hash.hexdigest()
    except:
        return None

def load_whitelist():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def is_whitelisted(file_path):
    """تابعی که main.py دنبالش می‌گرده"""
    file_hash = calculate_sha256(file_path)
    if not file_hash: return False
    return file_hash in load_whitelist()

def add_to_whitelist(file_path):
    """تابعی که برای اعتماد کردن به فایل استفاده میشه"""
    file_hash = calculate_sha256(file_path)
    if not file_hash: return False
    
    whitelist = load_whitelist()
    if file_hash not in whitelist:
        whitelist.append(file_hash)
        with open(DB_FILE, "w") as f:
            json.dump(whitelist, f)
        return True
    return False