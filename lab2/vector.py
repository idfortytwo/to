from __future__ import annotations

import math
from abc import ABC, abstractmethod


class IVector(ABC):
    @abstractmethod
    def abs(self) -> float:
        pass

    @abstractmethod
    def cdot(self, param: IVector) -> float:
        pass

    @abstractmethod
    def get_components(self) -> [float]:
        pass


class Vector2D(IVector):
    def __init__(self, x: float, y: float):
        self._x = float(x)
        self._y = float(y)

    def abs(self) -> float:
        return math.sqrt(self._x * self._x + self._y * self._y)

    def cdot(self, param: IVector) -> float:
        other_x, other_y = param.get_components()
        return self._x * other_x + self._y * other_y

    def get_components(self) -> [float]:
        return [self._x, self._y]

    def __str__(self):
        return f'Vector2D({self._x:.5}, {self._y:.5})'


class Polar2DInheritance(Vector2D):
    def get_angle(self) -> float:
        return math.atan(self._y / self._x)

    def __str__(self):
        return f'Polar2DInheritance({self._x:.5}, {self._y:.5})'


class IPolar2D(ABC):
    @abstractmethod
    def abs(self) -> float:
        pass

    @abstractmethod
    def get_angle(self) -> float:
        pass


class Polar2DAdapter(IVector, IPolar2D):
    def __init__(self, src_vector: Vector2D):
        self._src_vector = src_vector

    def abs(self) -> float:
        return self._src_vector.abs()

    def get_angle(self) -> float:
        x, y = self._src_vector.get_components()
        return math.atan(y / x)

    def get_components(self) -> [float]:
        return self._src_vector.get_components()

    def cdot(self, param: IVector):
        return self._src_vector.cdot(param)

    def __str__(self):
        x, y = self._src_vector.get_components()
        return f'Polar2DAdapter({x:.5}, {y:.5})'


class Vector3DDecorator(IVector):
    def __init__(self, x: float, y: float, z: float):
        self._src_vector = Vector2D(x, y)
        self._z = float(z)

    def abs(self):
        x, y = self._src_vector.get_components()
        return math.sqrt(x * x + y * y + self._z * self._z)

    def cdot(self, param: IVector) -> float:
        x, y = self._src_vector.get_components()

        comp = param.get_components()
        other_x = comp[0]
        other_y = comp[1]
        other_z = comp[2] if len(comp) > 2 else 0

        return x * other_x + y * other_y + self._z * other_z

    def get_components(self) -> [float]:
        return self._src_vector.get_components() + [self._z]

    def cross(self, param: IVector):
        a, b = self._src_vector.get_components()
        c = self._z

        comp = param.get_components()
        d = comp[0]
        e = comp[1]
        f = comp[2] if len(comp) > 2 else 0

        new_x = b * f - c * e
        new_y = c * d - a * f
        new_z = a * e - b * d
        return Vector3DDecorator(new_x, new_y, new_z)

    def get_src_v(self):
        return self._src_vector

    def __str__(self):
        x, y = self._src_vector.get_components()
        return f'Vector3DDecorator({x:.5}, {y:.5}, {self._z:.5})'


class Vector3DInheritance(Vector2D):
    def __init__(self, x: float, y: float, z: float):
        super().__init__(x, y)
        self._z = float(z)

    def abs(self):
        return math.sqrt(self._x * self._x + self._y * self._y + self._z * self._z)

    def cdot(self, param: IVector):
        comp = param.get_components()
        other_x = comp[0]
        other_y = comp[1]
        other_z = comp[2] if len(comp) > 2 else 0

        return self._x * other_x + self._y * other_y + self._z * other_z

    def get_components(self) -> [float]:
        return [self._x, self._y, self._z]

    def cross(self, param: IVector):
        a = self._x
        b = self._y
        c = self._z

        comp = param.get_components()
        d = comp[0]
        e = comp[1]
        f = comp[2] if len(comp) > 2 else 0

        new_x = b * f - c * e
        new_y = c * d - a * f
        new_z = a * e - b * d
        return Vector3DInheritance(new_x, new_y, new_z)

    def get_src_v(self):
        return Vector2D(self._x, self._y)

    def __str__(self):
        return f'Vector3DInheritance({self._x:.5}, {self._y:.5}, {self._z:.5})'
