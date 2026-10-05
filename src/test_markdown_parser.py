import unittest
from textnode import TextNode, TextType;
from markdown_parser import split_nodes_delimiter;


class TestMarkdownParser(unittest.TestCase):
    def test_splitter(self):
        text_node = TextNode('`This` is a `code` in text with another `code` here', TextType.TEXT);
        expected = [];
        expected.append(TextNode('This', TextType.CODE));
        expected.append(TextNode(' is a', TextType.TEXT));
        expected.append(TextNode('code', TextType.CODE));
        expected.append(TextNode(' in text with another', TextType.TEXT));
        expected.append(TextNode('code', TextType.CODE));
        expected.append(TextNode(' here', TextType.TEXT));
        print(expected == split_nodes_delimiter([text_node], '`', TextType.CODE));
        self.assertEqual(', '.join([str(expected_node) for expected_node in expected]), ', '.join([str(new_node) for new_node in split_nodes_delimiter([text_node], '`', TextType.CODE)]));

if __name__ == "__main__":
    unittest.main();