from __future__ import print_function

import argparse
import contextlib
import datetime
import os
import six
import sys
import time
import unicodedata
import socket

if sys.version.startswith('2'):
    input = raw_input  # noqa: E501,F821; pylint: disable=redefined-builtin,undefined-variable,useless-suppression

import dropbox

# OAuth2 access token.  TODO: login etc.
TOKEN = 'QS78pqL8MhUAAAAAAAAAAQ1aJ6MwxmA392jrpui_eNs1_P7PZZSVE_EMOQvb6ujS'

parser = argparse.ArgumentParser(description='Sync ~\Downloads to Dropbox')
parser.add_argument('folder', nargs='?', default='Downloads', help='Folder name in your Dropbox')
parser.add_argument('rootdir', nargs='?', default='~\Downloads', help='Local directory to upload')
parser.add_argument('--token', default=TOKEN, help='Access token' '(see https://www.dropbox.com/developers/apps)')
parser.add_argument('--yes', '-y', action='store_true', help='Answer yes to all questions')
parser.add_argument('--no', '-n', action='store_true', help='Answer no to all questions')
parser.add_argument('--default', '-d', action='store_true', help='Take default answer on all questions')

def main():
    """Main program.
    Parse command line, then iterate over files and directories under
    rootdir and upload all files.  Skips some temporary files and
    directories, and avoids duplicate uploads by comparing size and
    mtime with the server.
    """
    args = parser.parse_args()
    if sum([bool(b) for b in (args.yes, args.no, args.default)]) > 1:
        print('At most one of --yes, --no, --default is allowed')
        sys.exit(2)
    if not args.token:
        print('--token is mandatory')
        sys.exit(2)

    folder = args.folder
    rootdir = os.path.expanduser(args.rootdir)
    print('Dropbox folder name:', folder)
    print('Local directory:', rootdir)
    if not os.path.exists(rootdir):
        print(rootdir, 'does not exist on your filesystem')
        sys.exit(1)
    elif not os.path.isdir(rootdir):
        print(rootdir, 'is not a folder on your filesystem')
        sys.exit(1)

    dbx = dropbox.Dropbox(args.token)

    download(dbx, "Apps", "Contract Drafter", "2.amr")

    dbx.close()

def list_folder(dbx, folder, subfolder):
    """List a folder.
    Return a dict mapping unicode filenames to
    FileMetadata|FolderMetadata entries.
    """
    path = '/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'))
    while '//' in path:
        path = path.replace('//', '/')
    path = path.rstrip('/')
    try:
        with stopwatch('list_folder'):
            res = dbx.files_list_folder(path)
    except dropbox.exceptions.ApiError as err:
        print('Folder listing failed for', path, '-- assumed empty:', err)
        return {}
    else:
        rv = {}
        for entry in res.entries:
            rv[entry.name] = entry
        return rv

def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % ("Apps", "Contract Drafter", "2.amr")
    while '//' in path:
        path = path.replace('//', '/')
    with stopwatch('download'):
        try:
            md, res = dbx.files_download(path)
        except dropbox.exceptions.HttpError as err:
            print('*** HTTP error', err)
            return None
    data = res.content
    print(data, 'bytes; md:', md)
    return data

@contextlib.contextmanager
def stopwatch(message):
    """Context manager to print how long a block of code took."""
    t0 = time.time()
    try:
        yield
    finally:
        t1 = time.time()
        print('Total elapsed time for %s: %.3f' % (message, t1 - t0))

def listen():
	s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	s.bind((socket.gethostname(),1234))
	s.listen(5)

	while True:
		clientsocket, address = s.accept()
		s.send(bytes("Welcome to server!","utf-8"))

if __name__ == '__main__':
    main()
    listen()