from textnode import TextNode;

def main() -> None:
    new_node = TextNode('This is some anchor text', 'link', 'https://www.boot.dev');
    print(new_node);

if __name__ == '__main__':
    main();