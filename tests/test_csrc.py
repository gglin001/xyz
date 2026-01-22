from __future__ import annotations

import xyz


# TODO: add a pytest marker
def test_mul():
    x0, x1 = 2, 3
    y = xyz._C.mul(x0, x1)
    z = x0 * x1
    assert y == z
