from copy_files import copy_static_to_public
from generation import generate_pages_recursive


def main():
    copy_static_to_public()
    generate_pages_recursive(
        dir_path_content="content",
        template_path="template.html",
        dest_dir_path="public",
    )


if __name__ == "__main__":
    main()
