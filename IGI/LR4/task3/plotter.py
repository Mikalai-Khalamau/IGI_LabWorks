# Lab 4, Task 3
# Version: 1
# Developer: Khalamau Mikalai Andreevich
# Date: 17.04.2026
"""
Module for matplotlib visualization of Taylor series vs math function.
Handles axes, legend, annotations, and file saving as required by Lab 4.
"""
import matplotlib.pyplot as plt
from typing import List, Dict
import os

class Plotter:
    """Creates and saves comparison plots with full formatting."""
    def __init__(self, title: str = "Taylor Series vs Math Function"):
        self.title = title
        self._fig = None
        self._ax = None

    def create_plot(self, data: List[Dict], series_label: str = "Taylor Series",
                    math_label: str = "Math Function"):
        if not data:
            raise ValueError("No data to plot.")

        x_vals = [d["x"] for d in data]
        y_series = [d["F_series"] for d in data]
        y_math = [d["F_math"] for d in data]

        self._fig, self._ax = plt.subplots(figsize=(10, 6))

        # Lab 4: Different colors on same axis
        self._ax.plot(x_vals, y_series, color='blue', linewidth=2,
                      label=series_label, marker='o', markersize=5)
        self._ax.plot(x_vals, y_math, color='red', linewidth=2,
                      label=math_label, linestyle='--')

        # Lab 4: Axes, legend, text, annotation
        self._ax.set_xlabel("x", fontsize=12)
        self._ax.set_ylabel("F(x)", fontsize=12)
        self._ax.set_title(self.title, fontsize=14, fontweight='bold')
        self._ax.legend(loc='best', fontsize=10)
        self._ax.grid(True, alpha=0.3, linestyle=':')

        max_err = max(data, key=lambda d: d["error"])
        self._ax.annotate(f"Max error: {max_err['error']:.2e}\n@ x={max_err['x']}",
                          xy=(max_err["x"], max_err["F_series"]),
                          xytext=(max_err["x"]+0.5, max_err["F_series"]*1.1),
                          fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.4),
                          arrowprops=dict(arrowstyle="->", color="black"))

        info_text = f"Points: {len(data)} | Max Iter: {data[0]['n']}"
        self._ax.text(0.02, 0.98, info_text, transform=self._ax.transAxes,
                      fontsize=10, verticalalignment='top',
                      bbox=dict(boxstyle="square", facecolor="white", alpha=0.8, edgecolor="gray"))

        return self._fig, self._ax

    def show_plot(self):
        if self._fig: plt.show()

    def save_plot(self, filepath: str) -> bool:
        """Saves plot to file. Creates directory if needed."""
        if not self._fig: return False
        try:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            self._fig.savefig(filepath, dpi=300, bbox_inches='tight')
            print(f"Plot saved to: {os.path.abspath(filepath)}")
            return True
        except Exception as e:
            print(f"Save error: {e}")
            return False