import os
from engine.ml_engine import MalwareBrain
from engine.feature_extractor import PEFeatureExtractor

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

if __name__ == "__main__":
    path = input("آدرس پوشه MG_Lab رو وارد کن: ")
    deep_train(path)

    