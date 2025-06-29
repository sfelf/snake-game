"""
Snake Game - Main Entry Point

Copyright (c) 2025 Thomas Nelson (https://github.com/sfelf)
Licensed under CC BY-NC-SA 4.0 (https://creativecommons.org/licenses/by-nc-sa/4.0/)
"""

import sys
from .controllers import GameController


def main():
    """Main function to run the Snake game."""
    try:
        game_controller = GameController()
        game_controller.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        sys.exit()


if __name__ == "__main__":
    main()
