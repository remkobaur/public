
import sys
from HelperClasses import FileCopier   


if __name__ == "__main__":
	copier = FileCopier()
	src = r"D:\Git\MicroControllers"
	dst = r"D:\Git\Public\MicroControllers"
	skip_extensions = ["secret.h"]
	skip_folders = [".git"]  # Example: relative to src
	copier.copy_structure_with_extensions(src, dst, skip_extensions, skip_folders)
	
