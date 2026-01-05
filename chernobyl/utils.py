from typing import Optional, List, Tuple

import numpy as np

from chernobyl import V2D


class Fixer:
    @staticmethod
    def vector(vector: Optional[V2D] = None, randomize: bool = True) -> V2D:
        if vector is None:
            if randomize:
                return V2D.random()
            return V2D()

        return vector

    @staticmethod
    def colors(n: int = 20) -> List[Tuple[int, int, int]]:
        colors = []
        for i in range(n):
            r = int((i / (n - 1)) * 255)
            g = 0
            b = int((1 - i / (n - 1)) * 255)
            colors.append((r, g, b))
        return colors

    @classmethod
    def fps(cls, value: Optional[int] = None) -> float:
        if value is None:
            return 60

        return value
