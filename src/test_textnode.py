import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_noteq_url(self):
        node = TextNode("This is a testing node", TextType.ITALIC, url=None)
        node2 = TextNode("This is a testing node", TextType.ITALIC, url="https://www.google.com")
        self.assertNotEqual(node, node2)
    
    def test_noteq_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a testing text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    
    # Test text_node_to_html_node() function
    def test_text_node_to_html_node_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold Text")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italics Text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italics Text")

    def test_text_node_to_html_node_code(self):
        node = TextNode("Code displayed", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code displayed")

    def test_text_node_to_html_node_link(self):
        node = TextNode("Google link displayed", TextType.LINK, url="https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Google link displayed")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_text_node_to_html_node_link_no_url(self):
        node = TextNode("Google link displayed", TextType.LINK)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_node_to_html_node_image(self):
        node = TextNode("Image here with alt text", TextType.IMAGE, url="https://img.com/pics.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://img.com/pics.png", "alt": "Image here with alt text"})

    def test_text_node_to_html_node_image_no_url(self):
        node = TextNode("Image here with alt text", TextType.IMAGE)
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

    def test_text_node_to_html_node_unsupported_type(self):
        node = TextNode("This is a list item", "")
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)

# Test Split Node Delimiters that create TextNodes from raw markdown strings.
class TestSplitNodesDelimiter(unittest.TestCase):
    def test_basic_split(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
        ]
        self.assertEqual(len(result), 3) # or write it like below
        self.assertEqual(result, expected)

    def test_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("This is plain text", TextType.TEXT))

    def test_unmatched_delimiter(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError) as context: # This captures the exception information into a variable called context
            split_nodes_delimiter([node], "`", TextType.CODE) 
        # Take the error message from the exception that was raised, and make sure it exactly matches this expected message."
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: unmatched delimiter '`' in text 'This is text with a `code block word'")

    def test_multiple_nodes(self):
        nodes = [
            TextNode("Text with `code`", TextType.TEXT),
            TextNode("Another `example` here", TextType.TEXT)
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        
        expected = [
            TextNode("Text with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT),
            TextNode("Another ", TextType.TEXT),
            TextNode("example", TextType.CODE),
            TextNode(" here", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_non_text_node(self):
        node = TextNode("Bold text", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_special_character_delimiter(self):
        node = TextNode("This is text with a ~special~ delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "~", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("special", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" delimiter", TextType.TEXT))

    def test_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], TextNode("", TextType.TEXT))

    def test_delimiter_at_start(self):
        node = TextNode("`code block` at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" at the start", TextType.TEXT))

    def test_delimiter_at_end(self):
        node = TextNode("Text with `code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("Text with ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode("", TextType.TEXT))

    def test_multiple_delimiters(self):
        node = TextNode("This is text with a `code block` and ~bold~ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "~", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" and ", TextType.TEXT))
        self.assertEqual(new_nodes[3], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[4], TextNode(" text", TextType.TEXT))

if __name__ == "__main__":
    unittest.main()