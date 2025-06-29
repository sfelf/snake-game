"""Path smoothing utilities for creating smooth snake curves."""

import math
from typing import List, Optional, Tuple

from . import GameConstants


class PathSmoother:
    """Handles path smoothing and curve generation for snake movement."""

    @staticmethod
    def create_smooth_path(points: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        """Create a completely smooth path through the snake segments.

        Args:
            points: List of screen coordinate points

        Returns:
            List of smoothed points for drawing
        """
        if len(points) < 2:
            return points

        if len(points) == 2:
            # For short snake, interpolate between head and tail
            return PathSmoother._interpolate_points(points[0], points[1], 8)

        smooth_points = []

        # Start with head - ensure smooth start
        smooth_points.append(points[0])

        # Handle first segment specially to avoid head issues
        if len(points) > 2:
            # Smooth transition from head to first body segment
            head_to_first = PathSmoother._interpolate_points(points[0], points[1], 10)
            smooth_points.extend(head_to_first[1:])  # Skip first point (already added)

        # Create smooth curves between remaining segments
        for i in range(1, len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]

            # Get context points for better curve calculation
            prev_point = points[i - 1] if i > 0 else None
            next_point = points[i + 2] if i + 2 < len(points) else None

            # Create smooth interpolation between segments
            if i == len(points) - 2:  # Last segment
                # Simple interpolation to tail
                interpolated = PathSmoother._interpolate_points(
                    start_point, end_point, 8
                )
                smooth_points.extend(
                    interpolated[1:]
                )  # Skip first point (already added)
            else:
                # Create curved path considering neighboring segments
                # Reduce curve intensity near head to prevent issues
                curve_intensity = min(1.0, i / 3.0)  # Gradual curve increase from head
                curved_points = PathSmoother._create_curved_segment(
                    start_point, end_point, prev_point, next_point, curve_intensity
                )
                smooth_points.extend(
                    curved_points[1:]
                )  # Skip first point (already added)

        return smooth_points

    @staticmethod
    def _interpolate_points(
        start_point: Tuple[int, int], end_point: Tuple[int, int], num_points: int
    ) -> List[Tuple[int, int]]:
        """Create smooth interpolation between two points.

        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            num_points: Number of interpolation points

        Returns:
            List of interpolated points
        """
        points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            x = int(start_point[0] + (end_point[0] - start_point[0]) * t)
            y = int(start_point[1] + (end_point[1] - start_point[1]) * t)
            points.append((x, y))
        return points

    @staticmethod
    def _create_curved_segment(
        start_point: Tuple[int, int],
        end_point: Tuple[int, int],
        prev_point: Optional[Tuple[int, int]],
        next_point: Optional[Tuple[int, int]],
        curve_intensity: float = 1.0,
    ) -> List[Tuple[int, int]]:
        """Create a curved segment with enhanced smoothness and controlled arcing.

        Args:
            start_point: Current segment start
            end_point: Current segment end
            prev_point: Previous segment (for curve context)
            next_point: Next segment (for curve context)
            curve_intensity: Intensity of curve (0.0 to 1.0) to control near-head smoothness

        Returns:
            List of points forming an ultra-smooth curve
        """
        # Increased interpolation points for maximum smoothness
        num_points = 16
        curve_points = []

        for i in range(num_points):
            t = i / (num_points - 1)

            # Use enhanced Catmull-Rom spline for ultra-smooth curves
            if prev_point and next_point:
                # Full spline with 4 control points and tension adjustment
                point = PathSmoother._enhanced_catmull_rom_spline(
                    prev_point, start_point, end_point, next_point, t
                )
            else:
                # Enhanced interpolation with controlled curve bias
                # Create more pronounced arc but controlled by curve_intensity
                mid_x = (start_point[0] + end_point[0]) / 2
                mid_y = (start_point[1] + end_point[1]) / 2

                # Enhanced curve factor with intensity control
                base_curve_factor = 0.4 * math.sin(t * math.pi)
                curve_factor = (
                    base_curve_factor * curve_intensity
                )  # Apply intensity control

                # Perpendicular offset for enhanced curve
                dx = end_point[0] - start_point[0]
                dy = end_point[1] - start_point[1]
                length = math.sqrt(dx * dx + dy * dy)

                if length > 0:
                    perp_x = -dy / length * curve_factor * 15  # Curve strength
                    perp_y = dx / length * curve_factor * 15
                else:
                    perp_x = perp_y = 0

                x = int(start_point[0] + (end_point[0] - start_point[0]) * t + perp_x)
                y = int(start_point[1] + (end_point[1] - start_point[1]) * t + perp_y)
                point = (x, y)

            curve_points.append(point)

        return curve_points

    @staticmethod
    def _enhanced_catmull_rom_spline(
        p0: Tuple[int, int],
        p1: Tuple[int, int],
        p2: Tuple[int, int],
        p3: Tuple[int, int],
        t: float,
    ) -> Tuple[int, int]:
        """Calculate enhanced Catmull-Rom spline with tension control for ultra-smooth curves.

        Args:
            p0, p1, p2, p3: Control points
            t: Parameter (0 to 1)

        Returns:
            Interpolated point (x, y)
        """
        # Enhanced tension parameter for smoother curves
        tension = 0.5  # Standard Catmull-Rom tension

        t2 = t * t
        t3 = t2 * t

        # Enhanced Catmull-Rom spline formula with tension
        x = tension * (
            (2 * p1[0])
            + (-p0[0] + p2[0]) * t
            + (2 * p0[0] - 5 * p1[0] + 4 * p2[0] - p3[0]) * t2
            + (-p0[0] + 3 * p1[0] - 3 * p2[0] + p3[0]) * t3
        )

        y = tension * (
            (2 * p1[1])
            + (-p0[1] + p2[1]) * t
            + (2 * p0[1] - 5 * p1[1] + 4 * p2[1] - p3[1]) * t2
            + (-p0[1] + 3 * p1[1] - 3 * p2[1] + p3[1]) * t3
        )

        return (int(x), int(y))

    @staticmethod
    def convert_segments_to_screen_points(
        segments: List[Tuple[int, int]]
    ) -> List[Tuple[int, int]]:
        """Convert grid positions to screen coordinates.

        Args:
            segments: List of snake segment positions in grid coordinates

        Returns:
            List of screen coordinate points
        """
        screen_points = []
        for x, y in segments:
            screen_x = (
                GameConstants.PLAY_AREA_X
                + x * GameConstants.CELL_SIZE
                + GameConstants.CELL_SIZE // 2
            )
            screen_y = (
                GameConstants.PLAY_AREA_Y
                + y * GameConstants.CELL_SIZE
                + GameConstants.CELL_SIZE // 2
            )
            screen_points.append((screen_x, screen_y))
        return screen_points
