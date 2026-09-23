import os
import time
import requests

class AutoFlow:
    def __init__(self, target_url, output_dir="downloads"):
        self.target_url = target_url
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def fetch_data(self):
        print(f"[INFO] Initializing worker workflow for: {self.target_url}")
        try:
            response = requests.get(self.target_url, timeout=10)
            if response.status_code == 200:
                filename = f"data_{int(time.time())}.txt"
                filepath = os.path.join(self.output_dir, filename)
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text[:1000]) # Save preview
                print(f"[SUCCESS] Automation sync complete. Saved to {filepath}")
                return True
            print(f"[ERROR] Sync failed with status code: {response.status_code}")
        except Exception as e:
            print(f"[CRITICAL] Operational failure: {str(e)}")
        return False

if __name__ == "__main__":
    # Test workflow locally
    worker = AutoFlow("https://github.com")
    worker.fetch_data()
