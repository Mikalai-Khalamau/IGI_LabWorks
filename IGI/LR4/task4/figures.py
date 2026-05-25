# Lab 4, Task 4
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module defining geometric figures using OOP principles.
Implements: abstract base class, inheritance, properties, mixins, polymorphism.
Variant 27: Regular Hexagon with side length 'a'.
"""
import math
from abc import ABC, abstractmethod

class FigureColor:
    """Class representing figure color with property-based encapsulation."""
    _valid_colors = ['red', 'green', 'blue', 'yellow', 'cyan', 'magenta',
                     'black', 'white', 'orange', 'purple', 'pink', 'brown']

    def __init__(self, color: str = 'blue'):
        self._color = color.lower() if color.lower() in self._valid_colors else 'blue'

    @property
    def color(self) -> str:
        """Getter for color property."""
        return self._color

    @color.setter
    def color(self, value: str):
        """Setter with validation for color property."""
        if value.lower() in self._valid_colors:
            self._color = value.lower()
        else:
            raise ValueError(f"Invalid color. Choose from: {self._valid_colors}")

    def get_color(self) -> str:
        """Classic getter method."""
        return self._color

    def set_color(self, value: str):
        """Classic setter method."""
        self.color = value

    def __str__(self) -> str:
        return self._color


class GeometricFigure(ABC):
    """Abstract base class for all geometric figures."""
    _figures_count: int = 0  # Static attribute: total instances created

    def __init__(self, color: str = 'blue'):
        self._color_obj = FigureColor(color)
        self._label: str = ""  # Dynamic attribute for text annotation
        GeometricFigure._figures_count += 1

    @property
    def color_obj(self) -> FigureColor:
        """Property to access color object."""
        return self._color_obj

    @property
    def label(self) -> str:
        return self._label

    @label.setter
    def label(self, value: str):
        self._label = value

    @abstractmethod
    def area(self) -> float:
        """Abstract method: calculate figure area. Must be overridden."""
        pass

    @abstractmethod
    def get_parameters(self) -> dict:
        """Abstract method: return figure parameters dict. Must be overridden."""
        pass

    @abstractmethod
    def get_vertices(self) -> list:
        """Abstract method: return list of (x, y) vertices for plotting. Must be overridden."""
        pass

    @classmethod
    def get_figures_count(cls) -> int:
        """Class method: return total created figures."""
        return cls._figures_count

    def __str__(self) -> str:
        return f"{self.get_name()}(color={self.color_obj.color}, area={self.area():.2f})"

    @staticmethod
    @abstractmethod
    def get_name() -> str:
        """Static method: return figure name. Must be overridden."""
        pass


class DrawableMixin:
    """Mixin providing drawing-related utility methods."""

    def get_formatted_info(self) -> str:
        """Returns formatted string with figure info using format() method."""
        params = self.get_parameters()
        params_str = ", ".join(f"{k}={v}" for k, v in params.items())
        return "{} [{}] | Area: {:.2f} | Color: {}".format(
            self.get_name(), params_str, self.area(), self.color_obj.color
        )

    def to_dict(self) -> dict:
        """Converts figure to dictionary for serialization."""
        return {
            "name": self.get_name(),
            "parameters": self.get_parameters(),
            "area": self.area(),
            "color": self.color_obj.color,
            "label": self.label
        }


class RegularHexagon(GeometricFigure, DrawableMixin):
    """Regular hexagon with side length 'a'. Inherits from GeometricFigure."""

    def __init__(self, side: float, color: str = 'blue'):
        if side <= 0:
            raise ValueError("Side length must be positive.")
        super().__init__(color)  # Call parent constructor via super()
        self._side = side

    @property
    def side(self) -> float:
        return self._side

    @side.setter
    def side(self, value: float):
        if value <= 0:
            raise ValueError("Side length must be positive.")
        self._side = value

    def area(self) -> float:
        """Calculates area of regular hexagon: A = (3√3/2) * a²"""
        return (3 * math.sqrt(3) / 2) * (self._side ** 2)

    def perimeter(self) -> float:
        """Calculates perimeter: P = 6 * a"""
        return 6 * self._side

    def get_parameters(self) -> dict:
        """Returns dictionary of figure parameters."""
        return {
            "side": round(self._side, 4),
            "perimeter": round(self.perimeter(), 4),
            "apothem": round(self._side * math.sqrt(3) / 2, 4)
        }

    def get_vertices(self) -> list:
        """Returns list of (x, y) coordinates for plotting centered at origin."""
        vertices = []
        for i in range(6):
            angle = math.radians(60 * i)
            x = self._side * math.cos(angle)
            y = self._side * math.sin(angle)
            vertices.append((round(x, 4), round(y, 4)))
        return vertices

    @staticmethod
    def get_name() -> str:
        """Returns static figure name."""
        return "RegularHexagon"

    def __repr__(self) -> str:
        return f"RegularHexagon(side={self._side}, color='{self.color_obj.color}')"