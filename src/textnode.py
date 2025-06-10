from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return( 
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        if text_node.url is None:
            raise ValueError("LINK type requires a URL.")
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        if text_node.url is None:
            raise ValueError("IMAGE type requires a URL.")
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unsupported text type: {text_node.text_type}")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
# delimiter are special characters that wrap around text, 
# It could be ` backtick for code like `code` or ** for **bold** or _ for _italic_
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            parts = node.text.split(delimiter)
            if len(parts) % 2 == 0: # checks for unmatched delimiters once.
                raise ValueError(f"Invalid Markdown syntax: unmatched delimiter '{delimiter}' in text '{node.text}'")
            # Loop through parts once.
            for i, part in enumerate(parts):
                # Alternate between TextType.TEXT and the provided text_type for delimited parts
               # if part: # check if part is empty or if len(part) > 0:
                    
                if i % 2 == 0: # create TextNode with correct type.
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            # If the node is not of type TEXT, add it directly to the new nodes list
            new_nodes.append(node)   
    return new_nodes

# Using Regex to breakdown markdown text into tuples with alt text and url
import re

def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)

def split_nodes_image(old_nodes): # Splits raw markdown text into TextNodes based on images
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Extract images from the text
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        else: # split text into parts for image capture groups
            text_parts = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
            i = 0
            while i < len(text_parts):
                text_part = text_parts[i]
                if text_part:
                    new_nodes.append(TextNode(text_part, TextType.TEXT))
                # If we're at an image match, the next two elements are alt and url
                if i + 2 < len(text_parts):
                    alt_text = text_parts[i+1]
                    url = text_parts[i+2]
                    new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
                i += 3
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # Extract links from the text
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        else: # split text into parts for link capture groups
            text_parts = re.split(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)
            i = 0
            while i < len(text_parts):
                text_part = text_parts[i]
                if text_part:
                    new_nodes.append(TextNode(text_part, TextType.TEXT))
                # If we're at an image match, the next two elements are alt and url
                if i + 2 < len(text_parts):
                    anchor_text = text_parts[i+1]
                    url = text_parts[i+2]
                    new_nodes.append(TextNode(anchor_text, TextType.LINK, url))
                i += 3
    return new_nodes

def text_to_textnodes(text):
    text = text.replace("\n", " ")
    text_node = TextNode(text, TextType.TEXT)

    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([text_node], "**", TextType.BOLD), 
                "_", TextType.ITALIC), 
            "`", TextType.CODE)))
