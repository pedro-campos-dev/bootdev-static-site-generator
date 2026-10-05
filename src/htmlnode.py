class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict[str, str] | None = None):
        self.tag = tag;
        self.value = value;
        self.children = children;
        self.props = props;

    def to_html(self):
        raise NotImplementedError('this method is not implemented');

    def props_to_html(self):
        if self.props is None or not self.props:
            return "";

        props = [];
        for prop in self.props:
            props.append(f'{prop}="{self.props[prop]}"');
        return " ".join(props);

    def __repr__(self):
        return f'Tag: {"No Tag" if self.tag is None else self.tag}, Value: {"No Value" if self.value is None else self.value}, Props: {self.props_to_html()}, Children: {"" if self.children is None else ", ".join([child.tag for child in self.children])}';

class LeafNode(HTMLNode):
    def __init__(self, tag: str | None, value: str, props: dict[str, str] | None = None):
        super().__init__(tag, value, None, props);

    def to_html(self):
        if self.value is None:
            raise ValueError('missing value');

        if self.tag is None:
            return self.value;

        props = self.props_to_html();
        return f'<{self.tag}{'' if not props else ' '}{props}>{self.value}</{self.tag}>';

    def __repr__(self):
        return f'Tag: {"No Tag" if self.tag is None else self.tag}, Value: {"No Value" if self.value is None else self.value}, Props: {self.props_to_html()}';

class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list['HTMLNode'], props: dict[str, str] | None = None):
        super().__init__(tag, None, children, props);

    def to_html(self):
        if not self.tag:
            raise ValueError('missing tag');

        if not self.children:
            raise ValueError('missing children');

        child_nodes = [];
        for child in self.children:
            child_nodes.append(child.to_html());

        cur_props = self.props_to_html();
        return f'<{self.tag}{'' if not cur_props else ' '}{cur_props}>{''.join(child_nodes)}</{self.tag}>';

    def __repr__(self):
        return f'Tag: {"No Tag" if self.tag is None else self.tag}, Props: {self.props_to_html()}, Children: {"" if self.children is None else ", ".join([child.tag for child in self.children])}';