import os
from pathlib import Path
import py7zr


def create_acs_archive(source_folder, output_name="compressed.acs"):
    filemap_path = "filemap.txt"
    filecntt_path = "filecntt.txt"

    # Step 1: Generate filemap and filecntt
    with open(filemap_path, "w") as fmap, open(filecntt_path, "w") as fcntt:
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, source_folder)

                fmap.write(f"{rel_path}\n")

                with open(full_path, "r", errors="ignore") as f:
                    content = f.read()
                    fcntt.write(f"--- {rel_path} ---\n{content}\n\n")

    # Step 2: Create .7z archive and rename to .acs
    with py7zr.SevenZipFile("temp.7z", 'w') as archive:
        archive.write(filemap_path)
        archive.write(filecntt_path)

    os.rename("temp.7z", output_name)

    # Step 3: Clean up
    os.remove(filemap_path)
    os.remove(filecntt_path)

    print(f"ACS archive created with 7z compression: {output_name}")


                    
class Decompressor:
    def restore(self, filecnttpath, filemappath, outputpath):
        output_dir = Path(outputpath)
        output_dir.mkdir(parents=True, exist_ok=True)

        path_stack = [output_dir]

    # Step 1: Rebuild folder structure
        with open(filemappath, 'r', encoding='utf-8') as f:
            for line in f:
                depth = len(line) - len(line.lstrip(" "))
                name = line.strip()

                if not name:  # skip empty lines
                    continue

                if name.endswith("/"):  # folder
                    # trim stack to current depth
                    path_stack = path_stack[:depth // 4 + 1]
                    new_dir = path_stack[-1] / name.strip("/")
                    new_dir.mkdir(parents=True, exist_ok=True)
                    path_stack.append(new_dir)
                else:  # file
                    # Just record structure now — file contents come later
                    pass

        # Step 2: Restore file contents from .filecntt
        current_file = None
        buffer = []
        with open(filecnttpath, 'r', encoding='utf-8') as f:
            for raw_line in f:
                line = raw_line.rstrip("\n")
                if line.startswith("[") and line.endswith("]"):
                    if current_file:
                        with open(current_file, 'w', encoding='utf-8') as out_file:
                            out_file.write("\n".join(buffer))
                        buffer.clear()
                    rel_name = line[1:-1]
                    file_path = output_dir / rel_name
                    file_path.parent.mkdir(parents=True, exist_ok=True)
                    current_file = file_path
                else:
                    buffer.append(line)
            if current_file:
                with open(current_file, 'w', encoding='utf-8') as out_file:
                    out_file.write("\n".join(buffer))
