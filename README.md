# Picture annotator project - CS-A1121 - Basics of programing Y2

## Introduction

The Picture Annotator is a software application designed for users to easily add annotations to their pictures. With 
this program, users can easily select an image, add annotations, and export them as a dataset used to train a deep 
learning model for object detection task. It is user-friendly, intuitive, and efficient in managing images, making it a 
valuable tool for any individuals.

## File and directory structure

y2_2023_08713_picture_annotator/
├─ data/
│  ├─ annotations/
├─ doc/
│  ├─ project_plan.pdf
│  ├─ project_document.pdf
├─ src/
│  ├─ menu_bar.py
│  ├─ file_list.py
│  ├─ file_view.py
│  ├─ filter_widget.py
│  ├─ graphics_view.py
│  ├─ image.py
│  ├─ UI.py
│  ├─ canvas.py
│  ├── config.py
│  ├── writer.py
├── .gitignore
├── dataset.py
├── README.md
└── requirements.txt

## Installation instructions

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

- Put images into the folder `picture_annotator/y2_2023_08713_picture_annotator/data/images`

- Run the program by running

```commandline
python3 src/UI.py
```

## User instructions

- When a window pops up, navigate to the menu bar and select `File > Open file..` (or by pressing "Ctrl + O") then choose 
the directory where the pictures are located.
- Selecting the picture from the left-hand view displays it on the middle canvas.
- When the picture is on the canvas, the user can press "Ctrl + D" to switch to drawing mode from viewing mode (as 
default). After switched to drawing mode, the user can draw rectangles as bounding box on the picture by left click and 
drag the mouse then release when finished. A small window will pop up asking for the label name. After entered the name, 
another window might pop up asking the user to select a color. After a color is chosen, a rectangle will be drawn on the 
canvas, and also the entered label will appear on the right-hand side under the "Label list" area. The user can click on 
the checkboxes to hide or display the corresponding bounding boxes.
- When all the annotations are done, press "Ctrl + S" to save the annotations. The annotation files can be found in the 
`picture_annotator/y2_2023_08713_picture_annotator/data/annotations` directory.
- Select the next images from the file list in the left and repeat the annotation process.
- When finished annotating all the images, define your deep learning model file and store it in the directory 
`picture_annotator/y2_2023_08713_picture_annotator/` then add `from dataset import CustomDataset` to your file. Create
an instance follows the parameters used in the class. Load it with the data loader of Pytorch and train your model. 

**Shortcuts**

| Shortcut | Short name | Action                                                      |
|----------|------------|-------------------------------------------------------------|
| Ctrl + Z | Undo       | Remove the last bounding box that was drawn on the canvas   |
| Ctrl + R | Reset      | Remove all the bounding boxes that were drawn on the canvas |
| Ctrl + S | Save       | Save the annotations into a file                            |
| Ctrl + G | Print      | Print the labels into the console                           |
| Ctrl + D | Draw       | Switch to drawing mode                                      |
| Ctrl + V | View       | Switch to viewing mode                                      |