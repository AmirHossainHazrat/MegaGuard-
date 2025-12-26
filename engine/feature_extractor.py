import pefile
import math
import os

class PEFeatureExtractor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.features = {}

    def calculate_entropy(self, data):
        """محاسبه آنتروپی برای تشخیص فایل‌های پک شده یا رمزگذاری شده"""
        if not data:
            return 0
        entropy = 0
        for x in range(256):
            p_x = float(data.count(x)) / len(data)
            if p_x > 0:
                entropy += - p_x * math.log(p_x, 2)
        return entropy

    def extract(self):
        try:
            pe = pefile.PE(self.file_path, fast_load=True)
            
            # 1. ویژگی‌های پایه
            self.features['Machine'] = pe.FILE_HEADER.Machine
            self.features['SizeOfOptionalHeader'] = pe.FILE_HEADER.SizeOfOptionalHeader
            self.features['Characteristics'] = pe.FILE_HEADER.Characteristics
            self.features['MajorLinkerVersion'] = pe.OPTIONAL_HEADER.MajorLinkerVersion
            self.features['SizeOfCode'] = pe.OPTIONAL_HEADER.SizeOfCode
            self.features['SizeOfImage'] = pe.OPTIONAL_HEADER.SizeOfImage
            
            # 2. محاسبه آنتروپی (ویروس‌ها معمولاً آنتروپی بالایی دارند)
            with open(self.file_path, 'rb') as f:
                data = f.read()
                self.features['Entropy'] = self.calculate_entropy(data)

            # 3. تعداد بخش‌ها (Sections)
            self.features['NumberOfSections'] = pe.FILE_HEADER.NumberOfSections

            # 4. بررسی ایمپورت‌ها (تعداد توابع صدا زده شده)
            pe.parse_data_directories(directories=[pefile.DIRECTORY_ENTRY['IMAGE_DIRECTORY_ENTRY_IMPORT']])
            import_count = 0
            if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
                for entry in pe.DIRECTORY_ENTRY_IMPORT:
                    import_count += len(entry.imports)
            self.features['ImportCount'] = import_count
            pe.close()
            return features
            return list(self.features.values())  # برگرداندن لیست اعداد برای هوش مصنوعی
            
        except Exception as e:
            # در صورت خطا، یک لیست صفر برمی‌گردانیم
            return [0]*9
        finally:
        # بستن اجباری فایل حتی اگر ارور رخ دهد
            if pe:
                pe.close()