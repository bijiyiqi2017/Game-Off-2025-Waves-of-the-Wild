# Game-Off-2025: Waves of the Wild  
### Developer Progress Log

This document tracks daily and weekly development progress for *Waves of the Wild*.  
It follows semantic versioning alignment with the project's `CHANGELOG.md` but is focused on developer milestones, experiments, and notes.

---


## 🗓️ November 27, 2025

- Added audio to wave of energy burst

- Replace placeholder with one_banana.jpg

## 🗓️ November 26, 2025

- Added audio to win screen 

## 🗓️ November 25, 2025

- Reverted code to previous version in order to simplify for game off and slowly break main.py into smaller packages

## 🗓️ November 24, 2025

- Started to separate main.py into smaller packages

## 🗓️ November 22, 2025

- Added audio files & sprite images from Chen Bao
- Linked jump action to audio file


## 🗓️ November 21, 2025

- Added platforms, and adjusted heights
- Adjusted energy drain speed
- Relocated the win screen trigger banana
- Merged pull request & fix broken issuess
- Updated CHANGELOG


## 🗓️ November 20, 2025

- Created waves of energy text on screen and burst of energy in energy bar (5 burts of 4)

## 🗓️ November 18, 2025

- Created simple text win screen and center text

## 🗓️ November 17, 2025

- Removed extra jump code to fix broken jump mechanics 

## 🗓️ November 16, 2025

- Cherry picked platforms

## 🗓️ November 15, 2025

- Created rectangle blue lake ~ Tiger speed slows down when it touches the water. 

## 🗓️ November 14, 2025

- Push and merged energy-system branch to remote

- Created pylint.yml & .pylintrc and pulled (GitHub workflows)

- 

## 🗓️ November 13, 2025 

- Create new branch energy-system


## 🗓️ November 12 2025 

- Created TeamMembers.md

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
