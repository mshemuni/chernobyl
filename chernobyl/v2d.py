from random import random

import numpy as np
from typing import Optional, Union, Tuple


class V2D:
    """
    A 2D vector class using NumPy for fast operations.

    Supports vector arithmetic, polar coordinates, rotation, magnitude,
    unit vector, dot product, angle calculation, and parallel/perpendicular checks.
    """

    def __init__(self, x: float = 0, y: float = 0) -> None:
        """
        Initialize a 2D vector.

        Args:
            x (float): X component of the vector.
            y (float): Y component of the vector.
        """
        self.vec = np.array([x, y], dtype=float)

    @property
    def x(self) -> float:
        """Return the x component of the vector."""
        return self.vec[0]

    @property
    def y(self) -> float:
        """Return the y component of the vector."""
        return self.vec[1]

    def __repr__(self) -> str:
        """Return a detailed string representation of the vector."""
        return f"{self.__class__.__name__}(x={self.x}, y={self.y})"

    def __str__(self) -> str:
        """Return a simple string representation of the vector."""
        return repr(self)

    def __iter__(self):
        """Allow unpacking of the vector: x, y = vector"""
        return iter(self.vec)

    # Arithmetic operators
    def __add__(self, other: "V2D") -> "V2D":
        """Add two vectors."""
        return V2D(*(self.vec + other.vec))

    def __sub__(self, other: "V2D") -> "V2D":
        """Subtract another vector from this vector."""
        return V2D(*(self.vec - other.vec))

    def __neg__(self) -> "V2D":
        """Return the negation of the vector."""
        return V2D(*(-self.vec))

    def __mul__(self, other: Union[float, "V2D"]) -> "V2D":
        """
        Multiply the vector by a scalar.

        Raises:
            TypeError: If multiplying by a non-scalar.
        """
        if isinstance(other, (int, float)):
            return V2D(*(self.vec * other))
        raise TypeError("2D vector can only multiply by a scalar")

    def __rmul__(self, scalar: float) -> "V2D":
        """Right-hand scalar multiplication."""
        return self * scalar

    def __truediv__(self, scalar: float) -> "V2D":
        """
        Divide the vector by a scalar.

        Raises:
            ValueError: If scalar is zero.
        """
        if scalar == 0:
            raise ValueError("Cannot divide by zero")
        return V2D(*(self.vec / scalar))

    def __eq__(self, other: "V2D") -> bool:
        """Check if two vectors are approximately equal."""
        return self.is_same(other)

    # Copy
    def copy(self) -> "V2D":
        """Return a copy of the vector."""
        return V2D(*self.vec)

    # Random vector
    @classmethod
    def random(cls, magnitude: float = 10, angle_range: float = 360.0) -> "V2D":
        """
        Generate a random 2D vector with a given magnitude and optional random angle range.

        Args:
            magnitude (float): The length of the vector. Defaults to 1.0.
            angle_range (float): Maximum angle in degrees for randomization. The angle
                                 will be chosen uniformly from 0 to `angle_range`.
                                 Defaults to 360 (full circle).

        Returns:
            V2D: A new 2D vector with the specified magnitude and random direction.
        """
        angle = np.random.uniform(0, angle_range)
        return cls.from_polar(magnitude, angle)

    # Create vector from polar coordinates
    @classmethod
    def from_polar(cls, magnitude: float, angle_deg: float, random_angle: float = 0) -> "V2D":
        """
        Create a vector from magnitude and angle in degrees.

        Args:
            magnitude (float): Length of the vector.
            angle_deg (float): Angle in degrees from the x-axis.
            random_angle (float): Optional ±randomization of angle in degrees.

        Returns:
            V2D: Vector represented by magnitude and angle.
        """
        angle = angle_deg
        if random_angle != 0:
            angle += np.random.uniform(-random_angle, random_angle)
        rad = np.radians(angle)
        x = magnitude * np.cos(rad)
        y = magnitude * np.sin(rad)
        return cls(x, y)

    # Magnitude
    def mag(self) -> float:
        """Return the magnitude (length) of the vector."""
        return np.linalg.norm(self.vec)

    # Distance
    def dist(self, other: Optional["V2D"] = None) -> float:
        """
        Compute distance to another vector.

        Args:
            other (V2D, optional): Another vector. Defaults to the origin (0,0).

        Returns:
            float: Euclidean distance.
        """
        if other is None:
            other = V2D()
        return np.linalg.norm(self.vec - other.vec)

    # Unit vector
    def unit(self) -> "V2D":
        """
        Return a unit vector in the same direction.

        Raises:
            ValueError: If the vector is zero-length.

        Returns:
            V2D: Unit vector.
        """
        m = self.mag()
        if m == 0:
            raise ValueError("Cannot get unit of zero vector")
        return self / m

    # Dot product
    def dot(self, other: "V2D") -> float:
        """Return the dot product with another vector."""
        return float(np.dot(self.vec, other.vec))

    # Angle between vectors in degrees
    def angle_between(self, other: "V2D") -> float:
        """
        Compute the angle between two vectors in degrees.

        Raises:
            ValueError: If either vector is zero-length.

        Returns:
            float: Angle in degrees.
        """
        if self.mag() == 0 or other.mag() == 0:
            raise ValueError("Cannot compute angle with zero vector")
        cos_angle = np.clip(self.dot(other) / (self.mag() * other.mag()), -1.0, 1.0)
        return np.degrees(np.arccos(cos_angle))

    # Parallel/perpendicular checks
    def is_parallel(self, other: "V2D", tolerance: float = 1e-6) -> bool:
        """
        Check if two vectors are parallel.

        Args:
            tolerance (float): Acceptable deviation.

        Returns:
            bool: True if parallel.
        """
        return abs(self.x * other.y - self.y * other.x) < tolerance

    def is_perpendicular(self, other: "V2D", tolerance: float = 1e-6) -> bool:
        """
        Check if two vectors are perpendicular.

        Args:
            tolerance (float): Acceptable deviation.

        Returns:
            bool: True if perpendicular.
        """
        return abs(self.dot(other)) < tolerance

    def is_non_parallel(self, other: "V2D") -> bool:
        """Check if the vector is neither parallel nor perpendicular to another vector."""
        return not (self.is_parallel(other) or self.is_perpendicular(other))

    # Rotate vector by angle in degrees
    def rotate(self, angle: float) -> "V2D":
        """
        Rotate the vector counter-clockwise by an angle in degrees.

        Args:
            angle (float): Rotation angle in degrees.

        Returns:
            V2D: Rotated vector.
        """
        rad = np.radians(angle)
        cos_a = np.cos(rad)
        sin_a = np.sin(rad)
        x, y = self.vec
        return V2D(x * cos_a - y * sin_a, x * sin_a + y * cos_a)

    # Output as tuple
    def as_tuple(self, whole: bool = False) -> Tuple[float, float]:
        """
        Return vector as a tuple.

        Args:
            whole (bool): If True, returns integer components.

        Returns:
            Tuple[float, float]: (x, y) tuple.
        """
        if whole:
            return int(self.x), int(self.y)
        return self.x, self.y

    # Compare with tolerance
    def is_same(self, other: "V2D", tolerance: float = 1e-6) -> bool:
        """
        Check if two vectors are approximately the same.

        Args:
            other (V2D): Another vector.
            tolerance (float): Maximum allowed difference.

        Returns:
            bool: True if vectors are approximately equal.
        """
        return self.dist(other) < tolerance
