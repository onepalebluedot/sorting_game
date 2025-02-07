# sorting_game

# Shape Sorting Game in Python (Pygame)

A simple shape-sorting game built with **Pygame**. The game displays four draggable shapes (square, triangle, heart, star) at the bottom of the screen and four corresponding “cutouts” (placeholders) near the top. The player drags each shape to its matching placeholder. When a shape is placed correctly, the game briefly shows a **“CORRECT!”** message at the top. There is also a **Restart** button to reset the game at any time.

---

## Features
1. **4 Shapes:** Square, Triangle, Heart, Star – each with a distinct color.  
2. **Matching Cutouts:** The cutouts at the top visually match each shape.  
3. **Click and Drag:** Use the mouse to drag shapes around.  
4. **Correct Placement Feedback:** When you drop a shape on its correct cutout, it snaps into place and displays **“CORRECT!”** for a short duration.  
5. **Restart Button:** Resets all shapes back to their original positions.

---

## Requirements
- **Python 3.6+** (or any modern Python 3 version)
- **Pygame** (tested on version 2.0+)

To install or upgrade Pygame:
```bash
python3 -m pip install --upgrade pip
python3 -m pip install pygame
```
## How to Run

1.	Clone or download this repository.
2.	Open a terminal or command prompt in the project folder.
3.	Run:
 
```
python3 shape_sorting_game.py
```
## Gameplay Instructions
1.	Left-click on a shape to pick it up.
2.	Drag the shape to one of the cutouts at the top.
3.	Release the mouse button to drop the shape.
	•	If you placed it correctly, the cutout gets filled and “CORRECT!” is displayed briefly.
	•	If incorrect, nothing happens and the shape remains draggable.
4.	Restart the game at any time by clicking the “Restart” button at the top-right corner.



