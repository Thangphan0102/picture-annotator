# Picture annotator project - CS-A1121 - Basics of programing Y2

## Checkpoint 1

## Current properties

- I've implemented the basic UI for the program. The users can open it and choose a directory containing the pictures to
get started. Then they can choose which of the pictures they want to annotate from the left-hand view and draw rectangles
on the canvas in the middle.
- The program is still missing some features such as storing the annotations, creating a dataset, etc.

## Instructions

>Important! The user should have a directory that contains some pictures in these formats .png, .jpg, or .jpeg 

- The program can be executed by running the python file located at `src/UI.py`
- When a window pops up, navigate to the menu bar and select `File > Open file..` (or by pressing "Ctrl + O") then choose 
the directory where the pictures are located.
- Selecting the picture from the left-hand view displays it on the middle canvas.
- When the picture is on the canvas, the user can draw rectangles as bounding box on the picture by click and drag the
mouse then release when finished. A small window will pop up asking for the label name.
- The user can also use the shortcuts "Ctrl + Z" to undo the previous drawn rectangle, "Ctrl + R" to remove all rectangles,
and "Ctrl + D" to print all the labels into the console.

## Schedule

- I've spent about 2 weeks for coding the project.

## Other

- The problem that I'm facing now is I'm not sure which formats should I use to store the annotated labels.
- I've decided to implement the UI first, since the program is heavily related to the UI.