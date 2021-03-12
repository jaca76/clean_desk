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
        'noname':  'other/uncategorized',
        # audio
        '.aif':    'media/audio',
        '.cda':    'media/audio',
        '.mid':    'media/audio',
        '.midi':   'media/audio',
        '.mp3':    'media/audio',
        '.mpa':    'media/audio',
        '.ogg':    'media/audio',
        '.wav':    'media/audio',
        '.wma':    'media/audio',
        '.wpl':    'media/audio',
        '.m3u':    'media/audio',
        # text
        '.txt':    'text/text_files',
        '.doc':    'text/microsoft/word',
        '.docx':   'text/microsoft/word',
        '.odt ':   'text/text_files',
        '.pdf':    'text/pdf',
        '.rtf':    'text/text_files',
        '.tex':    'text/text_files',
        '.wks ':   'text/text_files',
        '.wps':    'text/text_files',
        '.wpd':    'text/text_files',
        # video
        '.3g2':    'media/video',
        '.3gp':    'media/video',
        '.avi':    'media/video',
        '.flv':    'media/video',
        '.h264':   'media/video',
        '.m4v':    'media/video',
        '.mkv':    'media/video',
        '.mov':    'media/video',
        '.mp4':    'media/video',
        '.mpg':    'media/video',
        '.mpeg':   'media/video',
        '.rm':     'media/video',
        '.swf':    'media/video',
        '.vob':    'media/video',
        '.wmv':    'media/video',
        # images
        '.ai':     'media/images',
        '.bmp':    'media/images',
        '.gif':    'media/images',
        '.jpg':    'media/images',
        '.jpeg':   'media/images',
        '.png':    'media/images',
        '.ps':     'media/images',
        '.psd':    'media/images',
        '.svg':    'media/images',
        '.tif':    'media/images',
        '.tiff':   'media/images',
        '.cr2':    'media/images',
        # internet
        '.asp':    'other/internet',
        '.aspx':   'other/internet',
        '.cer':    'other/internet',
        '.cfm':    'other/internet',
        '.cgi':    'other/internet',
        '.pl':     'other/internet',
        '.css':    'other/internet',
        '.htm':    'other/internet',
        '.js':     'other/internet',
        '.jsp':    'other/internet',
        '.part':   'other/internet',
        '.php':    'other/internet',
        '.rss':    'other/internet',
        '.xhtml':  'other/internet',
        '.html':   'other/internet',
        # compressed
        '.7z':     'other/compressed',
        '.arj':    'other/compressed',
        '.deb':    'other/compressed',
        '.pkg':    'other/compressed',
        '.rar':    'other/compressed',
        '.rpm':    'other/compressed',
        '.tar.gz': 'other/compressed',
        '.z':      'other/compressed',
        '.zip':    'other/compressed',
        # disc
        '.bin':    'other/disc',
        '.dmg':    'other/disc',
        '.iso':    'other/disc',
        '.toast':  'other/disc',
        '.vcd':    'other/disc',
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
        '.apk':    'other/executables',
        '.bat':    'other/executables',
        '.com':    'other/executables',
        '.exe':    'other/executables',
        '.gadget': 'other/executables',
        '.jar':    'other/executables',
        '.wsf':    'other/executables',
        # fonts
        '.fnt':    'other/fonts',
        '.fon':    'other/fonts',
        '.otf':    'other/fonts',
        '.ttf':    'other/fonts',
        # presentations
        '.key':    'text/presentations',
        '.odp':    'text/presentations',
        '.pps':    'text/presentations',
        '.ppt':    'text/presentations',
        '.pptx':   'text/presentations',
        # programming
        '.c':      'programming/c&c++',
        '.class':  'programming/java',
        '.java':   'programming/java',
        '.py':     'programming/python',
        '.sh':     'programming/shell',
        '.h':      'programming/c&c++',
        # spreadsheets
        '.ods':    'text/microsoft/excel',
        '.xlr':    'text/microsoft/excel',
        '.xls':    'text/microsoft/excel',
        '.xlsx':   'text/microsoft/excel',
        # system
        '.bak':    'text/other/system',
        '.cab':    'text/other/system',
        '.cfg':    'text/other/system',
        '.cpl':    'text/other/system',
        '.cur':    'text/other/system',
        '.dll':    'text/other/system',
        '.dmp':    'text/other/system',
        '.drv':    'text/other/system',
        '.icns':   'text/other/system',
        '.ico':    'text/other/system',
        '.ini':    'text/other/system',
        '.lnk':    'text/other/system',
        '.msi':    'text/other/system',
        '.sys':    'text/other/system',
        '.tmp':    'text/other/system'
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
    watch_path = Path.home() / 'Desktop'
    destination_root = Path.home() / 'Desktop/holder of things'
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
