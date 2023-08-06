#!/usr/bin/env python3

import tempfile
import os
import re
import pytest
import pexpect
import logging 
from queue import Queue, Empty

from uboot import setup_uboot, UBoot, PROMPT, PROMPT_RE, PROMPT_RE_END, ENDL

logger = logging.getLogger(__name__)

@pytest.fixture
def uboot_process():
    basedir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'tmp')
    uboot_executable = os.path.join(basedir, 'u-boot')
    if not os.path.exists(uboot_executable):
        prefix = os.path.join(basedir, 'uboot-')
        tempdir = tempfile.mkdtemp(prefix=prefix)
        setup_uboot(tempdir, uboot_executable)
    date = 'now' # TODO
    logfile_path = os.path.join(basedir, 'uboot-{}.log'.format(date))
    proc = UBoot(uboot_executable, logfile_path)
    proc.search_output([re.compile(b'Hit any key to stop autoboot:')])
    proc.send_line(b'')
    return proc

def test_bind(uboot_process):
    up = uboot_process
    up.search_output([PROMPT_RE_END])
    # Bind to the image
    up.send_line(b'host bind 0 ../examples/baz.img')
    up.search_output([PROMPT_RE_END])
    _compare_directory_with_partition(up, '', '../examples/bar.img', 1)
        

def _compare_directory_with_partition(up, source_dir, dest_image,
                                      dest_partition,
                                      ignore_list=('lost+found',)):
    up.send_line(b'host bind 0 ' + dest_image.encode('ascii'))
    up.search_output([PROMPT_RE_END])
    match_list = [
        re.compile(ENDL + PROMPT + b'$'),
        re.compile(ENDL + rb'[ ]+\.{1,2}/'),
        re.compile(ENDL + rb'[ ]+([^/]+)/'),
        re.compile(ENDL + rb'[ ]+([0-9])+[ ]+([^/]+)'),
        re.compile(ENDL + rb'[0-9]+ file(s), [0-9]+ dir(s)'),
        re.compile(ENDL + rb'*[^\n]+\*\*'),
        re.compile(ENDL + rb'\*\*[^\n]+\*\*'),
    ]

    # Släng ut pexpect, läs per rad istället, om det går..

    queue = Queue()
    queue.put('/')
    directories = []
    files = []
    class QueueIter():
        def __iter__(self):
            return self
        def __next__(self):
            try:
                return queue.get_nowait()
            except Empty:
                raise StopIteration
    for directory in iter(QueueIter()):
        up.send_line(b'ls host 0: ' + str(dest_partition).encode('ascii') + \
            b' ' + directory.encode('ascii'))
        while True:
            num, mobj, _skipped, matched = up.match_output(match_list)
            logger.debug('Match no %d: %s', num, matched)
            if num == 0: # Prompt
                break
            elif num == 1: # . or ..
                continue
            elif num == 2: # Directory
                logger.info('dir: {}'.format(mobj))
            elif num == 3: # File
                logger.info('file: {}'.format(mobj))
            elif num == 4: # summary
                pass
            elif num == 5: # . or ..
                continue
            elif num == 6: # Error
                return False, matched
        logger.error(directory)
    up.communicate()
