import math

def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in range(256):
        p_x = float(data.count(x)) / len(data)
        if p_x > 0:
            entropy += - p_x * math.log(p_x, 2)
    return entropy

def get_advanced_features(pe):
    features = {}
    
    # 1. آنتروپی کل فایل
    features['entire_entropy'] = calculate_entropy(pe.__data__)
    
    # 2. بررسی سکشن‌ها
    sections = pe.sections
    features['num_sections'] = len(sections)
    
    # پیدا کردن سکشن با بیشترین آنتروپی (نشانه پکر)
    section_entropies = [calculate_entropy(s.get_data()) for s in sections]
    features['max_section_entropy'] = max(section_entropies) if section_entropies else 0
    
    # 3. شناسایی توابع خطرناک (Suspicious APIs)
    suspicious_apis = ['CreateRemoteThread', 'WriteProcessMemory', 'VirtualAllocEx', 'GetKeyLog']
    api_count = 0
    if hasattr(pe, 'DIRECTORY_ENTRY_IMPORT'):
        for entry in pe.DIRECTORY_ENTRY_IMPORT:
            for imp in entry.imports:
                if imp.name and imp.name.decode() in suspicious_apis:
                    api_count += 1
    features['suspicious_api_count'] = api_count
    
    return features
