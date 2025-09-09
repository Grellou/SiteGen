import re
from enum import Enum


# The 6 types of markdown blocks
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block):
    # Check for Heading (must be H1-H6)
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    # Check for Code block
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    # Split block into lines for further checks
    lines = block.split("\n")

    # Check for Quote block (all lines must start with '>')
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    # Check for Unordered List block (all lines must start with '* ' or '- ')
    if all(line.startswith("* ") or line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    # Check for Ordered List block
    # (all lines must start with 'i. ' and increment from 1)
    is_ordered_list = True
    for i, line in enumerate(lines):
        # Check if the line starts with the correct number, a dot, and a space
        if not line.startswith(f"{i + 1}. "):
            is_ordered_list = False
            break
    if is_ordered_list:
        return BlockType.ORDERED_LIST

    # If none of the above, it's a Paragraph
    return BlockType.PARAGRAPH


def markdown_to_blocks(markdown):
    """
    Splits a raw markdown string into a list of "blocks".
    A block is a chunk of text separated by two or more newlines.
    """
    blocks = []
    # Split by 2 or more newlines
    split_by_newlines = re.split(r"\n{2,}", markdown)
    for block in split_by_newlines:
        if block.strip():  # Ensure the block isn't just whitespace
            blocks.append(block.strip())
    return blocks
