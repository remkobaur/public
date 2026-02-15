# Standalone script to copy folder structure and files while ignoring specific extensions.
# Usage:
#     python update_Unity_folder.py <source_dir> <destination_dir> <ext1> [<ext2> ...]
# Example (ignore .cs and .meta):
#     python update_Unity_folder.py C:/src C:/dst .cs .meta
import os
import sys
import shutil

def copy_structure_with_extensions(src, dst, extensions, skip_folders=None):
	src = os.path.abspath(src)
	dst = os.path.abspath(dst)
	if skip_folders is None:
		skip_folders = []
	skip_folders = [os.path.normpath(f) for f in skip_folders]
	ignored_exts = [ext.lower() for ext in extensions]
	non_meta_ignored_exts = [ext for ext in ignored_exts if ext != '.meta']
	for root, dirs, files in os.walk(src):
		# Remove directories to skip from traversal
		dirs[:] = [d for d in dirs if os.path.relpath(os.path.join(root, d), src) not in skip_folders and d not in skip_folders]

		# Find files in this folder that do NOT match the ignored extensions (excluding .meta for now)
		matching_files = [
			file for file in files
			if not file.lower().endswith('.meta') and not any(file.lower().endswith(ext) for ext in non_meta_ignored_exts)
		]

		# Prepare set of base names for .cs files that are not ignored
		cs_basenames = set(
			os.path.splitext(file)[0]
			for file in files
			if file.lower().endswith('.cs') and not any(file.lower().endswith(ext) for ext in non_meta_ignored_exts)
		)

		# Determine which subfolders would be created (i.e., contain matching files)
		subfolders_to_create = set()
		for d in dirs:
			subfolder_path = os.path.join(root, d)
			subfolder_files = []
			try:
				subfolder_files = os.listdir(subfolder_path)
			except Exception:
				pass
			if any(
				not f.lower().endswith('.meta') and not any(f.lower().endswith(ext) for ext in non_meta_ignored_exts)
				for f in subfolder_files
			):
				subfolders_to_create.add(d)

		# Find .meta files that match .cs files or subfolders that would be created
		meta_files = []
		if '.meta' not in ignored_exts:
			for file in files:
				if file.lower().endswith('.meta'):
					base = os.path.splitext(file)[0]
					if base in cs_basenames or base in subfolders_to_create:
						meta_files.append(file)

		# Only create the folder if there are files to copy
		if matching_files or meta_files:
			rel_path = os.path.relpath(root, src)
			dst_dir = os.path.join(dst, rel_path)
			os.makedirs(dst_dir, exist_ok=True)
			for file in matching_files:
				src_file = os.path.join(root, file)
				dst_file = os.path.join(dst_dir, file)
				shutil.copy2(src_file, dst_file)
			for file in meta_files:
				src_file = os.path.join(root, file)
				dst_file = os.path.join(dst_dir, file)
				shutil.copy2(src_file, dst_file)

def main():
	if len(sys.argv) < 4:
		print("Usage: python update_Unity_folder.py <source_dir> <destination_dir> <ext1> [<ext2> ...]")
		sys.exit(1)
	src = sys.argv[1]
	dst = sys.argv[2]
	extensions = sys.argv[3:]
	copy_structure_with_extensions(src, dst, extensions)
	print(f"Copied folder structure from {src} to {dst}. Ignored extensions: {', '.join(extensions)}")

if __name__ == "__main__":
	# main()
	src = r"I:\SW_Projects\Unity\PublicTester\Assets"
	dst = r"D:\Git\Public\Unity\HouseBuilder\Assets"
	extensions = []
	skip_folders = ['TextMesh Pro']  # Example: relative to src
	copy_structure_with_extensions(src, dst, extensions, skip_folders)
	print(f"Copied folder structure from {src} to {dst}. Ignored extensions: {', '.join(extensions)}. Skipped folders: {', '.join(skip_folders)}")
 
	src = r"I:\SW_Projects\Unity\PublicTester\ProjectSettings"
	dst = r"D:\Git\Public\Unity\HouseBuilder\ProjectSettings"
	copy_structure_with_extensions(src, dst, extensions, skip_folders)
