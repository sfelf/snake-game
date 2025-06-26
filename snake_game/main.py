"""Main entry point for the Snake game."""

import pygame
import sys


def main():
    """Main function to run the Snake game."""
    print("Snake Game starting...")
    print(f"Pygame version: {pygame.version.ver}")
    
    # Initialize pygame
    pygame.init()
    
    # Basic game window setup
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Snake Game")
    clock = pygame.time.Clock()
    
    # Game loop placeholder
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Fill screen with black
        screen.fill((0, 0, 0))
        
        # Update display
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
