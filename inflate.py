from acsmain import create_acs_archive, restore
from dawnbond import DawnbondCloud
import sys
from pathlib import Path

cloud = DawnbondCloud()

USAGE = """
Usage:
  python inflate.py --method acs  --compress   <folder_path>
  python inflate.py --method acs  --decompress <acs_file> [output_path]
  python inflate.py --method cbac --compress   <folder_path>
  python inflate.py --method cbac --decompress <retrieval_code> [output_path]
  python inflate.py --method cbac --purge      <retrieval_code>
"""

def log(msg):
    print(f"[INF] {msg}")

def warn(msg):
    print(f"[WRN] {msg}")

def err(msg):
    print(f"[ERR] {msg}")

if len(sys.argv) < 3:
    warn("Insufficient parameters supplied.")
    print(USAGE)
    sys.exit(1)

method = sys.argv[2].lower()
log(f"Selected compression protocol: {method.upper()}")

if method == "acs":
    if len(sys.argv) >= 4 and sys.argv[3] == "--compress":
        folder_path = sys.argv[4]
        try:
            log(f"Scanning target directory: {folder_path}")
            archive_name = create_acs_archive(folder_path)
            log(f"ACS archive successfully created → {archive_name}")
        except Exception as e:
            err(f"ACS compression failed: {e}")

    elif len(sys.argv) >= 5 and sys.argv[3] == "--decompress":
        acs_file = sys.argv[4]
        output_path = sys.argv[5] if len(sys.argv) >= 6 else "restored_acs"
        try:
            log(f"Loading ACS archive: {acs_file}")
            log(f"Restoration target directory: {output_path}")
            restore(acs_file, output_path)
            log("Restoration complete. All files reconstructed successfully.")
        except Exception as e:
            err(f"ACS decompression failed: {e}")

    else:
        warn("Invalid ACS parameters.")
        print(USAGE)

elif method == "cbac":
    if len(sys.argv) >= 5 and sys.argv[3] == "--compress":
        folder_path = sys.argv[4]
        try:
            log(f"Initiating CBAC compression for: {folder_path}")
            archive_name = create_acs_archive(folder_path)
            log(f"Local CBAC archive created: {archive_name}")
            code = cloud.save_to_cloud(archive_name)
            log(f"Upload complete. Retrieval code: -> {code} <-")
        except Exception as e:
            err(f"CBAC compression failed: {e}")

    elif len(sys.argv) >= 5 and sys.argv[3] == "--decompress":
        code = sys.argv[4]
        output_path = sys.argv[5] if len(sys.argv) >= 6 else "restored_cbac"
        try:
            log(f"Fetching CBAC archive from cloud using code: {code}")
            local_file = cloud.fetch_cloud(code, "compressed.cbac")
            log(f"Archive retrieved: {local_file}")
            restore(local_file, output_path)
            log("CBAC restoration complete.")
        except Exception as e:
            err(f"CBAC decompression failed: {e}")

    elif len(sys.argv) >= 5 and sys.argv[3] == "--purge":
        code = sys.argv[4]
        try:
            log(f"Purging cloud entry with code: {code}")
            cloud.purge_cloud(code)
            log("Purge successful.")
        except Exception as e:
            err(f"CBAC purge failed: {e}")

    else:
        warn("Invalid CBAC parameters.")
        print(USAGE)

else:
    err("Invalid method specified. Use 'acs' or 'cbac'.")
