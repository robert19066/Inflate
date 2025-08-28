import os
from pathlib import Path

class Compressor:
    def create_filemap(self, folder_path, filemap_path):
        folder_path = Path(folder_path)
        with open(filemap_path, 'w', encoding='utf-8') as f:
            for root, dirs, files in os.walk(folder_path):
                rel_root = os.path.relpath(root, folder_path)
                depth = 0 if rel_root == "." else rel_root.count(os.sep) + 1
                indent = "    " * depth
                f.write(f"{indent}{rel_root}/\n")
                for filename in files:
                    f.write(f"{indent}    {filename}\n")


    def create_filecntt(self, folder_path, filecntt_path):
        """Dump all file contents into filecntt_path."""
        folder_path = Path(folder_path)
        with open(filecntt_path, 'w', encoding='utf-8') as f:
            for root, _, files in os.walk(folder_path):
                for filename in files:
                    file_path = Path(root) / filename
                    rel_path = os.path.relpath(file_path, folder_path)
                    f.write(f"[{rel_path}]\n")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as content_file:
                            f.write(content_file.read())
                    except UnicodeDecodeError:
                        f.write("<BINARY FILE>")
                    f.write("\n\n")

                    
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
