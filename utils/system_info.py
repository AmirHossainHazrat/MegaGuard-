import os

def check_boot_sector():
    if os.name != 'nt': # فقط برای ویندوز
        return "Unsupported OS"
    
    try:
        # خوندن اولین ۵۱۲ بایت دیسک فیزیکی شماره ۰
        # نیاز به دسترسی ادمین دارد
        with open(r"\\.\PhysicalDrive0", "rb") as drive:
            mbr_data = drive.read(512)
            
            # چک کردن امضای استاندارد بوت سکتور (دو بایت آخر)
            if mbr_data[-2:].hex() == "55aa":
                return "HEALTHY", "امضای بوت‌سکتور استاندارد و سالم است."
            else:
                return "DANGEROUS", "امضای بوت‌سکتور تغییر کرده! احتمال آلودگی به باج‌افزار."
    except PermissionError:
        return "ADMIN_REQUIRED", "برای بررسی بوت‌سکتور باید برنامه را با Run as Administrator باز کنید."
    except Exception as e:
        return "ERROR", str(e)