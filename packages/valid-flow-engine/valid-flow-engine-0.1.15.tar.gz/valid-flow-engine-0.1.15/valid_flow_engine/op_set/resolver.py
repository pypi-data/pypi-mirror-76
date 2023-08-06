"""
Module for parsing JSON Dictionary to create valid flow results
"""
from __future__ import annotations
from abc import abstractmethod, ABC
import typing
import inspect


class ResolverRegistry:
    """
    Class to manage registry of ParamResolver implementations
    """
    _resolvers = {}

    @classmethod
    def register(
        cls,
        class_: typing.Type[ParamResolver]
    ) -> typing.Type[ParamResolver]:
        cls._resolvers[class_.__name__] = class_
        return class_

    @classmethod
    def get_resolver(cls, type_: str, default):
        return cls._resolvers.get(type_, default)


class ParamResolver(ABC):
    """
    Abstract class provided resolve method which will convert
    data to desired type (essentially a deserialization method)
    """

    @classmethod
    @abstractmethod
    def resolve(cls, data):
        """
        Resolve data to the desired type
        """
        pass
