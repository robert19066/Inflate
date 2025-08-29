from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()  # 👈 This loads your .env file


# Load credentials
url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_KEY")

# Connect to Supabase
supabase = create_client(url, key)
bucket = supabase.storage.from_("files")

# Upload a dummy file
with open("dummy.txt", "w") as f:
    f.write("This is a test file to trigger Supabase storage.")

response = bucket.upload("dummy.txt", "dummy.txt")

print("Upload response:", response)
