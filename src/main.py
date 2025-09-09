# In main.py
import sys

from copy_files import copy_static_to_docs
from generation import generate_pages_recursive


def main():
    # Default base URL for local testing
    base_url = "/"
    # Check for command-line argument for production builds
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    # Use the updated functions and paths
    copy_static_to_docs()
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="docs",
        base_url=base_url,
    )


if __name__ == "__main__":
    main()
