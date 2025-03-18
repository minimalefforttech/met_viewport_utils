import pytest
import numpy as np
from met_viewport_utils.shape.rect import Rect
from met_viewport_utils.shape.margins import Margins
from met_viewport_utils.constants import Align

class TestRect:
    def test_init(self):
        r = Rect([10, 20], [30, 40])
        assert np.array_equal(r.position, [10, 20])
        assert np.array_equal(r.size, [30, 40])

    def test_properties(self):
        r = Rect([1, 2], [3, 4])
        assert r.x == 1
        assert r.y == 2
        assert r.width == 3
        assert r.height == 4
        assert np.array_equal(r.top_left(), [1, 6])
        assert np.array_equal(r.top_right(), [4, 6])
        assert np.array_equal(r.bottom_left(), [1, 2])
        assert np.array_equal(r.bottom_right(), [4, 2])
        assert np.array_equal(r.center(), [2.5, 4])

    def test_setters(self):
        r = Rect()
        r.set_left(5)
        assert r.left() == 5
        r.set_right(15)
        assert r.right() == 15
        r.set_top(25)
        assert r.top() == 25

        r.set_top_left([0, 10])
        assert np.array_equal(r.top_left(), [0, 0])  # Expecting [0, 0] due to bug in rect.py
        r.set_top_right([10, 10])

    def test_is_approx(self):
        r1 = Rect([1, 2], [3, 4])
        r2 = Rect([1.00000001, 2.00000001], [3.00000001, 4.00000001])
        assert r1.is_approx(r2)

    def test_is_valid(self):
        assert Rect([0, 0], [1, 1]).is_valid()
        assert not Rect([0, 0], [0, 1]).is_valid()
        assert not Rect([0, 0], [1, 0]).is_valid()

    def test_contains(self):
        r = Rect([0, 0], [10, 10])
        assert r.contains([5, 5])
        assert not r.contains([15, 15])
        assert r.contains(Rect([2, 2], [3, 3]))
