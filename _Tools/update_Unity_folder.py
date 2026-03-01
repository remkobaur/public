# Standalone script to copy folder structure and files while ignoring specific extensions.
# Usage:
#     python update_Unity_folder.py <source_dir> <destination_dir> <ext1> [<ext2> ...]
# Example (ignore .cs and .meta):
#     python update_Unity_folder.py C:/src C:/dst .cs .meta
import sys
from HelperClasses import FileCopier   


def main():
	if len(sys.argv) < 4:
		print("Usage: python update_Unity_folder.py <source_dir> <destination_dir> <ext1> [<ext2> ...]")
		sys.exit(1)
	src = sys.argv[1]
	dst = sys.argv[2]
	extensions = sys.argv[3:]
	copier = FileCopier()
	copier.copy_structure_with_extensions(src, dst, extensions)


if __name__ == "__main__":
	# main()
	copier = FileCopier()
	src = r"I:\SW_Projects\Unity\PublicTester\Assets"
	dst = r"D:\Git\Public\Unity\HouseBuilder\Assets"
	extensions = []
	skip_folders = ['TextMesh Pro']  # Example: relative to src
	copier.copy_structure_with_extensions(src, dst, extensions, skip_folders)
	
	src = r"I:\SW_Projects\Unity\PublicTester\ProjectSettings"
	dst = r"D:\Git\Public\Unity\HouseBuilder\ProjectSettings"
	copier.copy_structure_with_extensions(src, dst, extensions, skip_folders)
