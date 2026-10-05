from textnode import TextType, TextNode;

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes: list[TextNode] = [];

    for old_node in old_nodes:
        cur_text = old_node.text;
        cur_nodes = [];
        while cur_text is not None:
            cur_text_splitted = cur_text.split(delimiter, maxsplit=2);

            if len(cur_text_splitted) == 1:
                cur_nodes.append(TextNode(cur_text, TextType.TEXT));
                cur_text = None;
            elif len(cur_text_splitted) < 3:
                raise Exception('invalid markdown');
            else:
                first,cur,last = cur_text_splitted;
                if first != '':
                    cur_nodes.append(TextNode(first, TextType.TEXT));
                cur_nodes.append(TextNode(cur, text_type));
                cur_text = last;
        new_nodes.extend(cur_nodes);
    return new_nodes;
