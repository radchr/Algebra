"""Geometry Engine package for Digital-First Marimo curriculum."""

from .db import BookDatabase, BookFigure, BookPage
from .lesson import Lesson, Segment, load_all_lessons, load_lesson, parse_lesson
from .svg_drawings import get_book_figure, get_book_figure_svg, render_figure_card

__all__ = [
    "BookDatabase",
    "BookFigure",
    "BookPage",
    "Lesson",
    "Segment",
    "get_book_figure",
    "get_book_figure_svg",
    "load_all_lessons",
    "load_lesson",
    "parse_lesson",
    "render_figure_card",
]
