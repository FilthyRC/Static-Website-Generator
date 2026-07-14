from enum import Enum
from htmlnode import *
import re

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
        return (
            self.text == other.text and
            self.text_type == other.text_type and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
    
def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        if delimiter not in node.text:
            new_nodes.append(node)
            continue
        if node.text.count(delimiter) % 2 !=0:
            raise Exception("No closing delimiter")
        

        parts = node.text.split(delimiter)
        
        for i, part in enumerate(parts):
            if part == "":
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return links

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        markdown_links = extract_markdown_links(node.text)
        if len(markdown_links) > 0:
            for i, links in enumerate(markdown_links):
                markdown_link_str = f"[{str(links[0])}]({str(links[1])})"
                if i == 0:
                    parts = node.text.split(markdown_link_str)
                else:
                    parts = parts.split(markdown_link_str)
                new_nodes.append(TextNode(parts[0],TextType.TEXT))
                new_nodes.append(TextNode(str(links[0]), TextType.LINK, str(links[1])))
                parts = parts[1]
            if parts != "":
                new_nodes.append(TextNode(parts, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        markdown_images = extract_markdown_images(node.text)
        if len(markdown_images) > 0:
            for i, images in enumerate(markdown_images):
                markdown_img_str = f"![{str(images[0])}]({str(images[1])})"
                if i == 0:
                    parts = node.text.split(markdown_img_str)
                else:
                    parts = parts.split(markdown_img_str)
                new_nodes.append(TextNode(parts[0],TextType.TEXT))
                new_nodes.append(TextNode(str(images[0]), TextType.IMAGE, str(images[1])))
                parts = parts[1]
            if parts != "":
                new_nodes.append(TextNode(parts, TextType.TEXT))
        else:
            new_nodes.append(node)

    return new_nodes

def text_to_textnodes(text):
    nodes = []
    text_node = TextNode(text, TextType.TEXT)

    nodes = split_nodes_delimiter([text_node],"**",TextType.BOLD)
    nodes = split_nodes_delimiter(nodes,"_",TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes,"`",TextType.CODE)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)

    return nodes

