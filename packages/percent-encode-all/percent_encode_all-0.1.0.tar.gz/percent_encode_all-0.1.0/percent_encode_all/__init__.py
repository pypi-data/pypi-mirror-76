"""percent_encode_all - Encode every charactor into percent format."""

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__ = []


def percent_encode(s, encoding="ascii"):
    return "".join(["%{:0>2x}".format(b) for b in s.encode(encoding)])
