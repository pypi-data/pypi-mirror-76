# Copyright 2020 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft

from datetime import date
import logging
import os
from pathlib import Path
import pwd
import re

from jinja2 import Environment, PackageLoader, StrictUndefined

from charmcraft.cmdbase import BaseCommand, CommandError
from .utils import make_executable

logger = logging.getLogger(__name__)


class InitCommand(BaseCommand):
    """Initialize a directory to be a charm project."""
    name = "init"
    help_msg = "initialize a directory to be a charm project"

    def fill_parser(self, parser):
        parser.add_argument(
            "--project-dir", type=Path, default=Path("."), metavar="DIR", dest="path",
            help="the directory to initialize. Must be empty, or not exist; defaults to '.'")
        parser.add_argument(
            "--name", type=str,
            help="the name of the project; defaults to the directory name")
        parser.add_argument(
            "--author", type=str,
            help="the author of the project;"
            " defaults to the current user's name as present in the GECOS field.")

    def run(self, args):
        args.path = args.path.resolve()
        if args.path.exists():
            if not args.path.is_dir():
                raise CommandError("{} is not a directory".format(args.path))
            if next(args.path.iterdir(), False):
                raise CommandError("{} is not empty".format(args.path))
            logger.debug("Using existing project directory '%s'", args.path)
        else:
            logger.debug("Creating project directory '%s'", args.path)
            args.path.mkdir()

        if args.author is None:
            gecos = pwd.getpwuid(os.getuid()).pw_gecos.split(',', 1)[0]
            if not gecos:
                raise CommandError("Author not given, and nothing in GECOS field")
            logger.debug("Setting author to %r from GECOS field", gecos)
            args.author = gecos

        if not args.name:
            args.name = args.path.name
            logger.debug("Set project name to '%s'", args.name)

        if not re.match(r"[a-z][a-z0-9-]*[a-z0-9]$", args.name):
            raise CommandError("{} is not a valid charm name".format(args.name))

        context = {
            "name": args.name,
            "author": args.author,
            "year": date.today().year,
            "class_name": "".join(re.split(r"\W+", args.name.title())) + "Charm",
        }

        env = Environment(
            loader=PackageLoader('charmcraft', 'templates/init'),
            autoescape=False,            # no need to escape things here :-)
            keep_trailing_newline=True,  # they're not text files if they don't end in newline!
            optimized=False,             # optimization doesn't make sense for one-offs
            undefined=StrictUndefined)   # fail on undefined

        _todo_rx = re.compile("TODO: (.*)")
        todos = []
        executables = ["run_tests", "src/charm.py"]
        for template_name in env.list_templates():
            if not template_name.endswith(".j2"):
                continue
            template = env.get_template(template_name)
            template_name = template_name[:-3]
            logger.debug("Rendering %s", template_name)
            path = args.path / template_name
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("wt", encoding="utf8") as fh:
                out = template.render(context)
                fh.write(out)
                for todo in _todo_rx.findall(out):
                    todos.append((template_name, todo))
                if template_name in executables:
                    make_executable(fh)
                    logger.debug("  made executable")
        logger.info("All done.")
        if todos:
            logger.info("There are some notes about things we think you should do.")
            logger.info("These are marked with ‘TODO:’, as is customary. Namely:")
            w = max(len(i[0]) for i in todos)
            for fn, todo in todos:
                logger.info("%*s: %s", w + 2, fn, todo)
