import yara
import os

class YaraScanner:
    def __init__(self):
        # تعریف قوانین یارا (الگوهای مشترک بدافزارها)
        self.rules_source = """
        rule Ransomware_Behavior {
            strings:
                $s1 = "crypt" nocase
                $s2 = "encrypt" nocase
                $s3 = "decrypt" nocase
                $s4 = ".locked"
            condition:
                2 of them
        }
        rule Anti_Analysis {
            strings:
                $a1 = "IsDebuggerPresent"
                $a2 = "CheckRemoteDebuggerPresent"
            condition:
                all of them
        }
        """
        self.rules = yara.compile(source=self.rules_source)

    def scan_file(self, file_path):
        try:
            matches = self.rules.match(file_path)
            if matches:
                return True, [str(m) for m in matches]
            return False, []
        except:
            return False, []