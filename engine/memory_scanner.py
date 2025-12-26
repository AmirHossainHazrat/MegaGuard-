import psutil
import os
from engine.behavior_ai import CrackAnalyzer

class MemoryScanner:
    def __init__(self):
        # لیست کلماتی که اگر در مسیر فایل باشند اسکن نمی‌کنیم (برای سرعت بیشتر)
        self.whitelist_paths = ["C:\\Windows\\System32", "C:\\Windows\\SysWOW64"]
    
    def kill_process(self, pid):
        try:
            proc = psutil.Process(pid)
            proc.terminate() # یا proc.kill() برای قطع فوری
            return True
        except:
            return False

    def scan_now(self):
        suspicious_list = []
        
        for proc in psutil.process_iter(['pid', 'name', 'exe']):
            try:
                exe_path = proc.info['exe']
                if not exe_path: continue
                
                # بهینه‌سازی: فایل‌های سیستمی ویندوز رو اسکن نکن
                if any(wp in exe_path for wp in self.whitelist_paths):
                    continue
                
                # تحلیل فایل اجرایی پروسس
                analyzer = CrackAnalyzer(exe_path)
                result, message = analyzer.analyze()
                SYSTEM_EXEMPT = ["Registry", "MemCompression", "System", "Idle", "csrss.exe", "lsass.exe"]
                if proc.info['name'] in SYSTEM_EXEMPT:
                    continue
                if result != "SAFE":
                    suspicious_list.append({
                        "name": proc.info['name'],
                        "pid": proc.info['pid'],
                        "path": exe_path,
                        "risk": result,
                        "msg": message
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue
        
        return suspicious_list