import os
import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from engine.feature_extractor import PEFeatureExtractor

MODEL_FILE = "models/brain_v2.pkl"
DATA_FILE = "data/scan_history.csv"

class MalwareBrain:
    def __init__(self):
        self.model = None
        # مطمئن شو پوشه‌ها وجود دارن
        os.makedirs("models", exist_ok=True)
        os.makedirs("data", exist_ok=True)
        self.load_brain()
        pass
    def load_brain(self):
        if os.path.exists(MODEL_FILE):
            self.model = joblib.load(MODEL_FILE)
            print("🧠 مغز هوشمند بارگذاری شد.")
        else:
            self.create_initial_model()

    def create_initial_model(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        # عدد 9 رو دقیقا برابر با تعداد ویژگی‌های خروجی extractor بذار
        X_init = np.random.rand(20, 9) 
        y_init = np.array([0, 1] * 10)
        self.model.fit(X_init, y_init)
        joblib.dump(self.model, MODEL_FILE)
        print("✨ مغز خام جدید با 9 ویژگی ساخته شد.")

    def predict(self, file_path):
        extractor = PEFeatureExtractor(file_path)
        features = extractor.extract()
        features_array = np.array(features).reshape(1, -1)
        
        # چک کردن تطابق تعداد ویژگی‌ها با مدل فعلی
        if self.model:
            expected_features = self.model.n_features_in_
            current_features = len(features)
            
            if current_features != expected_features:
                print(f"⚠️ تغییر در ساختار شناسایی! بازآموزی برای تطبیق با {current_features} ویژگی...")
                self.retrain() # خودش رو آپدیت می‌کنه
        
        prediction = self.model.predict(features_array)[0]
        confidence = self.model.predict_proba(features_array)[0]
        return prediction, confidence, features

    def learn_and_save(self, features, label):
        """ذخیره تجربه جدید در دیتابیس و بازآموزی مدل"""
        # ذخیره در CSV
        new_data = pd.DataFrame([features + [label]])
        header = not os.path.exists(DATA_FILE)
        new_data.to_csv(DATA_FILE, mode='a', index=False, header=header)
        
        # بازآموزی مدل (Retrain) با تمام داده‌های موجود
        self.retrain()

    # در فایل ml_engine.py متد retrain را آپدیت کنید:
    def retrain(self):
        import pandas as pd
        import joblib
        from sklearn.ensemble import RandomForestClassifier
        
        DATA_FILE = "data/scan_history.csv"
        MODEL_FILE = "models/brain_v2.pkl"
        
        if os.path.exists(DATA_FILE):
            df = pd.read_csv(DATA_FILE)
            if len(df) > 1:
                X = df.iloc[:, :-1].values
                y = df.iloc[:, -1].values
                self.model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
                self.model.fit(X, y)
                joblib.dump(self.model, MODEL_FILE)
                print(f"🔄 بازآموزی انجام شد. تعداد کل نمونه‌ها: {len(df)}")
                return True
        return False