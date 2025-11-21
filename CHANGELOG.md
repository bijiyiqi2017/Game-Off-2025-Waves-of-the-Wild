# Changelog

All notable changes to this project will be documented in this file.  
This file is intended for **team use** to track development progress, new features, bug fixes, and refactors.

We follow **[Semantic Versioning](https://semver.org/)**:

- **MAJOR** version when you make incompatible API or gameplay changes  
- **MINOR** version when you add functionality in a backwards-compatible way  
- **PATCH** version when you make backwards-compatible bug fixes  

## Format
```text
## [version] - YYYY-MM-DD
- Added new feature
- Fixed bug
- Changed behavior

[1.1.0] – 2025-11-21
Added

Win screen triggered by collecting the winning banana.

Energy burst system with visual effects and temporary energy boost.

Background music and start sound integrated into gameplay.

Resizable title and win screens with dynamic text scaling.

Platforms, clouds, water hazard, and collectibles functionality maintained.

Changed

Refactored main.py to use state-driven gameplay loop (TITLE_SCREEN, PLAYING, GAME_OVER_STATE, WIN_STATE).

Removed undefined variables game_over and game_win; replaced with current_state.

Consolidated game screens and logic for smoother transitions.

Adjusted banana respawn logic and energy system mechanics.

Fixed

Ensured player cannot exceed max energy during energy bursts.

Fixed collisions with platforms and lake hazard while jumping.

Smooth pulsing "Press any key" animation on title screen.


[0.1.0-dev]

Added

Initialized README.md with basic project information.

Evaluating the integration of Pylint for code quality enforcement.

Next Steps

Continue refining README.md with detailed project descriptions.

Plan and implement Pylint setup in development environment.

[v0.1.0-dev] - 2025-11-08

Created topics and a brief description for the "about" section of the repository.

[v0.1] - 2025-11-07

Studied parallax effect and set clouds to move via parallax effect.

Fixed left and right key movements and created a tiger placeholder.

## [v0.1.0] - 2025-11-05

- Set up project structure and created Python virtual environment.

- Installed Pygame 2.6.1 and added core project files (.gitignore, LICENSE, README.md, CHANGELOG.md).

- Implemented basic Pygame window with sky, clouds, and jungle floor.