import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()