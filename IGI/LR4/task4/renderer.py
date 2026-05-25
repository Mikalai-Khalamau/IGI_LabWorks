# Lab 4, Task 4
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for matplotlib visualization of geometric figures.
Handles plotting, coloring, text annotation, and file saving.
"""
import matplotlib.pyplot as plt
from typing import List, Tuple
import os


class FigureRenderer:
    """Renderer for geometric figures using matplotlib."""

    def __init__(self, figsize: tuple = (8, 8), title: str = "Geometric Figure"):
        self.figsize = figsize
        self.title = title
        self._fig = None
        self._ax = None

    def _setup_plot(self):
        """Initializes matplotlib figure and axes."""
        self._fig, self._ax = plt.subplots(figsize=self.figsize)
        self._ax.set_aspect('equal')
        self._ax.grid(True, alpha=0.3, linestyle=':')
        self._ax.set_title(self.title, fontsize=14, fontweight='bold')
        self._ax.set_xlabel("X")
        self._ax.set_ylabel("Y")

    def draw_hexagon(self, vertices: List[Tuple[float, float]],
                     color: str, label: str = "") -> bool:
        """Draws regular hexagon from vertices list."""
        if not vertices or len(vertices) != 6:
            raise ValueError("Hexagon requires exactly 6 vertices.")

        self._setup_plot()

        # Extract x, y coordinates
        xs, ys = zip(*vertices)
        xs = list(xs) + [xs[0]]  # Close the polygon
        ys = list(ys) + [ys[0]]

        # Draw filled polygon
        self._ax.fill(xs, ys, color=color, alpha=0.6, edgecolor='black', linewidth=2)

        # Add label/text annotation if provided
        if label:
            # Place label at centroid
            cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
            self._ax.text(cx, cy, label, ha='center', va='center',
                          fontsize=11, fontweight='bold',
                          bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))

        # Add info box with parameters
        info_text = f"Area: {sum(xs[i] * ys[i + 1] - xs[i + 1] * ys[i] for i in range(6)) / 2:.2f}"
        self._ax.text(0.02, 0.98, info_text, transform=self._ax.transAxes,
                      fontsize=9, verticalalignment='top',
                      bbox=dict(boxstyle='square', facecolor='lightyellow', alpha=0.7))

        return True

    def show_plot(self):
        """Displays the plot window."""
        if self._fig:
            plt.show()

    def save_plot(self, filepath: str) -> bool:
        """Saves plot to file with error handling."""
        if not self._fig:
            return False
        try:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            self._fig.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Figure saved to: {os.path.abspath(filepath)}")
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False

    def close(self):
        """Closes the figure to free memory."""
        if self._fig:
            plt.close(self._fig)