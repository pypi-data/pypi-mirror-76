# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018-2020 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

import io
import os
import sys
import logging
import functools
from contextlib import redirect_stdout, redirect_stderr

import typer
import gevent.server
import gevent.socket
from .cli import cli


def handle_message(request):
    request = request.decode().strip()
    if not request:
        return
    buff = io.StringIO()
    logging.info("handle command %r", request)
    with redirect_stderr(buff), redirect_stdout(buff):
        try:
            cli(args=request.split(), standalone_mode=False)
        except SystemExit:
            pass
        except Exception as error:
            import traceback
            traceback.print_exc()
    text = buff.getvalue()
    return text.encode()


class TCPServer(gevent.server.StreamServer):
    def handle(self, client, addr):
        logging.info("new connection from %r", addr)
        request = client.recv(4096)
        if not request:
            logging.info("client %r disconnected", addr)
            client.close()
            return
        result = handle_message(request)
        if result:
            client.sendall(result)
        client.close()


class UDPServer(gevent.server.DatagramServer):
    def handle(self, request, addr):
        result = handle_message(request)
        if result:
            self.socket.sendto(result, addr)


def execute(bind: str = ":10100"):
    fmt = "%(asctime)s %(levelname)s %(name)s %(message)s"
    logging.basicConfig(level="INFO", format=fmt)
    server = TCPServer(bind)
    server.start()
    logging.info("Ready to accept requests at %r", bind)
    server.serve_forever()


def daemonize():
    import resource

    proc_id = os.fork()
    if proc_id != 0:
        exit(0)
    # Stop listening for signals that the parent process receives.
    # setsid puts the process in a new parent group and detaches its controlling terminal.
    process_id = os.setsid()
    # Close all file descriptors
    std_fd = {sys.stdin.fileno(), sys.stdout.fileno(), sys.stderr.fileno()}
    for fd in range(resource.getrlimit(resource.RLIMIT_NOFILE)[0]):
        if fd not in std_fd:
            try:
                os.close(fd)
            except OSError:
                pass
    null_fd = os.open(getattr(os, "devnull", "/dev/null"), os.O_RDWR)
    for fd in std_fd:
        os.dup2(null_fd, fd)
    os.close(null_fd)
    # Set umask to default to safe file permissions when running as a root daemon
    os.umask(0o27)
    os.chdir("/")


def run(
    bind: str = typer.Option(":10100", help="bind address for text based socket"),
    daemon: bool = typer.Option(
        True, help="run in background(daemon) / foreground(no-daemon)"
    ),
):
    """Run tangoctl server"""
    if daemon:
        daemonize()
    execute(bind=bind)


def main():
    return typer.run(run)


if __name__ == "__main__":
    main()
