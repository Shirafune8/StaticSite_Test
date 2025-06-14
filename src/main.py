import os

from block_markdown import extract_title, markdown_to_html_node

def main():
    copy_source_static_to_destination_public_directory()
    generate_pages_recursive("content", "template.html", "public")

def copy_source_static_to_destination_public_directory(src="static", dest='public'):
    # Delete directory and contents
    def delete_dir(path):
        if not os.path.exists(path):
            return
        for item in os.listdir(path):
            full_path = os.path.join(path, item)
            if os.path.isdir(full_path):
                delete_dir(full_path)
            else:
                print(f"Deleting file: {full_path}")
                os.remove(full_path) # removes file
        print(f"Deleting directory: {path}")
        os.rmdir(path) # removes directory

    def recursive_copy(src_path, dest_path):
    # Copy files and directories recursively to destination directory aka public        
        if not os.path.exists(dest_path):
            os.mkdir(dest_path) # create directory

        for item in os.listdir(src_path):
            src_item = os.path.join(src_path, item)
            dest_item = os.path.join(dest_path, item)

            if os.path.isdir(src_item):
                print(f"Creating directory: {dest_item}")
                recursive_copy(src_item, dest_item)  # Recursively copy subdirectories
            else:
                with open(src_item, 'rb') as fsrc:
                    with open(dest_item, 'wb') as fdst:
                        fdst.write(fsrc.read())
                print(f"Copied file: {src_item} -> {dest_item}")

    delete_dir(dest)
    recursive_copy(src, dest)
    print("Copy complete.")

def generate_page(from_path, template_path, dest_path): # generate HTML page from Markdown
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, 'r') as file:
        markdown = file.read()
    with open(template_path, 'r') as file:
        template = file.read()
    
    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    html = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    with open(dest_path, 'w') as file:
        file.write(html)

def generate_pages_recursive(dir_path_content="content", template_path="template.html", dest_dir_path="public"):
    # Recursively go through the content directory, generate HTML file for each Markdown and writes them to the public directory
    print(f"Generating page from {dir_path_content} to {dest_dir_path} using {template_path}")

    # Ensure destination directory aka public exists       
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path) # create directory

    # Iterate through all items in the content directory
    for item in os.listdir(dir_path_content):
        src_item = os.path.join(dir_path_content, item)
        dest_item = os.path.join(dest_dir_path, os.path.splitext(item)[0] + ".html") # Convert .md to .html

        if os.path.isdir(src_item):
            print(f"Creating directory: {dest_dir_path}")
            new_dest_dir = os.path.join(dest_dir_path, item)
            generate_pages_recursive(src_item, template_path, new_dest_dir)  # Recursively copy subdirectories
        elif src_item.endswith(".md"): # If item is Markdown file, generate HTML page
            generate_page(src_item, template_path, dest_item)
        else:
            print(f"Skipping non-Markdown file: {src_item}")

if __name__ == "__main__":
    main()