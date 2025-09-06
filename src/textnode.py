from enum import Enum

from htmlnode import LeafNode


# Define the possible types of text nodes
class TextType(Enum):
    PLAIN_TEXT = "plain"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


def text_node_to_html_node(text_node):
    if not text_node.text_type:
        raise Exception("Text node has no text type.")

    # Plain text with no tags
    if text_node.text_type == TextType.PLAIN_TEXT:
        return LeafNode(None, text_node.text)
    # Text with bold tag
    elif text_node.text_type == TextType.BOLD_TEXT:
        return LeafNode("b", text_node.text)
    # Text with italic tag
    elif text_node.text_type == TextType.ITALIC_TEXT:
        return LeafNode("i", text_node.text)
    # Text with code tag
    elif text_node.text_type == TextType.CODE_TEXT:
        return LeafNode("code", text_node.text)
    # Text with a tag and href prop
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    # Img tag with src and alt props
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})


class TextNode:
    def __init__(self, text, text_type: TextType, url=None):
        self.text = text  # Raw text
        self.text_type = text_type  # Type of text
        self.url = url  # URL for links or images

    def __eq__(self, other):
        if isinstance(other, TextNode):
            if (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            ):
                return True
            else:
                return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
