import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag=p, value=introduction)
        node2 = HTMLNode(tag=p, value=introduction)
        self.assertEqual(node, node2)

    def test_url(self):
        node = HTMLNode("This is a testing node", HTMLNode.ITALIC)
        node2 = HTMLNode("This is a testing node", HTMLNode.ITALIC)
        self.assertNotEqual(node, node2)
    
    def test_italic(self):
        node = HTMLNode("This is a text node", TextType.ITALIC)
        node2 = HTMLNode("This is a testing text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()