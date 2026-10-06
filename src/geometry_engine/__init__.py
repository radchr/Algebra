"""Geometry Engine package for Digital-First Marimo curriculum."""

from .db import BookDatabase, BookFigure, BookPage
from .svg_drawings import get_book_figure, get_book_figure_svg, render_figure_card

__all__ = [
    "BookDatabase",
    "BookFigure",
    "BookPage",
    "get_book_figure",
    "get_book_figure_svg",
    "render_figure_card",
]
