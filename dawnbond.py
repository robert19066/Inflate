import os
import random
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
BUCKET_NAME = "files"  # your storage bucket

class DawnbondCloud:
    def __init__(self, url=SUPABASE_URL, key=SUPABASE_KEY, bucket_name=BUCKET_NAME):
        self.supabase = create_client(url, key)
        self.bucket = self.supabase.storage.from_(bucket_name)

    def _generate_code(self):
        """Generate a unique 5-digit code."""
        while True:
            code = random.randint(10000, 99999)
            # Check if file already exists in bucket
            files = self.bucket.list()
            if not any(f["name"].startswith(f"{code}.acs") for f in files):
                return code

    def save_to_cloud(self, file_path):
        """Upload raw .acs file to Supabase Storage."""
        code = self._generate_code()
        filename = f"{code}.acs"

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        self.bucket.upload(filename, file_bytes, {"content-type": "application/octet-stream"})
        print(f"[INF] File saved to cloud with code: {code}")
        return code

    def fetch_cloud(self, code, save_path=None):
        """Download a .acs file from Supabase Storage."""
        filename = f"{code}.acs"
        save_path = save_path or filename
        data = self.bucket.download(filename)
        if data:
            with open(save_path, "wb") as f:
                f.write(data)
            print(f"[INF] File downloaded to {save_path}")
            return save_path
        else:
            raise FileNotFoundError(f"No file found with code {code}")

    def purge_cloud(self, code):
        """Delete a .acs file from Supabase Storage."""
        filename = f"{code}.acs"
        self.bucket.remove([filename])
        print(f"[INF] File with code {code} purged from cloud.")
