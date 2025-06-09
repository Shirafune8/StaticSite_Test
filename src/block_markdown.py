from enum import Enum
from htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "HEADING"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def markdown_to_blocks(markdown):
    if not isinstance(markdown, str):
        raise TypeError("Input must be a string")
    if not markdown.strip():
        return []
    # separate blocks by blank lines
    blocks = markdown.split("\n\n")
    # strip any leading or trailing whitespace from each block
    stripped_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if stripped_block: # only add non-empty blocks
            stripped_blocks.append(stripped_block)
    return stripped_blocks

def block_to_block_type(markdown):
    lines = markdown.split("\n")
    if markdown.startswith("#"):
        heading_level = len(markdown.split(" ")[0])
        if 1 <= heading_level <=6:
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH

    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith("> ") for line in markdown.split("\n")):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in markdown.split("\n")):
        return BlockType.UNORDERED_LIST
    elif all(line.startswith(f"{i}. ") for i, line in enumerate(lines, start=1)):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
    
