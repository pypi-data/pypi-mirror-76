# -*- coding: utf-8 -*-
import os, sys, zipfile, importlib, signal
from subprocess import Popen
import argparse
import sqlite3

from . import __path__
from .handlers import CliException

def main():
    """Console script for pyvuejs_cli."""
    parser = argparse.ArgumentParser()
    parser.add_argument("job", help = "cli command")
    parser.add_argument("--name", default = "pyvuejs_project", help = "name of project to create")

    args = vars(parser.parse_args())

    if args["job"] == "create-project":
        template_zip = zipfile.ZipFile(os.path.join(__path__[0], "project_template.zip"), "r")
        template_zip.extractall(os.path.join(os.getcwd(), args["name"]))
    elif args["job"] == "start":
        con = sqlite3.connect(os.path.join(os.getcwd(), ".state"))

        if con.execute("select count(*) from `server`;").fetchone()[0] > 0:
            already_port = con.execute("select `port` from `server`;").fetchone()[0]
            raise CliException(f"Server started on {already_port}")

        server_pid = Popen([sys.executable, os.path.join(os.getcwd(), "main.py")]).pid
        con.execute(f"insert into `server` values ({server_pid})")
        con.commit()
        con.close()

    elif args["job"] == "stop":
        con = sqlite3.connect(os.path.join(os.getcwd(), ".state"))

        if con.execute("select count(*) from `server`;").fetchone()[0] == 0:
            raise CliException("Server is not started!")

        server_pid = con.execute("select `pid` from `server`;").fetchone()[0]
        os.kill(server_pid, signal.SIGTERM)

        con.execute("delete from `server`;")
        con.commit()
        con.close()

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
