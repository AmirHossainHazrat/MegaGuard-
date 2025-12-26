import customtkinter as ctk
import threading
import time
import os
from engine.behavior_ai import CrackAnalyzer
from guard.watcher import start_guard
from utils.database_manager import is_whitelisted, add_to_whitelist

class MegaGuardApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MegaGuard AI - v1.0")
        self.geometry("1100x700")
        self.configure(fg_color="#0f0f0f")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=220, corner_radius=0, fg_color="#171717")
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="🛡️ MG-PRO", font=("Orbitron", 24, "bold"), text_color="#3a86ff").pack(pady=40)

        self.create_menu_btn("اسکن فایل", self.manual_scan)
        self.create_menu_btn("اسکن حافظه", self.run_memory_scan)
        self.create_menu_btn("امنیت بوت", self.scan_boot)
        
        # --- Main Content ---
        self.content = ctk.CTkFrame(self, fg_color="transparent")
        self.content.grid(row=0, column=1, padx=30, pady=30, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)

        self.status_card = ctk.CTkFrame(self.content, height=120, corner_radius=15, fg_color="#1a1a1a")
        self.status_card.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.status_text = ctk.CTkLabel(self.status_card, text="سیستم در وضعیت امن قرار دارد", font=("Vazir", 20, "bold"), text_color="#4cc9f0")
        self.status_text.pack(pady=20)
        
        self.progress = ctk.CTkProgressBar(self.status_card, width=600, height=8, progress_color="#3a86ff")
        self.progress.set(0)
        self.progress.pack(pady=10)

        self.log_view = ctk.CTkTextbox(self.content, font=("Consolas", 13), fg_color="#0a0a0a", text_color="#d1d1d1")
        self.log_view.grid(row=1, column=0, sticky="nsew", pady=10)
        self.content.grid_rowconfigure(1, weight=1)

        self.trust_btn = None

        # Start Watcher
        try:
            download_path = os.path.join(os.path.expanduser("~"), "Downloads")
            self.observer = start_guard(download_path, self.auto_scan_callback)
            self.add_log(f"Guard Active on: {download_path}")
        except Exception as e:
            self.add_log(f"Guard Error: {e}")

    def create_menu_btn(self, text, command):
        btn = ctk.CTkButton(self.sidebar, text=text, command=command, height=45, fg_color="transparent", 
                            anchor="w", hover_color="#2b2b2b", font=("Vazir", 14))
        btn.pack(pady=5, padx=15, fill="x")

    def add_log(self, message):
        self.log_view.insert("end", f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_view.see("end")

    def manual_scan(self):
        import tkinter.filedialog as fd
        file_path = fd.askopenfilename()
        if file_path:
            threading.Thread(target=self.run_analysis, args=(file_path,)).start()

    def auto_scan_callback(self, file_path):
        self.add_log(f"🔔 واچ‌داگ: فایل جدید/تغییر یافته: {os.path.basename(file_path)}")
        self.run_analysis(file_path)
    
    def run_network_scan(self):
        from engine.network_monitor import get_network_connections
        self.add_log("🌐 در حال پایش اتصالات شبکه...")
        conns = get_network_connections()
        if not conns:
            self.add_log("✅ هیچ اتصال مشکوکی پیدا نشد.")
        else:
            for c in conns:
                # اگر پروسس ناشناس بود یا به پورت عجیبی وصل بود هشدار بده
                self.add_log(f"📡 اتصال فعال: {c['name']} (PID: {c['pid']}) -> {c['remote_ip']}:{c['remote_port']}")
                # اینجا می‌توانیم چک کنیم اگر IP مال ایران یا کشورهای امن نیست، قرمز نشان دهیم

    def run_analysis(self, file_path):
        self.progress.set(0.4)
        if is_whitelisted(file_path):
            self.add_log(f"⚪ تایید شده: {os.path.basename(file_path)}")
            self.status_text.configure(text="فایل مورد اعتماد است", text_color="#00ff00")
            self.progress.set(1.0)
            return

        analyzer = CrackAnalyzer(file_path)
        result, message = analyzer.analyze()
        self.progress.set(1.0)

        if result == "SAFE":
            self.status_text.configure(text="فایل سالم تشخیص داده شد ✅", text_color="#00ff00")
        elif result == "SUSPICIOUS":
            self.status_text.configure(text="هشدار: فایل مشکوک است! ⚠️", text_color="#ffcc00")
            self.show_trust_button(file_path)
        else:
            self.status_text.configure(text="خطر شناسایی و دفع شد! 🚨", text_color="#ff4444")
            
        self.add_log(f"نتیجه: {message}")

    def show_trust_button(self, file_path):
        if self.trust_btn: self.trust_btn.destroy()
        self.trust_btn = ctk.CTkButton(self.content, text="اعتماد به این فایل (Whitelist)", 
                                       fg_color="#2eb82e", command=lambda: self.trust_file(file_path))
        self.trust_btn.grid(row=2, column=0, pady=10)

    def trust_file(self, file_path):
        if add_to_whitelist(file_path):
            self.add_log("✅ فایل به لیست سفید اضافه شد.")
            self.trust_btn.destroy()
            self.status_text.configure(text="فایل تایید شد", text_color="#00ff00")

    def run_memory_scan(self):
        from engine.memory_scanner import MemoryScanner
        self.add_log("🔍 اسکن حافظه زنده...")
        def task():
            scanner = MemoryScanner()
            results = scanner.scan_now()
            if not results: self.add_log("✅ حافظه پاک است.")
            else:
                for p in results: self.add_log(f"🚨 خطر: {p['name']} (PID: {p['pid']})")
        threading.Thread(target=task).start()

    def scan_boot(self):
        from utils.system_info import check_boot_sector
        s, m = check_boot_sector()
        self.add_log(f"🛡️ بوت‌سکتور: {m}")

if __name__ == "__main__":
    app = MegaGuardApp()
    app.mainloop()