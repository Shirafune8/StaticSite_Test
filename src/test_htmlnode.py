import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization(self): #test that node initlaizes the correct attributes
        node = HTMLNode(tag="p", value="introduction", children=None, props={"id": "main-header"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "introduction")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"id": "main-header"})

    def test_repr(self):
        node = HTMLNode(tag="p", value="hello", children=None, props={"class": "intro"})
        repr_string = repr(node)
        self.assertIsInstance(repr_string, str)
        self.assertIn("p", repr_string)
        self.assertIn("hello", repr_string)
        self.assertIn("intro", repr_string)

    def test_props_to_html_empty(self): #Test props_to-html
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")
    
    def test_props_to_html_with_props(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank"
        }
        node = HTMLNode(props=props)
        possible_outputs = [
            ' href="https://www.google.com" target="_blank"',
            ' target="_blank" href="https://www.google.com"'
        ]
        self.assertIn(node.props_to_html(), possible_outputs)

if __name__ == "__main__":
    unittest.main()