#! /usr/bin/env python3

from pathlib import Path
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from collections import Counter

extension_paths = {
        # No name
        'noname':  'uncategorized',
        # audio
        '.aif':    'audio',
        '.cda':    'audio',
        '.mid':    'audio',
        '.midi':   'audio',
        '.mp3':    'audio',
        '.mpa':    'audio',
        '.ogg':    'audio',
        '.wav':    'audio',
        '.wma':    'audio',
        '.wpl':    'audio',
        '.m3u':    'audio',
        # text
        '.txt':    'text_files',
        '.doc':    'microsoft/word',
        '.docx':   'microsoft/word',
        '.odt ':   'text_files',
        '.pdf':    'pdf',
        '.rtf':    'text_files',
        '.tex':    'text_files',
        '.wks ':   'text_files',
        '.wps':    'text_files',
        '.wpd':    'text_files',
        # video
        '.3g2':    'video',
        '.3gp':    'video',
        '.avi':    'video',
        '.flv':    'video',
        '.h264':   'video',
        '.m4v':    'video',
        '.mkv':    'video',
        '.mov':    'video',
        '.mp4':    'video',
        '.mpg':    'video',
        '.mpeg':   'video',
        '.rm':     'video',
        '.swf':    'video',
        '.vob':    'video',
        '.wmv':    'video',
        # images
        '.ai':     'images',
        '.bmp':    'images',
        '.gif':    'images',
        '.jpg':    'images',
        '.jpeg':   'images',
        '.png':    'images',
        '.ps':     'images',
        '.psd':    'images',
        '.svg':    'images',
        '.tif':    'images',
        '.tiff':   'images',
        '.cr2':    'images',
        # internet
        '.asp':    'internet',
        '.aspx':   'internet',
        '.cer':    'internet',
        '.cfm':    'internet',
        '.cgi':    'internet',
        '.pl':     'internet',
        '.css':    'internet',
        '.htm':    'internet',
        '.js':     'internet',
        '.jsp':    'internet',
        '.part':   'internet',
        '.php':    'internet',
        '.rss':    'internet',
        '.xhtml':  'internet',
        '.html':   'internet',
        # compressed
        '.7z':     'compressed',
        '.arj':    'compressed',
        '.deb':    'compressed',
        '.pkg':    'compressed',
        '.rar':    'compressed',
        '.rpm':    'compressed',
        '.tar.gz': 'compressed',
        '.z':      'compressed',
        '.zip':    'compressed',
        # disc
        '.bin':    'disc',
        '.dmg':    'disc',
        '.iso':    'disc',
        '.toast':  'disc',
        '.vcd':    'disc',
        # data
        '.csv':    'programming/database',
        '.dat':    'programming/database',
        '.db':     'programming/database',
        '.dbf':    'programming/database',
        '.log':    'programming/database',
        '.mdb':    'programming/database',
        '.sav':    'programming/database',
        '.sql':    'programming/database',
        '.tar':    'programming/database',
        '.xml':    'programming/database',
        '.json':   'programming/database',
        # executables
        '.apk':    'executables',
        '.bat':    'executables',
        '.com':    'executables',
        '.exe':    'executables',
        '.gadget': 'executables',
        '.jar':    'executables',
        '.wsf':    'executables',
        # fonts
        '.fnt':    'fonts',
        '.fon':    'fonts',
        '.otf':    'fonts',
        '.ttf':    'fonts',
        # presentations
        '.key':    'presentations',
        '.odp':    'presentations',
        '.pps':    'presentations',
        '.ppt':    'presentations',
        '.pptx':   'presentations',
        # programming
        '.c':      'programming/c&c++',
        '.class':  'programming/java',
        '.java':   'programming/java',
        '.py':     'programming/python',
        '.sh':     'programming/shell',
        '.h':      'programming/c&c++',
        # spreadsheets
        '.ods':    'excel',
        '.xlr':    'excel',
        '.xls':    'excel',
        '.xlsx':   'excel',
        # system
        '.bak':    'system',
        '.cab':    'system',
        '.cfg':    'system',
        '.cpl':    'system',
        '.cur':    'system',
        '.dll':    'system',
        '.dmp':    'system',
        '.drv':    'system',
        '.icns':   'system',
        '.ico':    'system',
        '.ini':    'system',
        '.lnk':    'system',
        '.msi':    'system',
        '.sys':    'system',
        '.tmp':    'system',
        # cad
        '.stl':     'stl'
        }


def analyze_folder_content(folder_path: Path):
    """
    Analyze the content of a folder and determine the most common file type category.
    
    :param Path folder_path: path to the folder to analyze
    :return: category name based on most common file types in the folder
    """
    if not folder_path.is_dir():
        return None
    
    categories = []
    
    # Recursively scan all files in the folder
    for file_path in folder_path.rglob('*'):
        if file_path.is_file():
            file_extension = file_path.suffix.lower()
            if file_extension in extension_paths:
                categories.append(extension_paths[file_extension])
            else:
                categories.append('uncategorized')
    
    if not categories:
        return 'empty_folders'
    
    # Find the most common category
    category_count = Counter(categories)
    most_common_category = category_count.most_common(1)[0][0]
    
    return most_common_category


def rename_file(source: Path, destination_path: Path):
    """
    Helper function that renames file to reflect new path. If a file of the same
    name already exists in the destination folder, the file name is numbered and
    incremented until the filename is unique (prevents overwriting files).

    :param Path source: source of file to be moved
    :param Path destination_path: path to destination directory
    """
    if Path(destination_path / source.name).exists():
        increment = 0

        while True:
            increment += 1
            new_name = destination_path / f'{source.stem}_{increment}{source.suffix}'

            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name


def move_item(source: Path, destination_root: Path, category: str):
    """
    Move a file or folder to the appropriate category directory.
    
    :param Path source: source file or folder to be moved
    :param Path destination_root: root destination directory
    :param str category: category subdirectory name
    """
    destination_path = destination_root / category
    destination_path.mkdir(parents=True, exist_ok=True)
    
    final_destination = rename_file(source=source, destination_path=destination_path)
    shutil.move(src=source, dst=final_destination)
    print(f"Moved {source.name} to {category}")


class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        for child in self.watch_path.iterdir():
            # Skip the destination folder to avoid moving it
            if child.resolve() == self.destination_root:
                continue
                
            if child.is_file():
                # Handle files
                file_extension = child.suffix.lower()
                if file_extension in extension_paths:
                    category = extension_paths[file_extension]
                else:
                    category = 'uncategorized'
                
                move_item(child, self.destination_root, category)
                
            elif child.is_dir():
                # Handle folders based on their content
                category = analyze_folder_content(child)
                if category:
                    move_item(child, self.destination_root, category)


def select_folder():
    """
    Interactive function to select the folder to watch and organize.
    
    :return: tuple of (watch_path, destination_root)
    """
    print("File Organizer - Folder Selection")
    print("=" * 40)
    
    # Select folder to watch
    while True:
        print("\nSelect the folder you want to organize:")
        print("1. Downloads folder (default)")
        print("2. Desktop")
        print("3. Documents")
        print("4. Custom path")
        
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1' or choice == '':
            watch_path = Path.home() / 'Downloads'
            break
        elif choice == '2':
            watch_path = Path.home() / 'Desktop'
            break
        elif choice == '3':
            watch_path = Path.home() / 'Documents'
            break
        elif choice == '4':
            custom_path = input("Enter the full path to the folder: ").strip()
            watch_path = Path(custom_path)
            if not watch_path.exists():
                print(f"Error: Path '{custom_path}' does not exist. Please try again.")
                continue
            if not watch_path.is_dir():
                print(f"Error: '{custom_path}' is not a directory. Please try again.")
                continue
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")
            continue
    
    # Select destination folder
    print(f"\nSelected folder to organize: {watch_path}")
    print("\nWhere should organized files be moved?")
    print("1. Create 'organized' subfolder in the selected folder (default)")
    print("2. Custom destination path")
    
    while True:
        dest_choice = input("Enter your choice (1-2): ").strip()
        
        if dest_choice == '1' or dest_choice == '':
            destination_root = watch_path / 'organized'
            break
        elif dest_choice == '2':
            custom_dest = input("Enter the full path for organized files: ").strip()
            destination_root = Path(custom_dest)
            
            # Check if the destination is inside the watch folder
            try:
                destination_root.resolve().relative_to(watch_path.resolve())
                print("Note: Destination is inside the watch folder - this is fine.")
            except ValueError:
                print("Note: Destination is outside the watch folder.")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")
            continue
    
    return watch_path, destination_root


def organize_existing_files(watch_path: Path, destination_root: Path):
    """
    Organize files that already exist in the watch folder.
    
    :param Path watch_path: folder to scan for existing files
    :param Path destination_root: destination for organized files
    """
    print(f"\nScanning existing files in {watch_path}...")
    
    items_to_organize = []
    
    for child in watch_path.iterdir():
        # Skip the destination folder to avoid moving it
        if child.resolve() == destination_root.resolve():
            continue
        items_to_organize.append(child)
    
    if not items_to_organize:
        print("No files or folders found to organize.")
        return
    
    print(f"Found {len(items_to_organize)} items to organize.")
    
    organize_now = input("Do you want to organize existing files now? (y/n): ").strip().lower()
    
    if organize_now in ['y', 'yes']:
        print("Organizing existing files...")
        
        for child in items_to_organize:
            if child.is_file():
                # Handle files
                file_extension = child.suffix.lower()
                if file_extension in extension_paths:
                    category = extension_paths[file_extension]
                else:
                    category = 'uncategorized'
                
                move_item(child, destination_root, category)
                
            elif child.is_dir():
                # Handle folders based on their content
                category = analyze_folder_content(child)
                if category:
                    move_item(child, destination_root, category)
        
        print("Finished organizing existing files!")
    else:
        print("Skipping existing files. Only new files will be organized.")


if __name__ == '__main__':
    # Select folders interactively
    watch_path, destination_root = select_folder()
    
    # Ensure destination directory exists
    destination_root.mkdir(parents=True, exist_ok=True)
    
    # Ask about organizing existing files
    organize_existing_files(watch_path, destination_root)
    
    # Start watching for new files
    event_handler = EventHandler(watch_path=watch_path, destination_root=destination_root)

    observer = Observer()
    observer.schedule(event_handler, f'{watch_path}', recursive=False)
    observer.start()

    print(f"\nFile organizer started!")
    print(f"Watching: {watch_path}")
    print(f"Organizing files to: {destination_root}")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        observer.stop()
        print("\nFile organizer stopped.")
    observer.join()
