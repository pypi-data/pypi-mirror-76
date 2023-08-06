#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
python系统内的异常
 +-- Exception
      +-- StopIteration
      +-- StopAsyncIteration
      +-- ArithmeticError
      |    +-- FloatingPointError
      |    +-- OverflowError
      |    +-- ZeroDivisionError
      +-- AssertionError
      +-- AttributeError
      +-- BufferError
      +-- EOFError
      +-- ImportError
      |    +-- ModuleNotFoundError
      +-- LookupError
      |    +-- IndexError
      |    +-- KeyError
      +-- MemoryError
      +-- NameError
      |    +-- UnboundLocalError
      +-- OSError
      |    +-- BlockingIOError
      |    +-- ChildProcessError
      |    +-- ConnectionError
      |    |    +-- BrokenPipeError
      |    |    +-- ConnectionAbortedError
      |    |    +-- ConnectionRefusedError
      |    |    +-- ConnectionResetError
      |    +-- FileExistsError
      |    +-- FileNotFoundError
      |    +-- InterruptedError
      |    +-- IsADirectoryError
      |    +-- NotADirectoryError
      |    +-- PermissionError
      |    +-- ProcessLookupError
      |    +-- TimeoutError
      +-- ReferenceError
      +-- RuntimeError
      |    +-- NotImplementedError
      |    +-- RecursionError
      +-- SyntaxError
      |    +-- IndentationError
      |         +-- TabError
      +-- SystemError
      +-- TypeError
      +-- ValueError
      |    +-- UnicodeError
      |         +-- UnicodeDecodeError
      |         +-- UnicodeEncodeError
      |         +-- UnicodeTranslateError
      +-- Warning
           +-- DeprecationWarning
           +-- PendingDeprecationWarning
           +-- RuntimeWarning
           +-- SyntaxWarning
           +-- UserWarning
           +-- FutureWarning
           +-- ImportWarning
           +-- UnicodeWarning
           +-- BytesWarning
           +-- ResourceWarning
"""


class ConfigFileNotFoundError(FileNotFoundError):
    """
    配置文件没有找到
    """


class RequireArgumentError(Exception):
    """
    需要某个参数但是没有提供
    """


class FatalError():
    """Fatal Error, the program need shutdown imediately"""


class NotIntegerError(ValueError):
    """Need input is a integer"""


class NotFloatError(ValueError):
    """Need input is a float"""


class OutOfRangeError(ValueError):
    """The input required a range"""


class NotSupportedWarning(UserWarning):
    """This feature is not supported, program will ignore it."""


class UnDefinedError():
    """UndefinedError, lately we will talk about it. """


class CyclicError(Exception):
    pass


class GraphError(RuntimeError):
    """
    A base-class for the various kinds of errors that occur in the the python-graph class.
    """
    pass


class AdditionError(GraphError):
    """
    This error is raised when trying to add a node or edge already added to the graph or digraph.
    """
    pass


class GuessFailed(Warning):
    """
    某些猜测性试探性函数失败抛出异常
    """
