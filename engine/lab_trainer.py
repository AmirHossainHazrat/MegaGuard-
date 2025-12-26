import os
from engine.ml_engine import MalwareBrain
from engine.feature_extractor import PEFeatureExtractor

def deep_train(base_folder):
    brain = MalwareBrain()
    count = 0
    
    print("🚀 در حال جستجوی عمیق در پوشه‌های استخراج شده...")
    
    # پیمایش تمام زیرپوشه‌ها
    for root, dirs, files in os.walk(base_folder):
        for file in files:
            file_path = os.path.join(root, file)
            
            # فایل‌های سیستمی و متنی بیهوده را رد کن
            if file.endswith(('.txt', '.md', '.zip', '.pdf')):
                continue
                
            try:
                # تلاش برای استخراج ویژگی‌های فایلی
                extractor = PEFeatureExtractor(file_path)
                features = extractor.extract()
                
                # اگر هدر MZ (امضای فایل‌های اجرایی) پیدا شد
                # ویژگی ImportCount یا NumberOfSections معمولاً در فایل‌های واقعی غیرصفر هستند
                if features[7] > 0 or features[6] > 0: 
                    brain.learn_and_save(features, label=1)
                    count += 1
                    print(f"💀 کالبدشکافی موفق ویروس: {file}")
            except:
                continue
                
    brain.retrain()
    print(f"🏁 عملیات تمام شد. {count} بدافزار واقعی به هوش مصنوعی مگاگارد آموزش داده شد.")

if __name__ == "__main__":
    path = input("آدرس پوشه اصلی (جایی که ویروس‌ها رو استخراج کردی) رو بده: ")
    deep_train(path)