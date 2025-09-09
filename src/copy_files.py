import os
import shutil


def copy_directory_recursive(source_path, dest_path):
    """
    Recursively copies the contents of a source directory to a destination directory.
    """
    if not os.path.exists(source_path):
        raise Exception(f"Source directory not found: {source_path}")

    # Get all items in the current source directory
    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        dest_item_path = os.path.join(dest_path, item)

        # Check if the item is a file or a directory
        if os.path.isfile(source_item_path):
            print(f"Copying file: {source_item_path} -> {dest_item_path}")
            shutil.copy(source_item_path, dest_item_path)
        else:  # It's a directory
            # Create the corresponding directory in the destination
            os.mkdir(dest_item_path)
            # Make the recursive call for the subdirectory
            copy_directory_recursive(source_item_path, dest_item_path)


def copy_static_to_public():
    """
    Manages the full process of copying the static directory to public.
    """
    source_dir = "static"
    dest_dir = "public"

    # 1. Clean the public directory if it exists
    if os.path.exists(dest_dir):
        print(f"Deleting directory: {dest_dir}")
        shutil.rmtree(dest_dir)

    # 2. Recreate the public directory
    print(f"Creating directory: {dest_dir}")
    os.mkdir(dest_dir)

    # 3. Start the recursive copy from static to public
    print(f"Copying static files from '{source_dir}' to '{dest_dir}'")
    copy_directory_recursive(source_dir, dest_dir)
