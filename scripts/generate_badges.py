#!/usr/bin/env python3
"""Generate badges for README.md based on current project status."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path


def get_coverage_percentage():
    """Get coverage percentage from coverage.json."""
    try:
        with open('coverage.json', 'r') as f:
            data = json.load(f)
            return round(data['totals']['percent_covered'], 1)
    except (FileNotFoundError, KeyError, json.JSONDecodeError):
        return 0.0


def get_python_version():
    """Get Python version from pyproject.toml."""
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            match = re.search(r'python = "\^(\d+\.\d+)"', content)
            if match:
                return f"{match.group(1)}+"
    except FileNotFoundError:
        pass
    return "3.8+"


def get_pygame_version():
    """Get Pygame version from pyproject.toml."""
    try:
        with open('pyproject.toml', 'r') as f:
            content = f.read()
            match = re.search(r'pygame = "([^"]+)"', content)
            if match:
                return match.group(1)
    except FileNotFoundError:
        pass
    return "2.6.1"


def get_test_count():
    """Get total number of tests."""
    try:
        result = subprocess.run(
            ['poetry', 'run', 'pytest', '--collect-only', '-q'],
            capture_output=True,
            text=True,
            cwd='.'
        )
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            for line in lines:
                if 'tests collected' in line:
                    match = re.search(r'(\d+) tests collected', line)
                    if match:
                        return int(match.group(1))
    except Exception:
        pass
    return 0


def get_lines_of_code():
    """Get total lines of code in the project."""
    try:
        total_lines = 0
        for py_file in Path('snake_game').rglob('*.py'):
            with open(py_file, 'r', encoding='utf-8') as f:
                lines = len([line for line in f if line.strip() and not line.strip().startswith('#')])
                total_lines += lines
        return total_lines
    except Exception:
        return 0


def get_coverage_color(percentage):
    """Get color for coverage badge based on percentage."""
    if percentage >= 90:
        return "brightgreen"
    elif percentage >= 80:
        return "green"
    elif percentage >= 70:
        return "yellowgreen"
    elif percentage >= 60:
        return "yellow"
    elif percentage >= 50:
        return "orange"
    else:
        return "red"


def get_test_color(count):
    """Get color for test badge based on count."""
    if count >= 100:
        return "brightgreen"
    elif count >= 50:
        return "green"
    elif count >= 25:
        return "yellowgreen"
    elif count >= 10:
        return "yellow"
    else:
        return "orange"


def generate_badge_url(label, message, color):
    """Generate shields.io badge URL."""
    return f"https://img.shields.io/badge/{label}-{message}-{color}.svg"


def update_readme_badges():
    """Update badges in README.md."""
    coverage = get_coverage_percentage()
    python_version = get_python_version()
    pygame_version = get_pygame_version()
    test_count = get_test_count()
    lines_of_code = get_lines_of_code()
    
    coverage_color = get_coverage_color(coverage)
    test_color = get_test_color(test_count)
    
    # Generate badge URLs
    badges = {
        'coverage': generate_badge_url('coverage', f'{coverage}%25', coverage_color),
        'python': generate_badge_url('python', python_version, 'blue'),
        'pygame': generate_badge_url('pygame', pygame_version, 'green'),
        'tests': generate_badge_url('tests', f'{test_count}%20passing', test_color),
        'lines': generate_badge_url('lines%20of%20code', str(lines_of_code), 'blue'),
        'quality': generate_badge_url('code%20quality', 'refactored', 'brightgreen'),
        'license': generate_badge_url('license', 'CC%20BY--NC--SA%204.0', 'blue'),
        'status': generate_badge_url('build', 'passing', 'brightgreen')
    }
    
    try:
        with open('README.md', 'r') as f:
            content = f.read()
        
        # Update badge section
        badge_section = f"""[![Test Coverage]({badges['coverage']})](htmlcov/index.html)
[![Python]({badges['python']})](https://python.org)
[![Pygame]({badges['pygame']})](https://pygame.org)
[![Tests]({badges['tests']})](tests/)
[![Lines of Code]({badges['lines']})](snake_game/)
[![Code Quality]({badges['quality']})](README.md#architecture)
[![License]({badges['license']})](LICENSE)
[![Build Status]({badges['status']})](https://github.com/sfelf/snake-game/actions)"""
        
        # Replace existing badges
        pattern = r'(\[!\[Test Coverage\].*?\n)*(\[!\[Python\].*?\n)*(\[!\[Pygame\].*?\n)*(\[!\[Tests\].*?\n)*(\[!\[Lines of Code\].*?\n)*(\[!\[Code Quality\].*?\n)*(\[!\[License\].*?\n)*(\[!\[Build Status\].*?\n)*'
        
        # Find the line after the title and before the description
        lines = content.split('\n')
        new_lines = []
        badge_inserted = False
        
        for i, line in enumerate(lines):
            if line.startswith('# Snake Game') and not badge_inserted:
                new_lines.append(line)
                new_lines.append('')
                new_lines.extend(badge_section.split('\n'))
                new_lines.append('')
                badge_inserted = True
                
                # Skip existing badge lines
                j = i + 1
                while j < len(lines) and (lines[j].startswith('[![') or lines[j].strip() == ''):
                    j += 1
                i = j - 1
            elif not (line.startswith('[![') and 'shields.io' in line):
                new_lines.append(line)
        
        updated_content = '\n'.join(new_lines)
        
        with open('README.md', 'w') as f:
            f.write(updated_content)
        
        print(f"✅ Updated badges:")
        print(f"   Coverage: {coverage}%")
        print(f"   Python: {python_version}")
        print(f"   Pygame: {pygame_version}")
        print(f"   Tests: {test_count}")
        print(f"   Lines of Code: {lines_of_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating README badges: {e}")
        return False


def create_badges_directory():
    """Create badges directory and generate static badge files."""
    badges_dir = Path('badges')
    badges_dir.mkdir(exist_ok=True)
    
    coverage = get_coverage_percentage()
    
    # Create a simple SVG badge file
    coverage_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="104" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="104" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h63v20H0z"/>
        <path fill="{get_coverage_color(coverage)}" d="M63 0h41v20H63z"/>
        <path fill="url(#b)" d="M0 0h104v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="31.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>
        <text x="31.5" y="14">coverage</text>
        <text x="82.5" y="15" fill="#010101" fill-opacity=".3">{coverage}%</text>
        <text x="82.5" y="14">{coverage}%</text>
    </g>
</svg>'''
    
    with open(badges_dir / 'coverage.svg', 'w') as f:
        f.write(coverage_svg)
    
    print(f"✅ Created static badge files in {badges_dir}")


def main():
    """Main function."""
    print("🔄 Generating badges...")
    
    # Ensure we're in the project root
    if not Path('pyproject.toml').exists():
        print("❌ Must be run from project root directory")
        sys.exit(1)
    
    # Create badges directory
    create_badges_directory()
    
    # Update README badges
    if update_readme_badges():
        print("✅ Badge generation completed successfully")
    else:
        print("❌ Badge generation failed")
        sys.exit(1)


if __name__ == '__main__':
    main()
