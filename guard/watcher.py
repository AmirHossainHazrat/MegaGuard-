import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DownloadFolderHandler(FileSystemEventHandler):
    def __init__(self, callback_func):
        self.callback_func = callback_func

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".exe"):
            print(f"فایل جدید پیدا شد: {event.src_path}")
            self.callback_func(event.src_path)

def start_guard(path_to_watch, callback):
    event_handler = DownloadFolderHandler(callback)
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    observer.start()
    return observer


def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(".exe"):
            # وقتی فایل تغییر میکنه، یعنی ممکنه ویروس بهش کد تزریق کرده باشه
            print(f"⚠️ تغییر در فایل شناسایی شد: {event.src_path}")
            self.callback_func(event.src_path)