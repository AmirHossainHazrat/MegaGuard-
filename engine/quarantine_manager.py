import os
import shutil
from datetime import datetime

QUARANTINE_DIR = "quarantine"

if not os.path.exists(QUARANTINE_DIR):
    os.makedirs(QUARANTINE_DIR)

def move_to_quarantine(file_path):
    try:
        file_name = os.path.basename(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # اسم جدید برای جلوگیری از تداخل و اجرا نشدن
        safe_name = f"{timestamp}_{file_name}.locked"
        dest_path = os.path.join(QUARANTINE_DIR, safe_name)
        
        # جابجایی فایل (به جای کپی، که سریع‌تره)
        shutil.move(file_path, dest_path)
        
        # ذخیره متادیتا (که بعدا بدونیم فایل اصلی کجا بوده)
        with open(f"{dest_path}.info", "w") as f:
            f.write(file_path)
            
        return True, dest_path
    except Exception as e:
        return False, str(e)