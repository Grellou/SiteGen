from textnode import TextNode, TextType
from utils import extract_markdown_images, extract_markdown_links


# Splits node by provided delimiter
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_list = []

    for node in old_nodes:
        if node.text_type == TextType.PLAIN_TEXT:
            # Raise exception if matching delimiter not found
            delimiter_count = node.text.count(delimiter)
            if not delimiter_count % 2 == 0:
                raise Exception("Missing closing delimiter")

            # Split str by delimiter
            split_str_list = node.text.split(delimiter)

            for i in range(0, len(split_str_list)):
                if split_str_list[i]:
                    if not i % 2 == 0:
                        txt_node = TextNode(split_str_list[i], text_type)
                        new_list.append(txt_node)
                    else:
                        txt_node = TextNode(split_str_list[i], TextType.PLAIN_TEXT)
                        new_list.append(txt_node)
        else:
            # Add to the list if it's not plain text
            new_list.append(node)
    return new_list


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
