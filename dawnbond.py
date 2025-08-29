import os
import random
import base64
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class DawnbondCloud:
    def __init__(self, url=SUPABASE_URL, key=SUPABASE_KEY):
        self.supabase = create_client(url, key)

    def _generate_code(self):
        while True:
            code = random.randint(10000, 99999)
            resp = self.supabase.table("cbac").select("code").eq("code", code).execute()
            if not resp.data:
                return code

    def save_to_cloud(self, file_path):
        code = self._generate_code()
        filename = os.path.basename(file_path)

        with open(file_path, "rb") as f:
            file_bytes = f.read()

        # Encode to base64 so it can be sent via JSON
        file_b64 = base64.b64encode(file_bytes).decode("utf-8")

        self.supabase.table("cbac").insert({
            "code": code,
            "filename": filename,
            "file": file_b64
        }).execute()

        print(f"File saved to cloud with code: {code}")
        return code

    def fetch_cloud(self, code, save_path=None):
        resp = self.supabase.table("cbac").select("file, filename").eq("code", int(code)).execute()
        if not resp.data:
            raise FileNotFoundError(f"No file found with code {code}")

        file_b64 = resp.data[0]["file"]
        filename = resp.data[0]["filename"]
        file_bytes = base64.b64decode(file_b64)

        save_path = save_path or filename
        with open(save_path, "wb") as f:
            f.write(file_bytes)

        print(f"File downloaded to {save_path}")
        return save_path

    def purge_cloud(self, code):
        resp = self.supabase.table("cbac").delete().eq("code", int(code)).execute()
        if resp.data:
            print(f"File with code {code} purged from cloud.")
            return True
        else:
            print(f"No file found with code {code} to purge.")
            return False
