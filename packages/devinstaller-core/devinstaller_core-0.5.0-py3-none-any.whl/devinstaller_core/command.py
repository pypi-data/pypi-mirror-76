# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 16:55:05 IST
# Last-Updated: Sun 16 Aug 2020 22:19:52 IST
#
# commands.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Handles all the required logic to run shell commands
#
# Copyright (c) 2020, Justin Kizhakkinedath
# All rights reserved
#
# Licensed under the terms of The MIT License
# See LICENSE file in the project root for full information.
# -----------------------------------------------------------------------------
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "software"), to deal in the software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the software, and to permit
# persons to whom the software is furnished to do so, subject to the
# following conditions:
#
# the above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind,
# express or implied, including but not limited to the warranties of
# merchantability, fitness for a particular purpose and noninfringement.
# in no event shall the authors or copyright holders be liable for any claim,
# damages or other liability, whether in an action of contract, tort or
# otherwise, arising from, out of or in connection with the software or the
# use or other dealings in the software.
# -----------------------------------------------------------------------------

"""Handles everything related to running shell commands"""
import importlib
import pkgutil
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Generic, List, TypeVar, cast

from devinstaller_core import exception as e
from devinstaller_core import extension as ex


@dataclass
class CommandResponse:
    """Response object for the `devinstaller.comands.check_cmd`

    parameters:
        prog: The language code of the programming language used
        cmd: The actual command to be run
    """

    prog: str
    cmd: str


ExtBase = TypeVar("ExtBase", bound=ex.BaseExt)


class BaseCommand(Generic[ExtBase]):
    """Base class for importing extensions
    """

    def __init__(self, extensions: List[str], ext_class: str) -> None:
        self.prog: Dict[str, ExtBase] = {}
        self.extensions = extensions
        self.ext_class = ext_class
        for finder, name, ispkg in pkgutil.iter_modules():
            if name.startswith("devinstaller_ext_"):
                self.extensions.append(name)
        for ext_path in self.extensions:
            ext = self.import_ext(ext_path, self.ext_class)
            self.prog[ext.LANGUAGE_CODE] = ext

    @classmethod
    def import_ext(cls, module_name: str, ext_class_name: str) -> ExtBase:
        """Import Extension using the name of the module and the class where it is defined

        Returns:
            Instance of the class
        """
        module = importlib.import_module(module_name)
        ext_class = getattr(module, ext_class_name)
        try:
            assert issubclass(ext_class, ex.BaseExt)
            return ext_class()
        except AssertionError:
            raise e.DevinstallerError(ext_class, "D102")


class Command(BaseCommand[ex.ExtCommand]):
    """Create a session object for running prog commands

    Create a session using this class and use the `run` method to run the commands
    """

    def __init__(self) -> None:
        ext_class = "ExtCommand"
        extensions = [
            "devinstaller_core.command_python",
            "devinstaller_core.command_shell",
        ]
        super().__init__(extensions=extensions, ext_class=ext_class)

    def run(self, command: str) -> None:
        """Run shell or python command

        Args:
            command: The full spec based command string
                Ex: `sh: echo 'Hello world'`
                    `py: print('Hello world')`
        """
        res = self.parse(command)
        lang_obj = self.prog[res.prog]
        lang_obj.run(res.cmd)

    @classmethod
    def parse(cls, command: str) -> CommandResponse:
        """Check the command and returns the command response object
        """
        try:
            pattern = r"^(.*): (.*)"
            result = re.match(pattern, command)
            assert result is not None
            data = CommandResponse(prog=result.group(1), cmd=result.group(2))
            return data
        except AssertionError:
            raise e.SpecificationError(
                error=command,
                error_code="S100",
                message="The command didn't conform to the spec",
            )


class Prog(BaseCommand[ex.ExtProg]):
    """Create a session for executing prog files
    """

    def __init__(self) -> None:
        ext_class = "ExtProg"
        extensions = ["devinstaller_core.command_python"]
        super().__init__(extensions=extensions, ext_class=ext_class)

    def launch(
        self, function_name: str, prog_file_path: str, language_code: str = "py"
    ) -> None:
        pass
