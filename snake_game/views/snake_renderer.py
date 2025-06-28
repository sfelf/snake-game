"""Snake rendering components with proper separation of concerns."""

import pygame
import math
from typing import List, Tuple
from ..models import Snake, Direction
from ..utils import GameConstants


class SnakeBodyRenderer:
    """Handles rendering of the snake body with proper proportions and effects."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
    
    def draw_body(self, points: List[Tuple[int, int]], segments: List[Tuple[int, int]]):
        """Draw the snake body with proper proportions and green striped coloring.
        
        Args:
            points: Smoothed path points
            segments: Original segment positions for thickness calculation
        """
        if len(points) < 2:
            return
        
        # Draw the snake body with proper proportions and green stripes
        for i in range(len(points) - 1):
            start_point = points[i]
            end_point = points[i + 1]
            
            # Calculate proper body proportions
            progress = i / max(1, len(points) - 1)
            thickness = self._calculate_thickness(progress)
            
            # Draw enhanced segment with proper proportions and stripes
            self._draw_striped_segment(start_point, end_point, thickness, progress, i)
    
    def _calculate_thickness(self, progress: float) -> int:
        """Calculate body thickness based on position along snake.
        
        Args:
            progress: Position along snake (0=head, 1=tail)
            
        Returns:
            Thickness value for this position
        """
        # Create natural body thickness curve
        if progress < 0.3:  # Head section - thinner
            thickness_factor = 0.7 + (progress / 0.3) * 0.3  # 0.7 to 1.0
        elif progress < 0.7:  # Middle section - widest
            middle_progress = (progress - 0.3) / 0.4
            thickness_factor = 1.0 + math.sin(middle_progress * math.pi) * 0.3  # 1.0 to 1.3 and back
        else:  # Tail section - tapered
            tail_progress = (progress - 0.7) / 0.3
            thickness_factor = 1.0 - tail_progress * 0.6  # 1.0 to 0.4
        
        base_thickness = 16  # Base thickness
        return max(4, int(base_thickness * thickness_factor))
    
    def _draw_striped_segment(self, start_point: Tuple[int, int], end_point: Tuple[int, int], 
                            thickness: int, progress: float, segment_index: int):
        """Draw a single segment with green coloring and stripe patterns.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            thickness: Segment thickness
            progress: Position along snake (0=head, 1=tail)
            segment_index: Index for stripe patterns
        """
        # Calculate segment direction
        dx = end_point[0] - start_point[0]
        dy = end_point[1] - start_point[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
        
        # Enhanced green coloration with shimmer
        base_intensity = 1.0 - progress * 0.1
        
        # Multi-wave shimmer system
        time_ms = pygame.time.get_ticks()
        primary_shimmer = math.sin((time_ms * 0.003) + (segment_index * 0.2)) * 0.3 + 0.7
        secondary_shimmer = math.cos((time_ms * 0.002) + (segment_index * 0.15)) * 0.2 + 0.8
        shimmer_intensity = (primary_shimmer * secondary_shimmer) * base_intensity
        
        # Stripe pattern
        stripe_pattern = math.sin(segment_index * 0.4) > 0.3
        stripe_intensity = 0.7 if stripe_pattern else 1.0
        
        # Create shading layers
        shading_layers = self._create_shading_layers(base_intensity, shimmer_intensity, stripe_intensity)
        
        # Draw each shading layer
        for layer in shading_layers:
            layer_thickness = max(1, int(thickness * layer['thickness_mult']))
            
            # Calculate offset
            offset_scale = min(1.0, thickness / 16.0)
            offset_distance = thickness * 0.08 * offset_scale
            
            offset_x = layer['offset'][0] * offset_distance
            offset_y = layer['offset'][1] * offset_distance
            
            offset_start = (int(start_point[0] + offset_x), int(start_point[1] + offset_y))
            offset_end = (int(end_point[0] + offset_x), int(end_point[1] + offset_y))
            
            # Draw the layer
            if layer.get('blur', False):
                self._draw_blurred_line(offset_start, offset_end, layer['color'], layer_thickness)
            else:
                self._draw_ultra_smooth_line(offset_start, offset_end, layer['color'], layer_thickness)
    
    def _create_shading_layers(self, base_intensity: float, shimmer_intensity: float, 
                             stripe_intensity: float) -> List[dict]:
        """Create shading layers for 3D effect.
        
        Args:
            base_intensity: Base color intensity
            shimmer_intensity: Shimmer effect intensity
            stripe_intensity: Stripe pattern intensity
            
        Returns:
            List of shading layer definitions
        """
        # Green coloration with stripes
        base_colors = {
            'shadow': (int(8 * base_intensity * stripe_intensity), 
                      int(35 * base_intensity * stripe_intensity), 
                      int(8 * base_intensity * stripe_intensity)),
            'main_shadow': (int(18 * base_intensity * stripe_intensity), 
                           int(70 * base_intensity * stripe_intensity), 
                           int(18 * base_intensity * stripe_intensity)),
            'secondary': (int(25 * base_intensity * stripe_intensity), 
                         int(90 * base_intensity * stripe_intensity), 
                         int(25 * base_intensity * stripe_intensity)),
            'base': (int(40 * base_intensity * stripe_intensity), 
                    int(140 * base_intensity * stripe_intensity), 
                    int(40 * base_intensity * stripe_intensity)),
            'mid': (int(50 * shimmer_intensity * stripe_intensity), 
                   int(170 * shimmer_intensity * stripe_intensity), 
                   int(50 * shimmer_intensity * stripe_intensity)),
            'highlight': (int(65 * shimmer_intensity * stripe_intensity), 
                         int(210 * shimmer_intensity * stripe_intensity), 
                         int(65 * shimmer_intensity * stripe_intensity)),
            'top': (int(85 * shimmer_intensity * stripe_intensity), 
                   int(240 * shimmer_intensity * stripe_intensity), 
                   int(85 * shimmer_intensity * stripe_intensity)),
            'specular': (int(110 * shimmer_intensity * stripe_intensity), 
                        int(255 * shimmer_intensity * stripe_intensity), 
                        int(110 * shimmer_intensity * stripe_intensity)),
            'ultra': (int(140 * shimmer_intensity * stripe_intensity), 
                     int(255 * shimmer_intensity * stripe_intensity), 
                     int(140 * shimmer_intensity * stripe_intensity))
        }
        
        return [
            {'color': base_colors['shadow'], 'offset': (-0.3, -0.3), 'thickness_mult': 1.05, 'blur': True},
            {'color': base_colors['main_shadow'], 'offset': (-0.2, -0.2), 'thickness_mult': 1.0, 'blur': False},
            {'color': base_colors['secondary'], 'offset': (-0.1, -0.1), 'thickness_mult': 0.98, 'blur': False},
            {'color': base_colors['base'], 'offset': (0, 0), 'thickness_mult': 0.95, 'blur': False},
            {'color': base_colors['mid'], 'offset': (0.05, 0.05), 'thickness_mult': 0.8, 'blur': False},
            {'color': base_colors['highlight'], 'offset': (0.12, 0.12), 'thickness_mult': 0.65, 'blur': False},
            {'color': base_colors['top'], 'offset': (0.18, 0.18), 'thickness_mult': 0.45, 'blur': False},
            {'color': base_colors['specular'], 'offset': (0.22, 0.22), 'thickness_mult': 0.25, 'blur': False},
            {'color': base_colors['ultra'], 'offset': (0.25, 0.25), 'thickness_mult': 0.12, 'blur': False}
        ]
    
    def _draw_blurred_line(self, start_point: Tuple[int, int], end_point: Tuple[int, int], 
                          color: Tuple[int, int, int], thickness: int):
        """Draw a blurred line for shadow effects.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            color: Line color
            thickness: Line thickness
        """
        if thickness <= 0:
            return
        
        # Create multiple offset lines for blur effect
        blur_offsets = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
        blur_color = tuple(c // 2 for c in color[:3])
        
        # Draw blur layers
        for offset_x, offset_y in blur_offsets:
            blur_start = (start_point[0] + offset_x, start_point[1] + offset_y)
            blur_end = (end_point[0] + offset_x, end_point[1] + offset_y)
            
            if thickness > 1:
                pygame.draw.line(self.screen, blur_color, blur_start, blur_end, max(1, thickness - 1))
        
        # Draw main line
        self._draw_ultra_smooth_line(start_point, end_point, color, thickness)
    
    def _draw_ultra_smooth_line(self, start_point: Tuple[int, int], end_point: Tuple[int, int], 
                               color: Tuple[int, int, int], thickness: int):
        """Draw an ultra-smooth thick line with perfect anti-aliasing.
        
        Args:
            start_point: Starting point (x, y)
            end_point: Ending point (x, y)
            color: Line color
            thickness: Line thickness
        """
        if thickness <= 0:
            return
        
        # For very smooth lines, draw multiple thin lines with slight offsets
        if thickness > 4:
            # Draw main thick line
            pygame.draw.line(self.screen, color, start_point, end_point, thickness)
            
            # Add anti-aliasing by drawing thinner lines around the edges
            edge_color = tuple(min(255, c + 20) for c in color[:3])
            pygame.draw.line(self.screen, edge_color, start_point, end_point, max(1, thickness - 2))
            
            # Draw perfect rounded end caps
            radius = thickness // 2
            if radius > 0:
                # Main caps
                pygame.draw.circle(self.screen, color, start_point, radius)
                pygame.draw.circle(self.screen, color, end_point, radius)
                
                # Anti-aliased edge caps
                if radius > 2:
                    pygame.draw.circle(self.screen, edge_color, start_point, radius - 1)
                    pygame.draw.circle(self.screen, edge_color, end_point, radius - 1)
        else:
            # For thin lines, just draw normally
            pygame.draw.line(self.screen, color, start_point, end_point, thickness)
            if thickness > 1:
                radius = thickness // 2
                pygame.draw.circle(self.screen, color, start_point, radius)
                pygame.draw.circle(self.screen, color, end_point, radius)


class SnakeHeadRenderer:
    """Handles rendering of the snake head with realistic features."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
    
    def draw_head(self, x: int, y: int, direction: Direction):
        """Draw a realistic elongated snake head.
        
        Args:
            x: Grid x position
            y: Grid y position
            direction: Snake's current direction
        """
        screen_x = GameConstants.PLAY_AREA_X + x * GameConstants.CELL_SIZE
        screen_y = GameConstants.PLAY_AREA_Y + y * GameConstants.CELL_SIZE
        center_x = screen_x + GameConstants.CELL_SIZE // 2
        center_y = screen_y + GameConstants.CELL_SIZE // 2
        
        # More elongated head dimensions
        base_width = 14
        base_height = 24  # Much more elongated
        
        # Adjust head orientation based on direction
        if direction in [Direction.LEFT, Direction.RIGHT]:
            head_width, head_height = base_height, base_width
        else:
            head_width, head_height = base_width, base_height
        
        # Draw multi-layered elongated head
        self._draw_head_layers(center_x, center_y, head_width, head_height)
        
        # Draw features
        self._draw_eyes(center_x, center_y, direction)
        self._draw_tongue(center_x, center_y, direction)
        self._draw_nostrils(center_x, center_y, direction)
    
    def _draw_head_layers(self, center_x: int, center_y: int, width: int, height: int):
        """Draw multiple layers for elongated snake head with green coloring.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            width: Head width
            height: Head height
        """
        # Time-based shimmer for head
        time_ms = pygame.time.get_ticks()
        shimmer = math.sin(time_ms * 0.002) * 0.2 + 0.8
        
        # Green head layers with proper elongated shape
        head_layers = [
            {'color': (int(15 * shimmer), int(60 * shimmer), int(15 * shimmer)), 
             'offset': (-2, -2), 'size_mult': 1.1},
            {'color': (int(25 * shimmer), int(90 * shimmer), int(25 * shimmer)), 
             'offset': (-1, -1), 'size_mult': 1.05},
            {'color': (int(40 * shimmer), int(140 * shimmer), int(40 * shimmer)), 
             'offset': (0, 0), 'size_mult': 1.0},
            {'color': (int(55 * shimmer), int(180 * shimmer), int(55 * shimmer)), 
             'offset': (0, 0), 'size_mult': 0.85},
            {'color': (int(70 * shimmer), int(220 * shimmer), int(70 * shimmer)), 
             'offset': (1, 1), 'size_mult': 0.7},
            {'color': (int(90 * shimmer), int(255 * shimmer), int(90 * shimmer)), 
             'offset': (2, 2), 'size_mult': 0.5}
        ]
        
        # Draw each head layer with elongated shape
        for layer in head_layers:
            layer_width = int(width * layer['size_mult'])
            layer_height = int(height * layer['size_mult'])
            
            # Apply offset for 3D effect
            offset_x = center_x + layer['offset'][0]
            offset_y = center_y + layer['offset'][1]
            
            # Create elongated head shape rectangle
            head_rect = pygame.Rect(
                offset_x - layer_width // 2,
                offset_y - layer_height // 2,
                layer_width,
                layer_height
            )
            
            # Draw elongated elliptical head shape
            pygame.draw.ellipse(self.screen, layer['color'], head_rect)
    
    def _draw_eyes(self, center_x: int, center_y: int, direction: Direction):
        """Draw realistic snake eyes.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        eye_size = 5
        pupil_width = 2
        pupil_height = 6
        
        # Position eyes based on direction for elongated head
        if direction == Direction.RIGHT:
            eye1_pos = (center_x + 6, center_y - 4)
            eye2_pos = (center_x + 6, center_y + 4)
        elif direction == Direction.LEFT:
            eye1_pos = (center_x - 6, center_y - 4)
            eye2_pos = (center_x - 6, center_y + 4)
        elif direction == Direction.UP:
            eye1_pos = (center_x - 4, center_y - 6)
            eye2_pos = (center_x + 4, center_y - 6)
        else:  # DOWN
            eye1_pos = (center_x - 4, center_y + 6)
            eye2_pos = (center_x + 4, center_y + 6)
        
        # Draw both eyes
        for eye_pos in [eye1_pos, eye2_pos]:
            # Eye socket shadow
            pygame.draw.circle(self.screen, (15, 60, 15), (eye_pos[0], eye_pos[1] + 1), eye_size + 1)
            
            # Eye white/sclera
            pygame.draw.circle(self.screen, (250, 250, 220), eye_pos, eye_size)
            
            # Iris with golden-green coloring
            pygame.draw.circle(self.screen, (180, 200, 60), eye_pos, eye_size - 1)
            pygame.draw.circle(self.screen, (160, 180, 40), eye_pos, eye_size - 2)
            
            # Vertical slit pupil
            pupil_rect = pygame.Rect(
                eye_pos[0] - pupil_width // 2,
                eye_pos[1] - pupil_height // 2,
                pupil_width,
                pupil_height
            )
            pygame.draw.ellipse(self.screen, (0, 0, 0), pupil_rect)
            
            # Eye shine
            shine_pos = (eye_pos[0] - 2, eye_pos[1] - 2)
            pygame.draw.circle(self.screen, (255, 255, 255), shine_pos, 2)
            small_shine_pos = (eye_pos[0] + 1, eye_pos[1] - 1)
            pygame.draw.circle(self.screen, (200, 200, 200), small_shine_pos, 1)
    
    def _draw_tongue(self, center_x: int, center_y: int, direction: Direction):
        """Draw a flickering forked tongue.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        # Tongue flickers based on time
        time_ms = pygame.time.get_ticks()
        tongue_visible = (time_ms // 300) % 3 != 0
        
        if not tongue_visible:
            return
        
        tongue_length = 10
        tongue_color = (220, 20, 60)
        
        # Position tongue based on direction
        if direction == Direction.RIGHT:
            tongue_start = (center_x + 8, center_y)
            tongue_end = (center_x + 8 + tongue_length, center_y)
            fork1_end = (center_x + 8 + tongue_length, center_y - 2)
            fork2_end = (center_x + 8 + tongue_length, center_y + 2)
        elif direction == Direction.LEFT:
            tongue_start = (center_x - 8, center_y)
            tongue_end = (center_x - 8 - tongue_length, center_y)
            fork1_end = (center_x - 8 - tongue_length, center_y - 2)
            fork2_end = (center_x - 8 - tongue_length, center_y + 2)
        elif direction == Direction.UP:
            tongue_start = (center_x, center_y - 8)
            tongue_end = (center_x, center_y - 8 - tongue_length)
            fork1_end = (center_x - 2, center_y - 8 - tongue_length)
            fork2_end = (center_x + 2, center_y - 8 - tongue_length)
        else:  # DOWN
            tongue_start = (center_x, center_y + 8)
            tongue_end = (center_x, center_y + 8 + tongue_length)
            fork1_end = (center_x - 2, center_y + 8 + tongue_length)
            fork2_end = (center_x + 2, center_y + 8 + tongue_length)
        
        # Draw tongue
        pygame.draw.line(self.screen, tongue_color, tongue_start, tongue_end, 2)
        pygame.draw.line(self.screen, tongue_color, tongue_end, fork1_end, 1)
        pygame.draw.line(self.screen, tongue_color, tongue_end, fork2_end, 1)
    
    def _draw_nostrils(self, center_x: int, center_y: int, direction: Direction):
        """Draw detailed nostrils.
        
        Args:
            center_x: Head center x position
            center_y: Head center y position
            direction: Snake's current direction
        """
        nostril_size = 2
        nostril_color = (10, 40, 10)
        
        # Position nostrils based on direction
        if direction == Direction.RIGHT:
            nostril1_pos = (center_x + 8, center_y - 3)
            nostril2_pos = (center_x + 8, center_y + 3)
        elif direction == Direction.LEFT:
            nostril1_pos = (center_x - 8, center_y - 3)
            nostril2_pos = (center_x - 8, center_y + 3)
        elif direction == Direction.UP:
            nostril1_pos = (center_x - 3, center_y - 8)
            nostril2_pos = (center_x + 3, center_y - 8)
        else:  # DOWN
            nostril1_pos = (center_x - 3, center_y + 8)
            nostril2_pos = (center_x + 3, center_y + 8)
        
        # Draw nostrils with depth
        for nostril_pos in [nostril1_pos, nostril2_pos]:
            # Nostril shadow for depth
            pygame.draw.circle(self.screen, (5, 20, 5), (nostril_pos[0], nostril_pos[1] + 1), nostril_size)
            # Main nostril
            pygame.draw.circle(self.screen, nostril_color, nostril_pos, nostril_size)
            # Inner nostril darkness
            pygame.draw.circle(self.screen, (0, 0, 0), nostril_pos, nostril_size - 1)


class SnakeScaleRenderer:
    """Handles rendering of snake scales and texture details."""
    
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
    
    def draw_scales(self, points: List[Tuple[int, int]]):
        """Draw green scale patterns with stripe effects.
        
        Args:
            points: Path points along the snake body
        """
        scale_spacing = 20
        time_ms = pygame.time.get_ticks()
        
        for i in range(0, len(points) - 1, scale_spacing):
            if i + 1 < len(points):
                point = points[i]
                
                # Calculate scale size based on position
                progress = i / max(1, len(points) - 1)
                base_scale_size = max(2, int(4 * (1.0 - progress * 0.4)))
                
                # Shimmer effect
                shimmer = math.sin((time_ms * 0.004) + (i * 0.15)) * 0.4 + 0.6
                scale_size = int(base_scale_size * shimmer)
                
                # Green scale coloring with stripe variation
                stripe_pattern = math.sin(i * 0.4) > 0.3
                stripe_intensity = 0.7 if stripe_pattern else 1.0
                
                self._draw_single_scale(point, scale_size, shimmer, stripe_intensity)
    
    def _draw_single_scale(self, point: Tuple[int, int], scale_size: int, 
                          shimmer: float, stripe_intensity: float):
        """Draw a single scale with proper coloring.
        
        Args:
            point: Scale position
            scale_size: Size of the scale
            shimmer: Shimmer intensity
            stripe_intensity: Stripe pattern intensity
        """
        base_green = int(80 * shimmer * stripe_intensity)
        bright_green = int(160 * shimmer * stripe_intensity)
        
        scale_alpha = int(90 * shimmer)
        scale_color = (int(base_green * 0.5), base_green, int(base_green * 0.5), scale_alpha)
        highlight_color = (int(bright_green * 0.6), bright_green, int(bright_green * 0.6), int(scale_alpha * 0.7))
        
        # Draw diamond scale
        scale_points = [
            (point[0] - scale_size, point[1]),
            (point[0], point[1] - scale_size),
            (point[0] + scale_size, point[1]),
            (point[0], point[1] + scale_size)
        ]
        
        # Create surface for alpha blending
        scale_surface = pygame.Surface((scale_size * 2 + 2, scale_size * 2 + 2), pygame.SRCALPHA)
        
        # Adjust points for surface coordinates
        surface_points = [(x - point[0] + scale_size + 1, y - point[1] + scale_size + 1) for x, y in scale_points]
        
        pygame.draw.polygon(scale_surface, scale_color, surface_points)
        
        # Add highlight
        if scale_size > 1:
            highlight_points = [(x - 1, y - 1) for x, y in surface_points]
            pygame.draw.polygon(scale_surface, highlight_color, highlight_points)
        
        self.screen.blit(scale_surface, (point[0] - scale_size - 1, point[1] - scale_size - 1))
