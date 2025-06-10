import unittest

from block_markdown import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node

class TestMarkdowntoBlocks(unittest.TestCase):
    # Test markdown text to separate blocks of grouped text
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_input(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_whitespace_only(self):
        md = "     \n       \n"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block(self):
        md = "This is a single block of text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single block of text."])
    
    def test_multi_blocks_blank(self):
        md = "Block 1\n\nBlock 2\n\nBlock 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

# Test markdown block text inspection and determine what type of block it is.
class TestBlockToBlockType(unittest.TestCase):
    def test_heading(self):
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block\n```"), BlockType.CODE)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote.\n> Another line."), BlockType.QUOTE)

    def test_unordered_list(self):
        self.assertEqual(block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n2. Second item"), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)

    def test_malformed_heading(self):
        self.assertEqual(block_to_block_type("####### Invalid heading"), BlockType.PARAGRAPH)

    def test_malformed_code_block(self):
        self.assertEqual(block_to_block_type("```\nCode block without closing"), BlockType.PARAGRAPH)

    def test_malformed_quote_block(self):
        self.assertEqual(block_to_block_type("> This is a quote.\nNot a quote."), BlockType.PARAGRAPH)

    def test_malformed_ordered_list(self):
        self.assertEqual(block_to_block_type("1. First item\n3. Skipped number"), BlockType.PARAGRAPH)

class Test_Markdown_to_HTMLNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_all_markdown_to_html_node(self):
        md = """
# Heading 1

This is a **bold** paragraph with _italic_ text.

- Item 1
- Item 2

1. First item
2. Second item

```
Code block
```

> This is a quote.
"""
        html_node = markdown_to_html_node(md)

        # Check the structure of the resulting HTMLNode
        self.assertEqual(html_node.tag, "div")
        self.assertEqual(len(html_node.children), 6)
        self.assertEqual(html_node.children[0].tag, "h1")
        self.assertEqual(html_node.children[0].value, "Heading 1")
        self.assertEqual(html_node.children[1].tag, "p")
        self.assertEqual(html_node.children[2].tag, "ul")
        self.assertEqual(html_node.children[3].tag, "ol")
        self.assertEqual(html_node.children[4].tag, "pre")
        self.assertEqual(html_node.children[5].tag, "blockquote")

if __name__ == "__main__":
    unittest.main()