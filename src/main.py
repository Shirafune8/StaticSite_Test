import os

def main():
    copy_source_static_to_destination_public_directory()

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

if __name__ == "__main__":
    main()