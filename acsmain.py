import os
from pathlib import Path
import py7zr
import shutil
import tempfile
from pathlib import Path
import subprocess

import random

def create_acs_archive(source_folder):
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

    # Step 2: Create .7z archive and rename to .acs with random suffix
    random_id = str(random.randint(100000000, 999999999))
    output_name = f"compressed_{random_id}.acs"

    with py7zr.SevenZipFile("temp.7z", 'w') as archive:
        archive.write(filemap_path)
        archive.write(filecntt_path)

    os.rename("temp.7z", output_name)

    # Step 3: Clean up
    os.remove(filemap_path)
    os.remove(filecntt_path)

    print(f"ACS archive created with 7z compression: {output_name}")
    return output_name  # Return the actual filename



                    

def restore(self, acs_path, output_path):
    acs_path = Path(acs_path)
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Extract .acs archive (7z format)
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_dir_path = Path(temp_dir)
        subprocess.run(['7z', 'x', str(acs_path), f'-o{temp_dir}'], check=True)

        filemap_path = temp_dir_path / 'filemap.txt'
        filecntt_path = temp_dir_path / 'filecntt.txt'

        # Step 2: Rebuild folder structure from filemap.txt
        path_stack = [output_dir]
        with open(filemap_path, 'r', encoding='utf-8') as f:
            for line in f:
                depth = len(line) - len(line.lstrip(" "))
                name = line.strip()

                if not name:
                    continue

                if name.endswith("/"):
                    path_stack = path_stack[:depth // 4 + 1]
                    new_dir = path_stack[-1] / name.strip("/")
                    new_dir.mkdir(parents=True, exist_ok=True)
                    path_stack.append(new_dir)

        # Step 3: Restore file contents from filecntt.txt
        current_file = None
        buffer = []
        with open(filecntt_path, 'r', encoding='utf-8') as f:
            for raw_line in f:
                line = raw_line.rstrip("\n")
                if line.startswith("[") and line.endswith("]"):
                    if current_file:
                        with open(current_file, 'w', encoding='utf-8') as out_file:
                            out_file.write("\n".join(buffer))
                        buffer.clear()
                    rel_name = line[1:-1]
                    current_file = output_dir / rel_name
                    current_file.parent.mkdir(parents=True, exist_ok=True)
                else:
                    buffer.append(line)
            if current_file:
                with open(current_file, 'w', encoding='utf-8') as out_file:
                    out_file.write("\n".join(buffer))
