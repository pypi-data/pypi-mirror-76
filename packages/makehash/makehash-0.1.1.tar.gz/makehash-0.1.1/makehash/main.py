# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

from typing import *
import os
import sys
import traceback

import click
from click_anno import click_app
from click_anno.types import flag
from fsoopify import NodeInfo, NodeType, FileInfo, DirectoryInfo
from alive_progress import alive_bar
from alive_progress.core.utils import clear_traces

EXTENSION_NAME = '.hash'
ACCEPT_HASH_TYPES = ('sha1', 'md5')

def get_checksum_file(f: FileInfo) -> FileInfo:
    return FileInfo(f.path + EXTENSION_NAME)

def get_hash_value(f: FileInfo, hash_type: str):
    with f.get_hasher(hash_type) as hasher:
        with alive_bar(manual=True) as bar:
            while hasher.read_block():
                bar(hasher.progress)
        return hasher.result[0]

def verify_file(f: FileInfo):
    hash_file = get_checksum_file(f)
    if not hash_file.is_file():
        if f.path.name.ext != EXTENSION_NAME:
            click.echo('Ignore {} by checksum file not found.'.format(
                click.style(str(f.path), fg='blue')
            ))
        return

    data = hash_file.load('json')

    # find hash type:
    for hash_type in ACCEPT_HASH_TYPES:
        if hash_type in data:
            break
    else:
        hash_type = None

    if not hash_type:
        click.echo('Ignore {} by no known algorithms in checksum file.'.format(
            click.style(str(f.path), fg='blue')
        ))
        return

    hash_value = data[hash_type]
    click.echo('Verifing {}... '.format(
        click.style(str(f.path), fg='blue')
    ))
    real_hash_value = get_hash_value(f, hash_type)
    click.echo('Result : ', nl=False)
    if real_hash_value == hash_value:
        click.echo(click.style("Ok", fg="green") + '.')
    else:
        click.echo(click.style("Failed", fg="red") + '!')

def create_checksum_file(f: FileInfo, skip_exists: bool):
    hash_file = get_checksum_file(f)

    if skip_exists and hash_file.is_file():
        click.echo('Skiped {} by checksum file exists.'.format(
            click.style(str(f.path), fg='bright_blue')
        ), nl=True)
        return

    hash_type = ACCEPT_HASH_TYPES[0]
    click.echo('Computing checksum for {}...'.format(
            click.style(str(f.path), fg='bright_blue')
        ), nl=True)

    hash_value = get_hash_value(f, hash_type)
    data = {}
    data[hash_type] = hash_value
    hash_file.dump(data, 'json')

@click_app
class App:
    def _collected_files(self, paths: list, skip_hash_file: bool) -> List[FileInfo]:
        collected_files: List[FileInfo] = []

        def collect_from_dir(d: DirectoryInfo):
            for item in d.list_items():
                if item.node_type == NodeType.file:
                    collected_files.append(item)
                elif item.node_type == NodeType.dir:
                    collect_from_dir(item)

        if paths:
            for path in paths:
                node = NodeInfo.from_path(path)
                if node is not None:
                    if node.node_type == NodeType.file:
                        collected_files.append(item)
                    elif node.node_type == NodeType.dir:
                        collect_from_dir(node)
                else:
                    click.echo(f'Ignore {path} which is not a file or dir')

            # ignore *.hash file
            if skip_hash_file:
                collected_files = [f for f in collected_files if f.path.name.ext != EXTENSION_NAME]

            if collected_files:
                click.echo('Found {} files.'.format(
                    click.style(str(len(collected_files)), fg='bright_blue')
                ))
            else:
                click.echo(click.style("Path is required", fg="yellow"))
        else:
            click.echo(click.style("Path is required", fg="red"))

        return collected_files

    def make(self, *paths, skip_exists: flag=True, skip_hash_file: flag=True):
        'create *.hash files'
        collected_files = self._collected_files(paths, skip_hash_file)
        if collected_files:
            for f in collected_files:
                create_checksum_file(f, skip_exists=skip_exists)

    def verify(self, *paths, skip_hash_file: flag=True):
        'verify with *.hash files'
        collected_files = self._collected_files(paths, skip_hash_file)
        if collected_files:
            for f in collected_files:
                verify_file(f)


def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        App()(argv[1:])
    except Exception: # pylint: disable=W0703
        traceback.print_exc()

if __name__ == '__main__':
    main()
