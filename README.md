# Picture annotator project - CS-A1121 - Basics of programing Y2

## Checkpoint 1

## Current properties

- I've implemented the basic UI for the program. The users can open it and choose a directory containing the pictures to
get started. Then they can choose which of the pictures they want to annotate from the left-hand view and draw rectangles
on the canvas in the middle.
- The program is still missing some features such as storing the annotations, creating a dataset, etc.

## Instructions

>Important! The user must create a directory called `data`. In the `data` directory that you just have created, create 2
> directories, one called `annotaions` and the other can be `images` where you store pictures in these formats .png, 
> .jpg, or .jpeg.

- Start by creating a directory with its name such as `picture_annotator`.

```commandline
mkdir picture_annotator
cd picture_annotator
```

- Clone the repository.

```commandline
git clone git@version.aalto.fi:phanct1/y2_2023_08713_picture_annotator.git
cd y2_2023_08713_picture_annotator
```

- Next, create a virtual environment, activate it, and install the requirement packages

```commandline
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

- Run the program by running

```commandline
python3 src/UI.py
```

- When a window pops up, navigate to the menu bar and select `File > Open file..` (or by pressing "Ctrl + O") then choose 
the directory where the pictures are located.
- Selecting the picture from the left-hand view displays it on the middle canvas.
- When the picture is on the canvas, the user can press "Ctrl + D" to switch to drawing mode from viewing mode (as 
default). After switched to drawing mode, the user can draw rectangles as bounding box on the picture by click and drag the
mouse then release when finished. A small window will pop up asking for the label name. After entered the name, another
window might pop up asking the user to select a color. After a color is chosen, a rectangle will be drawn on the canvas,
and also the entered label will appear on the right-hand side under the "Label list" area. The user can click on the
checkboxes to hide or display the corresponding bounding boxes.

**Shortcuts**

| Shortcut | Short name | Action                                                      |
|----------|------------|-------------------------------------------------------------|
| Ctrl + Z | Undo       | Remove the last bounding box that was drawn on the canvas   |
| Ctrl + R | Reset      | Remove all the bounding boxes that were drawn on the canvas |
| Ctrl + S | Save       | Save the annotations into a file                            |
| Ctrl + G | Print      | Print the labels into the console                           |
| Ctrl + D | Draw       | Switch to drawing mode                                      |
| Ctrl + V | View       | Switch to viewing mode                                      |

## Schedule

- I've spent about 2 weeks for coding the project.

## Other

- The problem that I'm facing now is I'm not sure which formats should I use to store the annotated labels.
- I've decided to implement the UI first, since the program is heavily related to the UI.

## Checkpoint 2

### Current properties

- Added some new features for the program such as selecting different colors for different labels, guidelines.
- The users now can save the annotations and use them for their object detection program.

### Schedule

- I've spent 2 weeks for implementing new features into the project.

### Other

- I'll start to write some tests for the project, but I'm not sure how to write them. I've tried to avoid errors and
- bugs when I wrote the project's code. So far, everything is still working nicely, so I'm a bit confused. 