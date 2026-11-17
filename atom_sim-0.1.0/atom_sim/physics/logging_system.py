"""Structured logging setup for the atom simulator."""

from __future__ import annotations

import logging
import sys
from typing import Optional


def configure_logging(
    level: int = logging.INFO,
    stream: Optional[object] = None,
) -> logging.Logger:
    """
    Configure root logger for atom_sim.
    Deterministic: no timestamps that vary, or use fixed format.
    """
    logger = logging.getLogger("atom_sim")
    if logger.handlers:
        return logger  # already configured

    handler = logging.StreamHandler(stream or sys.stderr)
    formatter = logging.Formatter(
        "%(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(level)
    logger.propagate = False
    return logger


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(f"atom_sim.{name}")
