from enum import Enum
from htmlnode import HTMLNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes

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

def text_to_children(text):
    # Convert function into list of HTMLNode objects.
    text_nodes = text_to_textnodes(text) # Convert text to TextNodes
    return [text_node_to_html_node(node) for node in text_nodes] # Convert TextNodes to HTMLNodes

def markdown_to_html_node(markdown):
    # Convert a full markdown document into single parent HTMLNode. The parent HTMLNode should contain main child HTMLNodes
    blocks = markdown_to_blocks(markdown) # Split markdown into blocks using existing func.
    parent_node = HTMLNode("div") # Root node to contain all child nodes

    for block in blocks:
        block_type = block_to_block_type(block) # Determine type of block by looping with existing func

        if block_type == BlockType.HEADING:
            # Determine heading level
            heading_level = len(block.split(" ")[0])
            heading_text = block[heading_level + 1:]
            child_node = HTMLNode(f"h{heading_level}", heading_text)

        elif block_type == BlockType.PARAGRAPH:
            child_node = HTMLNode("p","", text_to_children(block))

        elif block_type == BlockType.CODE:
            code_content = "\n".join(block.split("\n")[1:-1])
            # text_node = TextNode(code_content, TextType.TEXT)
            child_node = HTMLNode("pre", "", [HTMLNode("code", code_content)]) # HTML codes use <pre></pre> for preformatted text

        elif block_type == BlockType.QUOTE:
            quote_content = "\n".join(line[2:] for line in block.split("\n"))
            child_node = HTMLNode("blockquote", quote_content)

        elif block_type == BlockType.UNORDERED_LIST: #HTML unordered list uses <ul><li>first item</li></ul> for unordered items (ul) and list (li)
            list_items = []
            for line in block.split("\n"):
                list_items.append(HTMLNode("li", line[2:]))
            child_node = HTMLNode("ul", list_items)
        
        elif block_type == BlockType.ORDERED_LIST: #HTML ordered list uses <ol><li>first item</li></ol> for ordered items (ol) and list (li)
            list_items = []
            for line in block.split("\n"):
                list_items.append(HTMLNode("li", line[line.index(". ") + 2:]))
            child_node = HTMLNode("ol", list_items)
        
        else:
            raise ValueError(f"Unsupported block type: {block_type}")
        
        # Add the child node to the parent node
        parent_node.add_child(child_node)
    return parent_node

