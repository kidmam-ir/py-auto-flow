import os
import time
import requests

class AutoFlow:
    def __init__(self, target_url, output_dir="downloads"):
        self.target_url = target_url
        self.output_dir = output_dir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def check_health(self):
        """Perform pre-flight health check on the targeted endpoint."""
        print(f"[INFO] Running system health check for upstream endpoint...")
        try:
            response = requests.head(self.target_url, timeout=5)
            print(f"[SUCCESS] Upstream connection verified. Status: {response.status_code}")
            return True
        except Exception as e:
            print(f"[WARNING] Health check failed or timeout reached: {str(e)}")
            return False

    def fetch_data(self):
        print(f"[INFO] Initializing worker workflow for: {self.target_url}")
        if not self.check_health():
            print("[ABORT] Canceling fetch operation due to unstable environment.")
            return False
            
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
    # Test workflow locally with health checks
    worker = AutoFlow("https://github.com")
    worker.fetch_data()
