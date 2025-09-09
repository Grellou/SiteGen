from htmlnode import ParentNode
from inline_markdown import BlockType, block_to_block_type, markdown_to_blocks
from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text):
    """Converts raw text with inline markdown into a list of HTMLNodes."""
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children


def paragraph_to_html_node(block):
    """Converts a paragraph block to an HTML <p> node."""
    # Join lines to handle multi-line paragraphs
    lines = block.split("\n")
    content = " ".join(lines)
    children = text_to_children(content)
    return ParentNode("p", children)


def heading_to_html_node(block):
    """Converts a heading block to an HTML <h1>-<h6> node."""
    level = 0
    while block[level] == "#":
        level += 1
    # Strip the '#' characters and the following space
    content = block[level:].lstrip()
    children = text_to_children(content)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    """Converts a code block to an HTML <pre><code> node."""
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block format")

    # Slice off the ``` markers, but preserve internal content exactly
    content = block[3:-3]

    # Do NOT parse for inline markdown.
    # Create a single raw text node to hold the code content.
    text_node = TextNode(content, TextType.PLAIN_TEXT)
    leaf_node = text_node_to_html_node(text_node)

    # Wrap the raw text in a <code> tag, then a <pre> tag.
    code_node = ParentNode("code", [leaf_node])
    return ParentNode("pre", [code_node])


def quote_to_html_node(block):
    """Converts a quote block to an HTML <blockquote> node."""
    lines = block.split("\n")
    # Strip the leading '>' from each line and join them
    new_lines = [line.lstrip(">").strip() for line in lines]
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)


def ulist_to_html_node(block):
    """Converts an unordered list block to an HTML <ul> node."""
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # Strip the list marker ('* ' or '- ')
        content = line[2:]
        children = text_to_children(content)
        list_items.append(ParentNode("li", children))
    return ParentNode("ul", list_items)


def olist_to_html_node(block):
    """Converts an ordered list block to an HTML <ol> node."""
    lines = block.split("\n")
    list_items = []
    for line in lines:
        # Find the first space to robustly strip '1. ', '10. ', etc.
        i = line.find(" ")
        content = line[i + 1 :]
        children = text_to_children(content)
        list_items.append(ParentNode("li", children))
    return ParentNode("ol", list_items)


def markdown_to_html_node(markdown):
    """
    Converts a full markdown document to a parent HTMLNode (a div).
    """
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            children_nodes.append(heading_to_html_node(block))
        elif block_type == BlockType.CODE:
            children_nodes.append(code_to_html_node(block))
        elif block_type == BlockType.QUOTE:
            children_nodes.append(quote_to_html_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            children_nodes.append(ulist_to_html_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            children_nodes.append(olist_to_html_node(block))
        else:  # Paragraph is the default
            children_nodes.append(paragraph_to_html_node(block))

    return ParentNode("div", children_nodes)
