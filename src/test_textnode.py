import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


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

class TestMarkdownExtraction(unittest.TestCase):
    # Test markdown extraction to images
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_multi_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/image2.png)"
        )
        self.assertListEqual(
            [("image1", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/image2.png")], 
            matches
            )

    def test_malformed_image_syntax(self):
        matches = extract_markdown_images("This is text with ![image](missing_parenthesis")
        self.assertListEqual([], matches)

    def test_empty_alt_text(self):
        matches = extract_markdown_images("![](https://i.imgur.com/image.png)")
        self.assertListEqual([("", "https://i.imgur.com/image.png")], matches)

    def test_image_with_special_characters_in_url(self):
        matches = extract_markdown_images("![image](https://i.imgur.com/image.png?query=123&key=value)")
        self.assertListEqual([("image", "https://i.imgur.com/image.png?query=123&key=value")], matches)

    def test_extract_markdown_no_image(self):
        matches = extract_markdown_images("There are no images")
        self.assertListEqual([], matches)

    # Test markdown extraction to links
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://www.boot.dev/@bootdotdev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev/@bootdotdev")], matches)
    
    def test_extract_markdown_no_link(self):
        matches = extract_markdown_images("There is no link")
        self.assertListEqual([], matches)
    
    def test_multiple_links(self):
        matches = extract_markdown_links(
        "[link1](https://www.example.com) and [link2](https://www.anotherexample.com)"
        )
        self.assertListEqual(
        [("link1", "https://www.example.com"), ("link2", "https://www.anotherexample.com")],
        matches
        )

    def test_malformed_link_syntax(self):
        matches = extract_markdown_links("This is text with [link](missing_parenthesis")
        self.assertListEqual([], matches)

    def test_empty_link_text(self):
        matches = extract_markdown_links("[](https://www.example.com)")
        self.assertListEqual([("", "https://www.example.com")], matches)

    def test_link_with_special_characters_in_url(self):
        matches = extract_markdown_links("[link](https://www.example.com?query=123&key=value)")
        self.assertListEqual([("link", "https://www.example.com?query=123&key=value")], matches)

    # Test with both images and links to make sure the respective elements are extracted
    def test_text_with_images_and_links(self):
        image_matches = extract_markdown_images(
        "![image](https://i.imgur.com/image.png) and [link](https://www.example.com)"
        )
        link_matches = extract_markdown_links(
        "![image](https://i.imgur.com/image.png) and [link](https://www.example.com)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/image.png")], image_matches)
        self.assertListEqual([("link", "https://www.example.com")], link_matches)

    def test_empty_input_text(self):
        image_matches = extract_markdown_images("")
        link_matches = extract_markdown_links("")
        self.assertListEqual([], image_matches)
        self.assertListEqual([], link_matches)

# Text markdown extraction with images and links
class TestMarkdownExtractionImagesLinks(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.boots.dev) and another [second link](https://www.youtube.com/@bootsdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.boots.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://www.youtube.com/@bootsdotdev"
                ),
            ],
            new_nodes,
        )

# Test raw string markdown convertion into TextNode objects
class TestConvertRawToTextNode(unittest.TestCase):
    def test_all_split_functions_together_to_TextNode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], new_nodes,
        )

    def test_text_to_textnodes_no_markdown(self):
        text = "This is plain text without any Markdown."
        result = text_to_textnodes(text)

        expected = [
            TextNode("This is plain text without any Markdown.", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_text_to_textnodes_empty_text(self):
        text = ""
        result = text_to_textnodes(text)

        expected = [
            TextNode("", TextType.TEXT),
        ]

        self.assertListEqual(result, expected)

    def test_text_to_textnodes_malformed_markdown(self):
        text = "This is **bold text with unmatched _italic and ![image](missing_parenthesis"
        with self.assertRaises(ValueError) as context: # This captures the exception information into a variable called context
            result = text_to_textnodes(text)
        # Take the error message from the exception that was raised, and make sure it exactly matches this expected message."
        self.assertEqual(str(context.exception), "Invalid Markdown syntax: unmatched delimiter '**' in text 'This is **bold text with unmatched _italic and ![image](missing_parenthesis'")

if __name__ == "__main__":
    unittest.main()