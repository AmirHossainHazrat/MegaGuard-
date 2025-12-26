import subprocess
import time
import psutil
import os
import sys

def start_mega_guard():
    # پیدا کردن مسیر دقیق فایل اصلی
    main_script = os.path.join(os.path.dirname(__file__), "main.py")
    python_exe = sys.executable
    
    print("🚀 پایشگر مگاگارد فعال شد...")
    
    while True:
        is_running = False
        # جستجو در پروسس‌ها برای پیدا کردن main.py
        for proc in psutil.process_iter(['cmdline']):
            try:
                cmd = proc.info.get('cmdline')
                if cmd and any("main.py" in s for s in cmd):
                    is_running = True
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        if not is_running:
            print("🚨 مگاگارد متوقف شده! در حال اجرای مجدد...")
            # اجرا در یک پنجره جدید یا به صورت پس‌زمینه
            subprocess.Popen([python_exe, main_script], creationflags=subprocess.CREATE_NEW_CONSOLE)
            
        time.sleep(3) # هر ۳ ثانیه چک کن

if __name__ == "__main__":
    start_mega_guard()