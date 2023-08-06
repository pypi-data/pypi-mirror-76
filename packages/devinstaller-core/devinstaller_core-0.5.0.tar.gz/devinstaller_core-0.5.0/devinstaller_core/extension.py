"""The Module for creating extensions
"""
from abc import ABC, abstractmethod


class BaseExt(ABC):
    """Base class for creating Abstract class for Extensions

    .. warning::
        Don't inherit this class for creating Extensions.
        This class is for creating other classes which is what you need to create
        base class for Extensions.
    """

    @property
    @abstractmethod
    def LANGUAGE_CODE(self):
        """The language code
        """

    @property
    @abstractmethod
    def LANGUAGE_NAME(self):
        """The name of the programming language
        """


class ExtCommand(BaseExt):
    """Base class for creating Extensions for running commands
    """

    @abstractmethod
    def run(self, command: str) -> None:
        """Run the given `command` in the interpretor
        """


class ExtProg(BaseExt):
    """Base class for creating Extensions for executing prog files
    """

    @abstractmethod
    def launch(self, launch: str) -> None:
        """Execute the given `launch` attribute using the prog module
        """
