# -*- coding: utf-8 -*-
from argparse import ArgumentParser, _ArgumentGroup, Namespace
from abc import ABC, abstractmethod


class AbstractParser(ABC):
    def __init__(self, *args, **kwargs):
        self.__parser: ArgumentParser = ArgumentParser(*args, **kwargs)
        self._required_arguments(group=self.__required_argument_group)
        self._optional_arguments()

    @abstractmethod
    def _optional_arguments(self) -> None:
        ...

    @abstractmethod
    def _required_arguments(self, group: _ArgumentGroup) -> None:
        ...

    @property
    def __required_argument_group(self) -> _ArgumentGroup:
        return self.parser.add_argument_group(title="required arguments")

    @property
    def parser(self) -> ArgumentParser:
        return self.__parser

    @property
    def args(self) -> Namespace:
        return self.parser.parse_args()
