from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"

def block_to_block_type(block:str):
    if block.startswith("#"):
        start = block.split(" ",1)[0]
        if len(start) <= 6 and all(c=="#" for c in start):
            return BlockType.HEADING

    if block.startswith("```\n"):
        return BlockType.CODE
    
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    
    if all(line.startswith(f"{i+1}. ") for i,line in enumerate(lines)):
        return BlockType.OLIST
    
    return BlockType.PARAGRAPH




def markdown_to_blocks(md):
    return md.strip().split("\n\n")

print(block_to_block_type("1. hello\n2. hwllo"))