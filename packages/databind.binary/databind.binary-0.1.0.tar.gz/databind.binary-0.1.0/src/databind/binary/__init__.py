
__author__ = 'Niklas Rosenstein <rosensteinniklas@gmail.com>'
__version__ = '0.1.0'

import io
import struct
from typing import Type, T
from databind.core import Context, Registry
from ._converters import BufferedBinaryStream, register_binary_converters
from ._types import *

__all__ = [
  'register_binary_converters',
  'registry',
  'from_bytes',
  'to_bytes',
] + _types.__all__


registry = Registry(None)
register_binary_converters(registry)


def from_bytes(type_: Type[T], data: bytes, registry: Registry=None) -> T:
  stream = BufferedBinaryStream(io.BytesIO(data))
  return Context.new(registry or globals()['registry'], type_, stream).to_python()


def to_bytes(value: T, type_: Type[T]=None, registry: Registry=None) -> bytes:
  type_ = type_ or type(value)
  return Context.new(registry or globals()['registry'], type_, value).from_python()


def calc_size(type_: Type[T], registry: Registry=None) -> int:
  context = Context.new(registry or globals()['registry'], type_, None)
  format_parts, _ = zip(*context.get_converter().get_format_parts(context))
  return struct.calcsize(''.join(format_parts))
