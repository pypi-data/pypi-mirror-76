# -*- coding: utf-8 -*-
#
# This file is part of the tangoctl project
#
# Copyright (c) 2018-2020 Tiago Coutinho
# Distributed under the GPLv3 license. See LICENSE for more info.

import socket


def main(args=None):
    if args is None:
        import sys

        args = list(sys.argv)
    args = " ".join(args[1:])
    try:
        sock = socket.create_connection(("localhost", 10100))
    except Exception as error:
        print(error)
        return
    sock.sendall(args.encode())
    while True:
        data = sock.recv(4096)
        if not data:
            break
        print(data.decode(), end="", flush=True)


if __name__ == "__main__":
    main()
