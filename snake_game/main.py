"""Main entry point for the Snake game."""

import sys
from .game import SnakeGame


def main():
    """Main function to run the Snake game."""
    try:
        game = SnakeGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sys.exit()


if __name__ == "__main__":
    main()
