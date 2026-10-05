from enum import Enum;
from textnode import TextType, TextNode;
import re;


class BlockType(Enum):
    PARAGRAPH = "paragraph";
    HEADING = "heading";
    CODE = "code";
    QUOTE ="quote";
    UNORDERED_LIST = "unordered_list";
    ORDERED_LIST = "ordered_list";

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = [];

    for old_node in old_nodes:
        cur_text = old_node.text;
        cur_nodes = [];
        while cur_text is not None:
            cur_text_splitted = cur_text.split(delimiter, maxsplit=2);

            if len(cur_text_splitted) == 1:
                cur_nodes.append(TextNode(cur_text, old_node.text_type));
                cur_text = None;
            elif len(cur_text_splitted) < 3:
                raise Exception('invalid markdown');
            else:
                first,cur,last = cur_text_splitted;
                if first != '':
                    cur_nodes.append(TextNode(first, old_node.text_type));
                cur_nodes.append(TextNode(cur, text_type));
                cur_text = last;
        new_nodes.extend(cur_nodes);
    return new_nodes;

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = [];

    for old_node in old_nodes:
        cur_images = extract_markdown_images(old_node.text);
        cur_text = old_node.text;
        cur_nodes = [];
        for cur_image in cur_images:
            image_alt, image_url = cur_image;
            cur_text_splitted = cur_text.split(f'![{image_alt}]({image_url})', maxsplit=1);
            first, second = cur_text_splitted;
            if first != '':
                cur_nodes.append(TextNode(first, TextType.TEXT));
            cur_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url));
            cur_text = second;
        if len(cur_images) > 0:
            if cur_text != '':
                cur_nodes.append(TextNode(cur_text, TextType.TEXT));
        else:
            cur_nodes.append(old_node);
        new_nodes.extend(cur_nodes);
    return new_nodes;

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = [];

    for old_node in old_nodes:
        cur_images = extract_markdown_links(old_node.text);
        cur_text = old_node.text;
        cur_nodes = [];
        for cur_image in cur_images:
            link_text, link_url = cur_image;
            cur_text_splitted = cur_text.split(f'[{link_text}]({link_url})', maxsplit=1);
            first, second = cur_text_splitted;
            if first != '':
                cur_nodes.append(TextNode(first, TextType.TEXT));
            cur_nodes.append(TextNode(link_text, TextType.LINK, link_url));
            cur_text = second;
        if len(cur_images) > 0:
            if cur_text != '':
                cur_nodes.append(TextNode(cur_text, TextType.TEXT));
        else:
            cur_nodes.append(old_node);
        new_nodes.extend(cur_nodes);
    return new_nodes;

def text_to_textnodes(text: str):
    new_nodes = [TextNode(text, TextType.TEXT)];
    new_nodes = split_nodes_delimiter(new_nodes, '`', TextType.CODE);
    new_nodes = split_nodes_delimiter(new_nodes, '**', TextType.BOLD);
    new_nodes = split_nodes_delimiter(new_nodes, '_', TextType.ITALIC);
    new_nodes = split_nodes_link(new_nodes);
    new_nodes = split_nodes_image(new_nodes);
    
    return new_nodes;

def extract_markdown_images(text: str) -> tuple[str, str]:
    pattern = r'!\[(.*?)\]\((.*?)\)';
    markdown_images = [];
    for match in re.findall(pattern, text):
        markdown_images.append(match);
    return markdown_images;

def extract_markdown_links(text: str) -> tuple[str, str]:
    pattern = r'(?<!!)\[(.*?)\]\((.*?)\)';
    markdown_links = [];
    for match in re.findall(pattern, text):
        markdown_links.append(match);
    return markdown_links;

def markdown_to_blocks(markdown: str):
    blocks = [];
    for block in markdown.split('\n\n'):
        block_stripped = block.strip();
        if block_stripped != '':
            blocks.append(block_stripped);
    return blocks;

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