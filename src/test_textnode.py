import unittest

from textnode import TextNode, TextType, text_node_to_html_node


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

if __name__ == "__main__":
    unittest.main()