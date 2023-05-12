"""
    This module contains code to test 'kuva-annotaattori'
    project for Y2 CS-A1121.

    The training produces torch model which can be loaded
    with `faster_rcnn` function to create a production model.

    See all `TODO:` labels.

    Changes:
        0.0.1 Runnable version
"""

import os
from time import time

import torch
import torchvision as tv
from PIL import ImageDraw

from dataset import CustomDataset

__authors__ = ("Otso Brummer",)
__date__ = "23.3.2021"
__version__ = "0.0.1"

MODEL_SAVEPATH = "model.pth"
EXPORT_FOLDER = "export"


def faster_rcnn(num_classes, load=False):
    """
        Creates torchvision fasterrcnn_resnet50_fpn
        model with number of classes given

        Args:
            num_classes (int): Number of export classes
                including background
        Returns:
            Torchvision Faster RCNN model
    """
    model = tv.models.detection.fasterrcnn_resnet50_fpn(
        num_classes=num_classes
    )

    if load:
        model.load_state_dict(torch.load(MODEL_SAVEPATH))
    return model


def create_device():
    """
        Create torch device with GPU if available

        Returns:
            Cuda device if available, otherwise CPU device.
    """
    return torch.device("cuda:0" if torch.cuda.is_available() else "cpu")


def collate(batch):
    """
        Dataset returns values in
        (img, boxes) (img, boxes) manner but it is required
        to (img, img) (boxes, boxes) form. Function
        does this transform.

        Args:
            batch (tuple): Iterable of (img, box) tuples

        Returns:
            Iterable of ((img,...), (box,...))
    """
    return tuple(zip(*batch))


def train_rcnn(dataset, model, epochs=10, lr=1e-5):
    """
        Train rcnn with provided dataset and save to
        defined model path.

        Args:
            dataset (Dataset): Training dataset
            model (Module): RCNN torch module
            epochs (int): How many epochs to run
            lr (float): Learning rate to be used
    """
    device = create_device()
    # DataLoader class handles parallelization
    # in torch
    dataloader = torch.utils.data.DataLoader(
        dataset=dataset,
        batch_size=1,
        shuffle=True,
        pin_memory="cuda" in device.type,
        num_workers=1,
        collate_fn=collate
    )

    model = model.to(device)
    # Optimizer tries to
    # change kernel values to optinum
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=lr
    )
    # Start time used in prints
    start = time()

    print(f"Starting training with dataset sized {len(dataset)}")

    for epoch in range(epochs):
        epoch_loss = .0

        for index, (img, targets) in enumerate(dataloader):
            # The img and targets are list of values
            # Here we move them to used device
            img = [item.to(device) for item in img]
            for target in targets:
                for key in target:
                    target[key] = target[key].to(device)

            optimizer.zero_grad()

            output = model(img, targets)

            # Sum of
            # loss_classifier
            # loss_box_reg
            # loss_objective
            # loss_rpn_box_reg
            losses = sum(output.values())

            losses.backward()
            optimizer.step()
            epoch_loss += float(losses.item())

            # TODO: You can remove this if you like
            # This is a heavy model so break the training early
            # if index > 10:
            #     break
        minutes = int((time() - start) // 60)
        seconds = (time() - start) % 60
        print(
            f"Epoch {epoch + 1}: Elapsed {minutes:2d}:{seconds:2.2f}, loss {epoch_loss:.2f}")

    torch.save(model.state_dict(), MODEL_SAVEPATH)


# The drawing constants
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# Usually score has mininum accepted threshold. Feel free to change this
# to see your responses.
SCORE_LIMIT = 0.5


def evaluate_dataset(dataset, model):
    """
        Exports model evaluations and ground truths
        on given dataset to evaluation folder

        Args:
            dataset (Dataset): Torch dataset to be evaluated
            model (Module): Torch module to use
    """
    print("Evaluating images")
    # Move to production mode
    model.eval()

    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    # Pil transformation function
    to_pil = tv.transforms.ToPILImage()

    # Disable autograd. Makes code faster
    with torch.no_grad():
        for index, (img, target) in enumerate(dataset):
            # The model expects and returns a list
            response = model([img])[0]
            # Transform to normal image
            pil = to_pil(img)
            # PIL drawer
            draw = ImageDraw.Draw(pil)
            # Iterate all guesses and draw them to image
            for guess_box, label, score in zip(response["boxes"], response["labels"], response["scores"]):
                if score < SCORE_LIMIT:
                    continue

                draw.rectangle(
                    tuple(map(int, guess_box)),
                    outline=BLUE
                )
                draw.text((guess_box[0], guess_box[1]),
                          f"{int(label)} {float(score):.2f}")
            # Print also the ground truths to the image
            for gt, label in zip(target["boxes"], target["labels"]):
                draw.rectangle(
                    tuple(map(int, gt)),
                    outline=GREEN
                )
                draw.text((gt[0], gt[1]), f"{int(label)}")

            pil.save(f"{EXPORT_FOLDER}/image{index}.png")
            # TODO: There are a lot of images. You can change this if you like.
            # if index > 10:
            #     break


# Rest of the module handles usage of the VOCDection torchvision
# dataset and might be useful when creating your own dataset

CLASS_DICT = {
    "background": 0,
    "cat": 1
}


def target_transform(target):
    """
        This function is required to
        parse VOC XML info from
        torchvision dataset class

        Args:
            target (dict): Dictionary as given by VOCDetections dataset

        Returns:
            Dictionary with keys 'boxes' and 'labels'
            and their respective boxes
    """
    # Seek relevant objects from XML
    objs = target["annotation"]["object"]
    # Collect all data to lists
    labels = []
    boxes = []
    for obj in objs:
        bbox = obj["bndbox"]
        xmin = int(bbox["xmin"])
        xmax = int(bbox["xmax"])
        ymin = int(bbox["ymin"])
        ymax = int(bbox["ymax"])

        boxes.append(
            (
                xmin,
                ymin,
                xmax,
                ymax,
            )
        )

        label_name = obj["name"]
        label = CLASS_DICT[label_name]
        labels.append(label)

    # Transform to dataset target element
    return {
        "boxes": torch.tensor(
            boxes,
            dtype=torch.float32
        ),
        "labels": torch.tensor(
            labels,
            dtype=torch.int64
        ),
    }


if __name__ == "__main__":
    # TODO: Remove and add your own dataset
    dataset = CustomDataset(
        root_dir='./data',
        transform=tv.transforms.ToTensor(),
        target_transform=target_transform
    )
    # TODO: Change amount of classes in your dataset here
    # The background has label 0 and is one of the classes
    model = faster_rcnn(len(CLASS_DICT))
    train_rcnn(dataset, model)
    print("Training done")
    # Test load
    model = faster_rcnn(len(CLASS_DICT), load=True)
    # Export images
    evaluate_dataset(dataset, model)
