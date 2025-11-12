# Game-Off-2025: Waves of the Wild  
### Developer Progress Log

This document tracks daily and weekly development progress for *Waves of the Wild*.  
It follows semantic versioning alignment with the project's `CHANGELOG.md` but is focused on developer milestones, experiments, and notes.

---


## 🗓️ November 10 2025 — Progress

- Fixed bug ~ Window screen resizing issue works properly now. Dug through Pygame's documentation for the answer.

## 🗓️ November 9 2025 — Progress

- README.md Initial content added; will be updated further as the project progresses.

- Pylint Integration: Considering adding Pylint to the project for improved code quality and consistency. Researching setup and best practices for integrating with VS Code and GitHub.

## 🗓️ November 8 2025 — Progress

- Created topics,and a brief description of the repo for the about section.



## 🗓️ November 7, 2025 — Progress

- Studied parallax effect & set clouds to move via parallax effect

- Fixed left and right key movements & created tiger placeholder.

## 🗓️ November 5, 2025 — Progress Entry
**Version:** 0.1.0-dev  
**Stage:** Initial setup and prototype foundation  

### Summary
- Initialized project structure in WSL2 environment.  
- Created Python virtual environment and installed Pygame 2.6.1.  
- Added `.gitignore`, `LICENSE`, `README.md`, and `CHANGELOG.md`.  
- Implemented base Pygame window with background sky, clouds, and jungle floor.  
- Added placeholder for player sprite (tiger) and structured movement logic comments for future expansion.  
- Verified rendering loop runs at 60 FPS without frame drops.  

### Next Steps
- Implement player movement for left/right inputs.  
- Add jump mechanic with gravity simulation.  
- Introduce collectible items (bananas) for energy system testing.  
- Begin sprite placeholder replacements and layout adjustments.  

---

### Notes
- `progress.md` is **not tracked in production** and should remain **developer-only**.  
- Version references should match or precede commits documented in `CHANGELOG.md`.  
