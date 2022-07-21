from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Union, Tuple


# class Pixels:
#     def __init__(self, value: Union[int, float]):
#         self.value = value
# 
#     def __str__(self):
#         return f'{round(self.value, 4)}px'
# 
#     def __repr__(self):
#         return f'Pixels({self.value})'
# 
#     def __sub__(self, other) -> Pixels:
#         if isinstance(other, Pixels):
#             return Pixels(self.value - other.value)
#         elif isinstance(other, (float, int)):
#             return Pixels(self.value - other)
#         else:
#             raise ValueError(f"Can't subtract object of type {type(other)} from Pixels object.")
# 
#     def __add__(self, other) -> Pixels:
#         if isinstance(other, Pixels):
#             return Pixels(self.value + other.value)
#         elif isinstance(other, (float, int)):
#             return Pixels(self.value + other)
#         else:
#             raise ValueError(f"Can't add object of type {type(other)} to Pixels object.")
# 
#     def __mul__(self, other) -> Pixels:
#         if isinstance(other, Pixels):
#             return Pixels(self.value * other.value)
#         elif isinstance(other, (float, int)):
#             return Pixels(self.value * other)
#         else:
#             raise ValueError(f"Can't multiply object of type {type(other)} with Pixels object.")
# 
#     def __truediv__(self, other) -> Pixels:
#         if isinstance(other, Pixels):
#             return Pixels(self.value / other.value)
#         elif isinstance(other, (float, int)):
#             return Pixels(self.value / other)
#         else:
#             raise ValueError(f"Can't divide Pixels object by object of type {type(other)}.")
# 
#     def __lt__(self, other):
#         if isinstance(other, Pixels):
#             return self.value < other.value
#         elif isinstance(other, (float, int)):
#             return self.value < other
#         else:
#             raise ValueError(f"Can't divide Pixels object by object of type {type(other)}.")


class HTML(ABC):
    @abstractmethod
    def css_style(self):
        pass

    @abstractmethod
    def inner_html(self):
        pass


class DIV(HTML):
    def css_style(self):
        pass

    def inner_html(self):
        pass


class Coordinates():
    xshift: float = None
    yshift: float = None

    def __init__(self, xy: Union[Tuple[float, float], Tuple[Pixels, Pixels]]):
        pass
