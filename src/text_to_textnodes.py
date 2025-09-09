from split_nodes import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def text_to_textnodes(text):
    """
    Converts a raw string of markdown into a list of TextNode objects,
    correctly handling all inline markdown syntax in the right order.
    """
    nodes = [TextNode(text, TextType.PLAIN_TEXT)]

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    # Process delimiters from longest to shortest to avoid conflicts
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD_TEXT)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC_TEXT)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE_TEXT)

    return nodes
