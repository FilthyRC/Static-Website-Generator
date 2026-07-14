import unittest
from textnode import *
from htmlnode import *
from blocks import *
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node.url, None)
    
    def test_valid_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://google.com")

        self.assertNotEqual(node.url, None)
    
    def test_diff(self):
        node = TextNode("This is a anchor node", TextType.LINK, "https://google.com")
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertNotEqual(node, node2)
    
    def test_print_details(self):
        node = TextNode("This is a anchor node", TextType.LINK, "https://google.com")
        print("\n----- TextNode Print -----")
        print(node)

class TestHTMLNode(unittest.TestCase):
    # ===== Main Class Tests =====
    def test_props_populated(self):
        node = HTMLNode(props={
            "href": "https://www.google.com",
            "target": "_blank",
            })
        expected = ' href="https://www.google.com" target="_blank"'

        self.assertEqual(node.props_to_html(), expected)
    
    def test_props_unpopulated(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")

    def test_print(self):
        node = HTMLNode("<p>","this is a p tag")
        print("\n----- HTMLNode Print -----")
        print(node)


    # ===== LeadNode Tests ======
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")   

        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Hello, world!")  

        self.assertEqual(node.to_html(), "<b>Hello, world!</b>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!") 

        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p",None).to_html()
    
    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world!")  

        self.assertEqual(node.to_html(), node.value)


    # ===== ParentNode Tests ======
    def test_parent_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None,"test").to_html()

    def test_parent_no_children(self):
            with self.assertRaises(ValueError):
                ParentNode("test", None).to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span>child</span></div>"

        self.assertEqual(parent_node.to_html(), expected)

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        expected = "<div><span><b>grandchild</b></span></div>"

        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_node_with_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode("i", "Italic text")
        node = ParentNode("div", [child1, child2])
        expected = "<div><b>Bold text</b><i>Italic text</i></div>"

        self.assertEqual(node.to_html(), expected)

    def test_parent_node_with_props(self):
        child = LeafNode("p", "Hello")
        node = ParentNode("div", [child], {"class": "container", "id": "main"})
        expected = '<div class="container" id="main"><p>Hello</p></div>'

        self.assertEqual(node.to_html(), expected)

    def test_parent_no_children_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

    def test_parent_empty_children_list_raises(self):
        with self.assertRaises(ValueError):
            ParentNode("div", []).to_html()

    def test_parent_no_tag_raises(self):
        child = LeafNode("p", "Hello")
        with self.assertRaises(ValueError):
            ParentNode(None, [child]).to_html()

    def test_nested_parent_nodes(self):
        inner = ParentNode("div", [LeafNode("p", "Nested")])
        outer = ParentNode("body", [inner])
        expected = "<body><div><p>Nested</p></div></body>"

        self.assertEqual(outer.to_html(), expected)

    # ===== Text Type to HTML Tests =====
    def test_text_node_to_plain_text(self):
        text_node = TextNode("Just normal text", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.to_html(), "Just normal text")

    def test_text_node_to_bold(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.to_html(), "<b>Bold text</b>")

    def test_text_node_to_italic(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.to_html(), "<i>Italic text</i>")

    def test_text_node_to_code(self):
        text_node = TextNode("print('hello')", TextType.CODE)
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.to_html(), "<code>print('hello')</code>")

    def test_text_node_to_link(self):
        text_node = TextNode("Click me", TextType.LINK, url="https://boot.dev")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(html_node.to_html(), '<a href="https://boot.dev">Click me</a>')

    def test_text_node_to_image(self):
        text_node = TextNode("Alt text here", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(text_node)
        
        self.assertEqual(
            html_node.to_html(), 
            '<img src="https://example.com/image.png" alt="Alt text here">'
        )

    def test_empty_text(self):
        text_node = TextNode("", TextType.TEXT)
        html_node = text_node_to_html_node(text_node)
        self.assertEqual(html_node.to_html(), "")

    # ===== Delimiter Testing =====
    def test_split_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_italic(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))

    def test_split_code(self):
        node = TextNode("Here is `code` example", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        self.assertEqual(new_nodes[1], TextNode("code", TextType.CODE))

    def test_no_delimiter(self):
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_multiple_delimiters(self):
        node = TextNode("This **bold** and **another bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        
        self.assertEqual(len(new_nodes), 4)

    def test_delimiter_at_start(self):
        node = TextNode("**Bold** at the start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("Bold", TextType.BOLD))

    def test_delimiter_at_end(self):
        node = TextNode("At the end **bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[-1], TextNode("bold", TextType.BOLD))

    def test_non_text_node(self):
        node = TextNode("Some bold", TextType.BOLD)  # already formatted
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0], node)

    def test_empty_string_between_delimiters(self):
        node = TextNode("**", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_unclosed_delimiter(self):
        node = TextNode("This is **unclosed", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)
    

    # ===== Find Link + Image =====
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )
    
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

    # ===== Full Node Creation Tests =====
    def test_node_creation(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.maxDiff = None
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
            ],
            nodes
        )

class TestBlock(unittest.TestCase):
    # ===== Markdown Block Test =====
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
    
    


if __name__ == "__main__":
    unittest.main()
