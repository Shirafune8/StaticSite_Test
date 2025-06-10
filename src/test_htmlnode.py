import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_initialization(self): #test that node initlaizes the correct attributes
        node = HTMLNode(tag="p", value="introduction", children=None, props={"id": "main-header"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "introduction")
        self.assertEqual(node.children, [])
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

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", None)
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_noTag(self):
        node = LeafNode(None, "Hello, world!", None)
        self.assertEqual(node.to_html(), "Hello, world!")
        # print(node.to_html())

    def test_leaf_to_html_link(self):
        node = LeafNode("a", "Click link", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click link</a>')
        # print(node.to_html())

    def test_leaf_to_html_NoValue(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", "", "")
            node.to_html()

    def test_leaf_to_html_None(self):
        with self.assertRaises(ValueError):
            node = LeafNode("p", None, None)
            node.to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
         parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_tag_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode("", [], {
            "href": "https://www.google.com",
            "target": "_blank"
        })
            node.to_html()

    def test_parent_to_html_children_error(self):
        with self.assertRaises(ValueError):
            node = ParentNode("p", [], {
            "href": "https://www.google.com",
            "target": "_blank"
        })
            node.to_html()

if __name__ == "__main__":
    unittest.main()