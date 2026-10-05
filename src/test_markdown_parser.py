import unittest
from textnode import TextNode, TextType;
from markdown_parser import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes, markdown_to_blocks, BlockType, block_to_block_type;


class TestMarkdownParser(unittest.TestCase):
    def test_splitter(self):
        text_node = TextNode('`This` is a `code` in text with another `code` here', TextType.TEXT);
        expected = [];
        expected.append(TextNode('This', TextType.CODE));
        expected.append(TextNode(' is a ', TextType.TEXT));
        expected.append(TextNode('code', TextType.CODE));
        expected.append(TextNode(' in text with another ', TextType.TEXT));
        expected.append(TextNode('code', TextType.CODE));
        expected.append(TextNode(' here', TextType.TEXT));
        new_nodes = split_nodes_delimiter([text_node], '`', TextType.CODE);
        self.assertEqual(len(expected), len(new_nodes));
        all_correct = True;
        for i in range(len(new_nodes)):
            if expected[i] != new_nodes[i]:
                all_correct = False;
                break;
        self.assertEqual(all_correct, True);
    
    def test_splitter_2(self):
        text_node = TextNode('This is a __italic__ text with some **bold** text', TextType.TEXT);
        text_node_2 = TextNode('This only has **bold** text here', TextType.TEXT);
        expected = [];
        expected.append(TextNode('This is a __italic__ text with some ', TextType.TEXT));
        expected.append(TextNode('bold', TextType.BOLD));
        expected.append(TextNode(' text', TextType.TEXT));
        expected.append(TextNode('This only has ', TextType.TEXT));
        expected.append(TextNode('bold', TextType.BOLD));
        expected.append(TextNode(' text here', TextType.TEXT));
        new_nodes = split_nodes_delimiter([text_node, text_node_2], '**', TextType.BOLD);
        self.assertEqual(len(expected), len(new_nodes));
        all_correct = True;
        for i in range(len(new_nodes)):
            if expected[i] != new_nodes[i]:
                all_correct = False;
                break;
        self.assertEqual(all_correct, True);
        
    def test_markdown_images(self):
        matches = extract_markdown_images('This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)');
        self.assertEqual(2, len(matches));
        self.assertListEqual([('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], matches);

    def test_markdown_images_mixed(self):
        matches = extract_markdown_images('This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and [dark vader](https://i.imgur.com/fJRm4Vk.jpeg)');
        self.assertEqual(2, len(matches));
        self.assertListEqual([('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], matches);

    def test_markdown_images_empty(self):
        matches = extract_markdown_images('This is text without any images');
        self.assertEqual(0, len(matches));
        self.assertListEqual([], matches);    
    
    def test_markdown_links(self):
        matches = extract_markdown_links('This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg)');
        self.assertEqual(2, len(matches));
        self.assertListEqual([('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], matches);

    def test_markdown_links_mixed(self):
        matches = extract_markdown_links('This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://i.imgur.com/fJRm4Vk.jpeg) and ![dark vader](https://i.imgur.com/fJRm4Vk.jpeg)');
        self.assertEqual(2, len(matches));
        self.assertListEqual([('rick roll', 'https://i.imgur.com/aKaOqIh.gif'), ('obi wan', 'https://i.imgur.com/fJRm4Vk.jpeg')], matches);

    def test_markdown_links_empty(self):
        matches = extract_markdown_links('This is text without any images');
        self.assertEqual(0, len(matches));
        self.assertListEqual([], matches);    
    
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        );
        new_nodes = split_nodes_image([node]);
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        );
    
    def test_split_images_mixed(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a link [link](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        );
        new_nodes = split_nodes_image([node]);
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a link [link](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        );
        
    def test_split_links(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        );
    
    def test_split_links_mixed(self):
        node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and a image ![image](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        );
        new_nodes = split_nodes_link([node]);
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a image ![image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        );
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes('This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)');
        expected = [
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
        ];
        self.assertListEqual(expected, nodes);

    def test_text_to_textnodes_not_all_types(self):
        nodes = text_to_textnodes('This is **text** with words and a `code block` and a [link](https://boot.dev)');
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with words and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ];
        self.assertListEqual(expected, nodes);
        
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
        
    def test_markdown_to_blocks_extra_lines(self):
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
    def test_paragraph(self):
        block_type = block_to_block_type('This is just a paragraph');
        self.assertEqual(BlockType.PARAGRAPH, block_type);
    def test_code(self):
        block_type = block_to_block_type('```\nThis is a code block\n```');
        self.assertEqual(BlockType.CODE, block_type);
    def test_quote(self):
        block_type = block_to_block_type('>This is the first item of the quote\n> This is the second item of the quote');
        self.assertEqual(BlockType.QUOTE, block_type);
    def test_unordered_list(self):
        block_type = block_to_block_type('- This is the first item of the list\n- This is the second item of the list');
        self.assertEqual(BlockType.UNORDERED_LIST, block_type);
    def test_ordered_list(self):
        block_type = block_to_block_type('1. This is the first item of the list\n2. This is the second item of the list');
        self.assertEqual(BlockType.ORDERED_LIST, block_type);
    def test_heading_1(self):
        block_type = block_to_block_type('# This is a heading');
        self.assertEqual(BlockType.HEADING, block_type);
    def test_heading_2(self):
        block_type = block_to_block_type('## This is a heading');
        self.assertEqual(BlockType.HEADING, block_type);
    def test_heading_3(self):
        block_type = block_to_block_type('### This is a heading');
        self.assertEqual(BlockType.HEADING, block_type);
    def test_heading_4(self):
        block_type = block_to_block_type('#### This is a heading');
        self.assertEqual(BlockType.HEADING, block_type);
    def test_heading_5(self):
        block_type = block_to_block_type('##### This is a heading');
        self.assertEqual(BlockType.HEADING, block_type);
    def test_heading_6(self):
        block_type = block_to_block_type('###### This is a heading');
        self.assertEqual(BlockType.HEADING, block_type);
    def test_non_heading(self):
        block_type = block_to_block_type('######$ This is not a heading');
        self.assertEqual(BlockType.PARAGRAPH, block_type);
    def test_non_unordered_list(self):
        block_type = block_to_block_type('- This is the first item of the list\n-This is the second item of the list');
        self.assertEqual(BlockType.PARAGRAPH, block_type);
    def test_non_ordered_list(self):
        block_type = block_to_block_type('1. This is the first item of the list\n2.This is the second item of the list');
        self.assertEqual(BlockType.PARAGRAPH, block_type);

if __name__ == "__main__":
    unittest.main();