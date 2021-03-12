#! /usr/bin/env python3

from pathlib import Path
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil
from datetime import date
from pathlib import Path
#test

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
        '.tmp':    'system'
        # cad
        '.stl':     'stl'
        }


def add_date_to_path(path: Path):
    """
    Helper function that adds current year/month to destination path. If the path
    doesn't already exist, it is created.

    :param Path path: destination root to append subdirectories based on date
    """
    dated_path = path / f'{date.today().year}' 
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path


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


class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

    def on_modified(self, event):
        for child in self.watch_path.iterdir():
            # skips directories and non-specified extensions
            if child.is_file() and child.suffix.lower() in extension_paths:
                destination_path = self.destination_root / extension_paths[child.suffix.lower()]
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)

if __name__ == '__main__':
    watch_path = Path.home() / 'Downloads'
    destination_root = Path.home() / 'Downloads/holder of things'
    event_handler = EventHandler(watch_path=watch_path, destination_root=destination_root)

    observer = Observer()
    observer.schedule(event_handler, f'{watch_path}', recursive=True)
    observer.start()

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
