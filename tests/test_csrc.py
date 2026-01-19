from __future__ import annotations

import xyz


def test_mul():
    x0, x1 = 2, 3
    y = xyz.mul(x0, x1)
    z = x0 * x1
    assert y == z
