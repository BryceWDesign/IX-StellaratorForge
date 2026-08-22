"""Cross-platform canonicalization for persisted numerical evidence."""
from __future__ import annotations

from functools import wraps
from math import isfinite
from typing import Any, Callable


def canonicalize_evidence(value: Any) -> Any:
    """Return evidence with finite floats rounded to 10 significant digits.

    LAPACK and BLAS implementations can differ in the last few floating-point
    bits. Persisted evidence needs a stable representation across supported
    platforms while retaining substantially more precision than any declared
    screening threshold.
    """
    if isinstance(value, float):
        return float(format(value, ".10g")) if isfinite(value) else value
    if isinstance(value, dict):
        return {
            key: canonicalize_evidence(item)
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [canonicalize_evidence(item) for item in value]
    if isinstance(value, tuple):
        return tuple(canonicalize_evidence(item) for item in value)
    return value


def canonical_evidence(
    function: Callable[..., dict[str, Any]],
) -> Callable[..., dict[str, Any]]:
    """Canonicalize the evidence dictionary returned by a calculation."""

    @wraps(function)
    def wrapped(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return canonicalize_evidence(function(*args, **kwargs))

    return wrapped