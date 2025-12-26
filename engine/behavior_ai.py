import pefile
import subprocess
from engine.ml_engine import MalwareBrain

class CrackAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        # مقداردهی اولیه مغز هوش مصنوعی
        self.brain = MalwareBrain()
        
        # تعریف وزن رفتارهای مشکوک (Heuristic Rules)
        self.behavior_weights = {
            "HttpSendRequest": 3,      # ارسال داده به اینترنت
            "URLDownloadToFile": 4,    # دانلود فایل مخفی
            "WriteProcessMemory": 5,   # تزریق کد به پروسس‌های دیگر
            "CreateRemoteThread": 5,   # اجرای کد در حافظه جانبی
            "GetKeyboardState": 6,     # پتانسیل کی‌لاگر
            "RegSetValue": 2,          # تغییر در تنظیمات سیستم
            "ShellExecute": 3,         # اجرای دستورات خط فرمان
            "SetWindowsHookEx": 4      # مانیتور کردن فعالیت‌های کاربر
        }

    def has_valid_signature(self):
        """بررسی امضای دیجیتال برای فیلتر کردن برنامه‌های معتبر شرکت‌ها"""
        try:
            cmd = f'Get-AuthenticodeSignature "{self.file_path}" | Select-Object -ExpandProperty Status'
            result = subprocess.check_output(['powershell', '-Command', cmd], stderr=subprocess.STDOUT, timeout=3).decode().strip()
            return result == "Valid"
        except:
            return False

    def analyze(self):
        # مقداردهی اولیه برای اطمینان از وجود متغیرها
        ai_risk_percent = 0
        ml_prediction = 0
        total_risk_score = 0
        
        try:
            # ۱. بررسی امضا
            if self.has_valid_signature():
                return "SAFE", "دارای امضای دیجیتال معتبر."

            # ۲. بخش هوش مصنوعی (با مدیریت خروجی ۳ تایی)
            try:
                # اینجا حتماً از _ برای دریافت ویژگی‌ها استفاده کن
                ml_prediction, ml_confidence, _ = self.brain.predict(self.file_path)
                
                if len(ml_confidence) > 1:
                    ai_risk_percent = int(ml_confidence[1] * 100)
                else:
                    ai_risk_percent = 100 if ml_prediction == 1 else 0
            except Exception as e:
                print(f"⚠️ AI Error: {e}")
                ml_prediction, ai_risk_percent = 0, 0

            # ۳. تحلیل Heuristic (ساده شده برای تست)
            # ... (کدهای تحلیل PE شما اینجا قرار دارد) ...

            # ۴. منطق تصمیم‌گیری نهایی
            report = f"(AI: {ai_risk_percent}% | Score: {total_risk_score})"
            
            if ml_prediction == 1 and ai_risk_percent > 80:
                return "MALICIOUS", f"🚨 بدافزار قطعی! {report}"
            elif ml_prediction == 1 or total_risk_score > 5:
                return "SUSPICIOUS", f"⚠️ مشکوک. {report}"
            else:
                return "SAFE", f"✅ ایمن. {report}"

        except Exception as e:
            # بسیار مهم: در صورت هرگونه خطا، حتماً دو مقدار برگردان
            print(f"❌ Error in analyze: {e}")
            return "ERROR", f"خطای سیستمی: {str(e)}"

    def learn_from_user(self, is_malicious):
        """متدی برای آپدیت کردن مغز بر اساس بازخورد کاربر"""
        return self.brain.learn(self.file_path, is_malicious)
    # در فایل lab_trainer.py
def deep_train(base_folder, is_malicious=False):
    brain = MalwareBrain()
    label = 1 if is_malicious else 0
    all_files = []

    # پیدا کردن همه فایل‌های معتبر قبل از شروع
    for root, dirs, files in os.walk(base_folder):
        for f in files:
            if not f.endswith(('.txt', '.md', '.zip')):
                all_files.append(os.path.join(root, f))
    
    total = len(all_files)
    print(f"📊 مجموع فایل‌های یافت شده برای آموزش: {total}")

    for i, file_path in enumerate(all_files):
        try:
            extractor = PEFeatureExtractor(file_path)
            features = extractor.extract()
            if any(f != 0 for f in features):
                brain.learn_and_save(features, label)
                
                # نمایش درصد پیشرفت در کنسول
                progress = ((i + 1) / total) * 100
                print(f"[{progress:.1f}%] در حال تحلیل: {os.path.basename(file_path)}", end='\r')
        except:
            continue
            
    brain.retrain()
    print(f"\n✅ آموزش پوشه با موفقیت تمام شد.")