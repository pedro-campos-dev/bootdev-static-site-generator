import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode;


class TestHtmlNode(unittest.TestCase):
    def test_none(self):
        node = HTMLNode();
        self.assertEqual('', node.props_to_html());

    def test_empty(self):
        node = HTMLNode(props={});
        self.assertEqual('', node.props_to_html());

    def test_href(self):
        node = HTMLNode(props={'href': 'www.google.com'});
        self.assertEqual('href="www.google.com"', node.props_to_html());

    def test_multi_props(self):
        node = HTMLNode(props={'href': 'www.google.com', 'title': 'test'});
        self.assertEqual('href="www.google.com" title="test"', node.props_to_html());

    def test_leaf_node(self):
        node = LeafNode('p', 'This is some test', {'name': 'test'});
        self.assertEqual('<p name="test">This is some test</p>', node.to_html());

    def test_leaf_node_without_tag(self):
        node = LeafNode(None, 'This is some test', {'name': 'test'});
        self.assertEqual('This is some test', node.to_html());

    def test_leaf_node_err(self):
        node = LeafNode('p', None, None);
        error_message = None;
        try:
            html = node.to_html();
        except ValueError as ve:
            error_message = str(ve);
        self.assertEqual(True, 'missing value' in error_message);

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child");
        parent_node = ParentNode("div", [child_node]);
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>");


    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild");
        child_node = ParentNode("span", [grandchild_node]);
        parent_node = ParentNode("div", [child_node]);
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        );

    def test_to_html_with_grandchildren(self):
        grand_grandchild_node = LeafNode("b", "grandchild");
        grand_grandchild_node_1 = LeafNode(None, 'testing empty tag');
        grand_grandchild_node_2 = LeafNode('a', 'link', {'href': 'www.test.com', 'target': '_blank'});
        grandchild_node = ParentNode('span', [grand_grandchild_node, grand_grandchild_node_1, grand_grandchild_node_2]);
        child_node = ParentNode("p", [grandchild_node], {'name': 'testing'});
        parent_node = ParentNode("div", [child_node], {'data-name': 'test'});
        self.assertEqual(
            parent_node.to_html(),
            """<div data-name="test"><p name="testing"><span><b>grandchild</b>testing empty tag<a href="www.test.com" target="_blank">link</a></span></p></div>""",
        );

if __name__ == "__main__":
    unittest.main();