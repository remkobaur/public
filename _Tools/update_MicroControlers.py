
import sys
from HelperClasses import FileCopier   


if __name__ == "__main__":
	copier = FileCopier()
	src = r"D:\Git\MicroControllers"
	dst = r"D:\Git\Public\MicroControllers"
	extensions = ["secret.h"]
	skip_folders = ["_Tools",".git"]  # Example: relative to src
	copier.copy_structure_with_extensions(src, dst, extensions, skip_folders)
	
