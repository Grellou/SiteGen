from textnode import TextNode, TextType
from utils import extract_markdown_images, extract_markdown_links


# Splits node by provided delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    """
    A robust function to split text nodes by a given delimiter (like **, *, or `).
    """
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(old_node)
            continue

        split_text = old_node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError(f"Invalid markdown: unclosed delimiter '{delimiter}'")

        for i, text_segment in enumerate(split_text):
            if text_segment == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(text_segment, TextType.PLAIN_TEXT))
            else:
                new_nodes.append(TextNode(text_segment, text_type))

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text_to_split = node.text
        images = extract_markdown_images(text_to_split)

        if not images:
            new_nodes.append(node)
            continue

        for alt_text, url in images:
            parts = text_to_split.split(f"![{alt_text}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text_to_split = parts[1]

        if text_to_split:
            new_nodes.append(TextNode(text_to_split, TextType.PLAIN_TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN_TEXT:
            new_nodes.append(node)
            continue

        text_to_split = node.text
        links = extract_markdown_links(text_to_split)

        if not links:
            new_nodes.append(node)
            continue

        for link_text, url in links:
            # We must use a non-greedy regex here to avoid issues with `findall` and links
            parts = text_to_split.split(f"[{link_text}]({url})", 1)

            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.PLAIN_TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            text_to_split = parts[1]

        if text_to_split:
            new_nodes.append(TextNode(text_to_split, TextType.PLAIN_TEXT))

    return new_nodes
