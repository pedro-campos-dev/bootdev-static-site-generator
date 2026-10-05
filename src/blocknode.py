from enum import Enum;
import re;

class BlockType(Enum):
    PARAGRAPH = "paragraph";
    HEADING = "heading";
    CODE = "code";
    QUOTE ="quote";
    UNORDERED_LIST = "unordered_list";
    ORDERED_LIST = "ordered_list";
    
def block_to_block_type(markdown_block: str) -> BlockType:
    if re.match(r'#{1,6}\s', markdown_block):
        return BlockType.HEADING;
    elif re.fullmatch(r'```(.|\n)*```', markdown_block):
        return BlockType.CODE;
    else:
        all_quote = True;
        all_unordered = True;
        all_numbered = True;
        
        for line in markdown_block.splitlines():
            if not re.match(r'>\s*', line):
                all_quote = False;
            if not re.match(r'-\s', line):
                all_unordered = False;
            if not re.match(r'\d+\.\s', line):
                all_numbered = False;
        if all_quote:
            return BlockType.QUOTE;
        elif all_unordered:
            return BlockType.UNORDERED_LIST;
        elif all_numbered:
            return BlockType.ORDERED_LIST;
        else:
            return BlockType.PARAGRAPH;
        
        
        
    