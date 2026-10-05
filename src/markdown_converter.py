from markdown_parser import block_to_block_type, BlockType, markdown_to_blocks, text_to_textnodes;
from textnode import text_node_to_html_node, TextNode, TextType;
from htmlnode import HTMLNode, ParentNode;
import re;

def markdown_to_html_node(markdown: str) -> HTMLNode:
    markdown_blocks: list[str] = markdown_to_blocks(markdown);
    html_nodes = [];
    for markdown_block in markdown_blocks:
        block_type = block_to_block_type(markdown_block);
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(ParentNode('p', text_to_children(markdown_block.replace('\n', ' '))));
        elif block_type == BlockType.CODE:
            html_nodes.append(ParentNode('pre', [text_node_to_html_node(TextNode(markdown_block.replace('```\n', '').replace('```', ''), TextType.CODE))]));
        elif block_type == BlockType.QUOTE:
            quote_lines = [];
            for quote_line in markdown_block.splitlines():
                quote_lines.append(remove_prefix(quote_line, block_type));
            html_nodes.append(ParentNode('blockquote', text_to_children(' '.join(quote_lines))));
        elif block_type == BlockType.UNORDERED_LIST:
            child_nodes = [];
            for line in markdown_block.splitlines():
                child_nodes.append(ParentNode('li', text_to_children(remove_prefix(line, block_type))));
            html_nodes.append(ParentNode('ul', child_nodes));
        elif block_type == BlockType.ORDERED_LIST:
            child_nodes = [];
            for line in markdown_block.splitlines():
                child_nodes.append(ParentNode('li', text_to_children(remove_prefix(line, block_type))));
            html_nodes.append(ParentNode('ol', child_nodes));
        else:
            html_nodes.append(ParentNode(get_header_tag(markdown_block), text_to_children(remove_prefix(markdown_block, block_type))));
    return ParentNode('div', html_nodes);
            
def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text);
    return [text_node_to_html_node(text_node) for text_node in text_nodes];

def remove_prefix(text: str, block_type: BlockType):
    if block_type == BlockType.ORDERED_LIST:
        return re.split(r'^\d+\.\s', text.strip())[1];
    elif block_type == BlockType.UNORDERED_LIST:
        return re.split(r'^-\s', text.strip())[1];
    elif block_type == BlockType.QUOTE:
        return re.split(r'^>\s{0,1}', text.strip())[1];
    elif block_type == BlockType.HEADING:
        return re.split(r'^#{1,6}\s', text.strip())[1];
    else:
        return text;
        

def get_header_tag(text: str) -> str:
    if text.startswith('######'):
        return 'h6';
    elif text.startswith('#####'):
        return 'h5';
    elif text.startswith('####'):
        return 'h4';
    elif text.startswith('###'):
        return 'h3';
    elif text.startswith('##'):
        return 'h2';
    else:
        return 'h1';