from acsmain import Compressor, Decompressor
import sys

if len(sys.argv) >= 3 and sys.argv[1] == "--compress":
    folder_path = sys.argv[2]
    try:
        comp = Compressor()
        print("Creating filemap...")
        comp.create_filemap(folder_path, "project.filemap")
        print("Filemap done.")

        print("Creating filecntt...")
        comp.create_filecntt(folder_path, "project.filecntt")
        print("File content dump done.")
    except Exception as e:
        print(f"An error occurred: {e}")

elif len(sys.argv) >= 5 and sys.argv[1] == "--decompress":
    filemap_path = sys.argv[2]
    filecntt_path = sys.argv[3]
    output_path = sys.argv[4]
    try:
        decomp = Decompressor()
        print("Restoring files...")
        decomp.restore(filecntt_path, filemap_path, output_path)
        print("Restoration done.")
    except Exception as e:
        print(f"An error occurred: {e}")

else:
    print("Usage:")
    print("  python inflate.py --compress <folder_path>")
    print("  python inflate.py --decompress <filemap_path> <filecntt_path> <output_path>")

