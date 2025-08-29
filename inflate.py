from acsmain import create_acs_archive, Decompressor
from dawnbond import DawnbondCloud
import sys

cloud = DawnbondCloud()

if len(sys.argv) < 3:
    print("Usage: python inflate.py --method <acs|cbac> [options]")
    sys.exit(1)

method = sys.argv[2]
print(f"Selected method: {method}")

if method == "acs":
    if len(sys.argv) >= 4 and sys.argv[3] == "--compress":
        folder_path = sys.argv[4]
        try:
            print("Creating ACS archive...")
            create_acs_archive(folder_path)
        except Exception as e:
            print(f"An error occurred: {e}")

    elif len(sys.argv) >= 6 and sys.argv[3] == "--decompress":
        filemap_path = sys.argv[4]
        filecntt_path = sys.argv[5]
        output_path = sys.argv[6]
        try:
            decomp = Decompressor()
            print("Restoring files...")
            decomp.restore(filecntt_path, filemap_path, output_path)
            print("Restoration done.")
        except Exception as e:
            print(f"An error occurred: {e}")

    else:
        print("Usage:")
        print("  python inflate.py --method acs --compress <folder_path>")
        print("  python inflate.py --method acs --decompress <filemap_path> <filecntt_path> <output_path>")

elif method == "cbac":
    if len(sys.argv) >= 5 and sys.argv[3] == "--compress":
        folder_path = sys.argv[4]
        try:
            print("Step 1: Creating CBAC archive...")
            archive_name = create_acs_archive(folder_path)  # returns archive filename

            code = cloud.save_to_cloud(archive_name)
            print(f"CBAC archive uploaded to public.cbac. Retrieval code: {code}")
        except Exception as e:
            print(f"Error during CBAC compression: {e}")

    elif len(sys.argv) >= 5 and sys.argv[3] == "--decompress":
        code = sys.argv[4]
        output_path = sys.argv[5] if len(sys.argv) >= 6 else "restored_cbac"
        try:
            local_file = cloud.fetch_cloud(code, "compressed.cbac")
            decomp = Decompressor()
            print("Restoring files from CBAC archive...")
            decomp.restore("filecntt.txt", "filemap.txt", output_path)
            print("Restoration complete.")
        except Exception as e:
            print(f"Error during CBAC decompression: {e}")

    elif len(sys.argv) >= 5 and sys.argv[3] == "--purge":
        code = sys.argv[4]
        try:
            cloud.purge_cloud(code)
        except Exception as e:
            print(f"Error during CBAC purge: {e}")

    else:
        print("Usage:")
        print("  python inflate.py --method cbac --compress <folder_path>")
        print("  python inflate.py --method cbac --decompress <retrieval_code> [output_path]")
        print("  python inflate.py --method cbac --purge <retrieval_code>")

else:
    print("Invalid method specified.")
