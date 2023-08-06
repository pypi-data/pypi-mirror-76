# -----------------------------------------------------------------------------
# Created: Mon 25 May 2020 15:40:37 IST
# Last-Updated: Sun 16 Aug 2020 16:55:06 IST
#
# file_handler.py is part of devinstaller
# URL: https://gitlab.com/justinekizhak/devinstaller
# Description: Handles everything file related
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

"""Handles everything file_handler"""
import hashlib
import os
import re
from dataclasses import dataclass
from typing import Any, Callable, Dict

import anymarkup
import requests
from typeguard import typechecked

from devinstaller_core import exception as e


@dataclass
class FileResponse:
    """Response object for the `devinstaller_core.file_handler.get_data`
    """

    digest: str
    contents: str


@dataclass
class PathResponse:
    """Response object for the `devinstaller_core.file_handler.check_path`
    """

    method: str
    path: str


class DevFile:
    @typechecked
    def parse_contents(
        self, file_contents: str, file_format: str = "toml"
    ) -> Dict[Any, Any]:
        """Parse `file_contents` and returns the python object

        Args:
            file_contents: The contents of file

        Returns:
            Python object

        Raises:
            SpecificationError
                with code :ref:`error-code-S100`
        """
        try:
            return anymarkup.parse(file_contents, format=file_format)
        except Exception:
            raise e.SpecificationError(
                error=file_contents,
                error_code="S100",
                message="There is some error in your file content",
            )

    @typechecked
    def read_file(self, file_path: str) -> str:
        """Reads the file at the path and returns the string representation

        Args:
            file_path: The path to the file

        Returns:
            String representation of the file
        """
        # TODO check if the path is starting with dot or two dots
        full_path = os.path.expanduser(file_path)
        with open(full_path, "r") as _f:
            return _f.read()

    @typechecked
    def read_file_and_parse(self, file_path: str) -> Dict[Any, Any]:
        """Reads the file at path and parse and returns the python object

        It is composed of `read_file` and `parse_contents`

        Args:
            file_path: The path to the file

        Returns:
            Python object
        """
        file_format = file_path.split(".")[-1]
        return self.parse_contents(self.read_file(file_path), file_format=file_format)

    @typechecked
    def download_url(self, url: str) -> str:
        """Downloads file from the internet

        Args:
            url: Url of the file

        Returns:
            String representation of file
        """
        response = requests.get(url)
        return response.content.decode("utf-8")

    @typechecked
    def write_file(self, file_content: str, file_path: str) -> None:
        """Downloads file from the internet and saves to file
        """
        with open(file_path, "w") as f:
            f.write(file_content)

    @typechecked
    def get_data(self, file_path: str) -> FileResponse:
        """Checks the input_str and downloads or reads the file.

        Methods:
            url:
                downloads the file
            file:
                reads the file
            data:
                returns the data as is

        Steps:
            1. Extract the method
            2. Use the method to get the file
            3. hash the contents and returns the response object

        Args:
            file_path: path to file. Follows the spec format

        Returns:
            Response object with digest and its contents

        Raises:
            SpecificationError
                with error code :ref:`error-code-S101`
        """
        method = self.check_path(file_path).method
        function: Dict[str, Callable[[str], str]] = {
            "file": self.read_file,
            "url": self.download_url,
            "data": lambda x: x,
        }
        file_contents = function[method](file_path)
        data = FileResponse(
            digest=self.hash_data(str(file_contents)), contents=file_contents
        )
        return data

    @typechecked
    def hash_data(self, input_data: str) -> str:
        """Hashes the input string and returns its digest
        """
        return hashlib.sha256(input_data.encode("utf-8")).hexdigest()

    @typechecked
    def check_path(self, file_path: str) -> PathResponse:
        """Check if the given path is adhearing to the spec

        Args:
            file_path: The file path according to the spec

        Returns:
            the spec object
        """
        try:
            pattern = r"^(url|file|data): (.*)"
            result = re.match(pattern, file_path)
            assert result is not None
            data = PathResponse(method=result.group(1), path=result.group(2))
            return data
        except AssertionError:
            raise e.SpecificationError(
                error=file_path,
                error_code="S101",
                message="The file_path you gave didn't start with a method.",
            )
