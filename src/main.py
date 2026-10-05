import os;
import shutil;
from markdown_parser import block_to_block_type, markdown_to_blocks, BlockType;
from markdown_converter import markdown_to_html_node;

def copy_contents(src: str, dest: str, is_root: bool):
    for item in os.listdir(src):
        cur_path = f'{src}/{item}';
        if os.path.isfile(cur_path):
            if not is_root and not os.path.exists(dest):
                print('Creating folder', dest);
                os.mkdir(dest);
            print('Copying file', cur_path);
            shutil.copy(cur_path, dest);
        else:
            copy_contents(cur_path, f'{dest}/{item}', False);

def extract_title(markdown: str) -> str:
    markdown_blocks = markdown_to_blocks(markdown);
    if block_to_block_type(markdown_blocks[0]) == BlockType.HEADING and markdown_blocks[0].startswith('# '):
        return markdown_blocks[0].replace('# ', '').strip();
    else:
        raise Exception('missing title');
    
def generate_pages_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for item in os.listdir(dir_path_content):
        cur_path = f'{dir_path_content}/{item}';
        dest_path = f'{dest_dir_path}/{item}';
        if os.path.isfile(cur_path):
            generate_page(cur_path, template_path, dest_path.replace('.md', '.html'));
        else:
            generate_pages_recursive(cur_path, template_path, dest_path);
    
def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}');
    markdown_file = None;
    with open(from_path, 'r') as f:
        markdown_file = f.read();
    template_file = None;
    with open(template_path, 'r') as f:
        template_file = f.read();
    html_node = markdown_to_html_node(markdown_file);
    html_content = html_node.to_html();
    title = extract_title(markdown_file);
    new_html = template_file.replace('{{ Title }}', title).replace('{{ Content }}', html_content);
    os.makedirs('/'.join(dest_path.split('/')[:-1]), exist_ok=True);
    with open(dest_path, 'w') as f:
        f.write(new_html);
    
def main() -> None:
    shutil.rmtree('public');
    os.mkdir('public');
    copy_contents('static', 'public', True);
    generate_pages_recursive('content', 'template.html', 'public');

if __name__ == '__main__':
    main();