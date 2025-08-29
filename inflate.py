from acsmain import create_acs_archive, Decompressor
import sys


method = sys.argv[2]
if sys.argv[1] == "--method":
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
        print("Sorry but the Cloud Based Abstract Compression method is yet not available.")
else:
    print("Invalid method specified.")