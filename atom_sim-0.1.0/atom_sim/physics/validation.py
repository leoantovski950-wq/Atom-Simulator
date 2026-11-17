"""Input validation and numerical safety helpers."""

from __future__ import annotations

from typing import Any, Optional
import math
import logging

logger = logging.getLogger("atom_sim.validation")


class ValidationError(ValueError):
    """Raised when physics inputs violate domain constraints."""


def require_positive(value: float, name: str) -> float:
    if not isinstance(value, (int, float)) or math.isnan(value) or math.isinf(value):
        raise ValidationError(f"{name} must be a finite number, got {value}")
    if value <= 0:
        raise ValidationError(f"{name} must be > 0, got {value}")
    return float(value)


def require_non_negative(value: float, name: str) -> float:
    if not isinstance(value, (int, float)) or math.isnan(value) or math.isinf(value):
        raise ValidationError(f"{name} must be a finite number, got {value}")
    if value < 0:
        raise ValidationError(f"{name} must be >= 0, got {value}")
    return float(value)


def require_int_ge(value: Any, minimum: int, name: str) -> int:
    if not isinstance(value, int) or isinstance(value, bool):
        raise ValidationError(f"{name} must be int, got {type(value)}")
    if value < minimum:
        raise ValidationError(f"{name} must be >= {minimum}, got {value}")
    return value


def finite_or_raise(value: float, name: str) -> float:
    if math.isnan(value) or math.isinf(value):
        raise ValidationError(f"{name} is not finite: {value}")
    return value


def assert_close(
    actual: float,
    expected: float,
    *,
    rtol: float = 1e-9,
    atol: float = 1e-12,
    msg: str = "",
) -> None:
    """Raise AssertionError if values differ beyond tolerance."""
    if math.isnan(actual) or math.isnan(expected):
        raise AssertionError(f"NaN encountered: actual={actual}, expected={expected}. {msg}")
    diff = abs(actual - expected)
    tol = atol + rtol * abs(expected)
    if diff > tol:
        raise AssertionError(
            f"Values not close: actual={actual}, expected={expected}, "
            f"diff={diff}, tol={tol}. {msg}"
        )
