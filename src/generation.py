# In generation.py
import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown):
    """
    Extracts the H1 header from a markdown string.
    """
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            # Strip the '# ' prefix and any surrounding whitespace
            return line[2:].strip()
    raise Exception("No H1 header found in markdown document")


def generate_page(from_path, template_path, dest_path, base_url="/"):  # Add base_url
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    # ... (read markdown and template files) ...
    with open(from_path, "r") as f:
        markdown_content = f.read()
    with open(template_path, "r") as f:
        template_content = f.read()

    html_node = markdown_to_html_node(markdown_content)
    html_content = html_node.to_html()
    title = extract_title(markdown_content)

    final_html = template_content.replace("{{ Title }}", title)
    final_html = final_html.replace("{{ Content }}", html_content)

    # FIX: Replace paths to work with GitHub Pages subdirectory
    final_html = final_html.replace('href="/', f'href="{base_url}')
    final_html = final_html.replace('src="/', f'src="{base_url}')

    # ... (write the final_html to dest_path) ...
    dest_dir = os.path.dirname(dest_path)
    if dest_dir:
        os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(final_html)


def generate_pages_recursive(
    dir_path_content, template_path, dest_dir_path, base_url="/"
):  # Add base_url
    for item in os.listdir(dir_path_content):
        source_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_item_path):
            if source_item_path.endswith(".md"):
                dest_file_path = os.path.splitext(dest_item_path)[0] + ".html"
                # Pass base_url to the single page generator
                generate_page(source_item_path, template_path, dest_file_path, base_url)
        else:
            os.makedirs(dest_item_path, exist_ok=True)
            # Pass base_url to the recursive call
            generate_pages_recursive(
                source_item_path, template_path, dest_item_path, base_url
            )
