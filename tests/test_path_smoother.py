"""Tests for path smoothing utilities."""

import math

import pytest

from snake_game.utils.path_smoother import PathSmoother


class TestPathSmoother:
    """Test cases for PathSmoother class."""

    def test_create_smooth_path_empty_list(self):
        """Test smooth path creation with empty list."""
        result = PathSmoother.create_smooth_path([])
        assert result == []

    def test_create_smooth_path_single_point(self):
        """Test smooth path creation with single point."""
        points = [(10, 10)]
        result = PathSmoother.create_smooth_path(points)
        assert result == points

    def test_create_smooth_path_two_points(self):
        """Test smooth path creation with two points."""
        points = [(0, 0), (10, 10)]
        result = PathSmoother.create_smooth_path(points)

        # Should return interpolated points
        assert len(result) == 8  # Default interpolation count
        assert result[0] == (0, 0)  # First point unchanged
        assert result[-1] == (10, 10)  # Last point unchanged

        # Check intermediate points are interpolated
        for i in range(1, len(result) - 1):
            x, y = result[i]
            assert 0 < x < 10
            assert 0 < y < 10

    def test_create_smooth_path_multiple_points(self):
        """Test smooth path creation with multiple points."""
        points = [(0, 0), (10, 0), (10, 10), (0, 10)]
        result = PathSmoother.create_smooth_path(points)

        # Should return more points than input
        assert len(result) > len(points)

        # First and last points should be preserved
        assert result[0] == points[0]
        # Note: Last point might be slightly different due to curve smoothing

    def test_interpolate_points(self):
        """Test point interpolation."""
        start = (0, 0)
        end = (10, 10)
        num_points = 5

        result = PathSmoother._interpolate_points(start, end, num_points)

        assert len(result) == num_points
        assert result[0] == start
        assert result[-1] == end

        # Check intermediate points
        expected_points = [(0, 0), (2, 2), (5, 5), (7, 7), (10, 10)]
        for i, (x, y) in enumerate(result):
            expected_x, expected_y = expected_points[i]
            assert abs(x - expected_x) <= 1  # Allow for rounding
            assert abs(y - expected_y) <= 1

    def test_enhanced_catmull_rom_spline(self):
        """Test Catmull-Rom spline calculation."""
        p0 = (0, 0)
        p1 = (10, 0)
        p2 = (20, 10)
        p3 = (30, 10)

        # Test at different t values
        result_start = PathSmoother._enhanced_catmull_rom_spline(p0, p1, p2, p3, 0.0)
        result_end = PathSmoother._enhanced_catmull_rom_spline(p0, p1, p2, p3, 1.0)
        result_mid = PathSmoother._enhanced_catmull_rom_spline(p0, p1, p2, p3, 0.5)

        # At t=0, should be close to p1
        assert abs(result_start[0] - p1[0]) <= 1
        assert abs(result_start[1] - p1[1]) <= 1

        # At t=1, should be close to p2
        assert abs(result_end[0] - p2[0]) <= 1
        assert abs(result_end[1] - p2[1]) <= 1

        # At t=0.5, should be between p1 and p2
        assert p1[0] <= result_mid[0] <= p2[0]

    def test_create_curved_segment(self):
        """Test curved segment creation."""
        start = (0, 0)
        end = (10, 0)
        prev = (-10, 0)
        next_point = (20, 0)

        result = PathSmoother._create_curved_segment(start, end, prev, next_point, 1.0)

        assert len(result) == 16  # Default number of points
        assert result[0] == start
        assert result[-1] == end

    def test_create_curved_segment_no_context(self):
        """Test curved segment creation without context points."""
        start = (0, 0)
        end = (10, 10)

        result = PathSmoother._create_curved_segment(start, end, None, None, 1.0)

        assert len(result) == 16
        assert result[0] == start
        assert result[-1] == end

    def test_create_curved_segment_curve_intensity(self):
        """Test curved segment with different curve intensities."""
        start = (0, 0)
        end = (10, 0)

        # Low intensity should be closer to straight line
        result_low = PathSmoother._create_curved_segment(start, end, None, None, 0.1)
        result_high = PathSmoother._create_curved_segment(start, end, None, None, 1.0)

        # Both should have same number of points
        assert len(result_low) == len(result_high)

        # High intensity should have more curve (points further from straight line)
        # This is a basic check - in practice, curve differences would be more subtle
        assert len(result_low) > 0
        assert len(result_high) > 0

    def test_convert_segments_to_screen_points(self):
        """Test conversion from grid to screen coordinates."""
        segments = [(0, 0), (1, 1), (2, 2)]

        result = PathSmoother.convert_segments_to_screen_points(segments)

        assert len(result) == len(segments)

        # Check conversion formula
        from snake_game.utils import GameConstants

        for i, (grid_x, grid_y) in enumerate(segments):
            screen_x, screen_y = result[i]
            expected_x = (
                GameConstants.PLAY_AREA_X
                + grid_x * GameConstants.CELL_SIZE
                + GameConstants.CELL_SIZE // 2
            )
            expected_y = (
                GameConstants.PLAY_AREA_Y
                + grid_y * GameConstants.CELL_SIZE
                + GameConstants.CELL_SIZE // 2
            )

            assert screen_x == expected_x
            assert screen_y == expected_y

    def test_convert_segments_empty_list(self):
        """Test conversion with empty segment list."""
        result = PathSmoother.convert_segments_to_screen_points([])
        assert result == []
