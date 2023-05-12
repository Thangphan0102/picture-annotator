import collections
import glob
import os
from typing import Any, Callable, Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET

from PIL import Image
from torchvision.datasets import VisionDataset

from src.config import *


class CustomDataset(VisionDataset):
    """ The custom dataset created using the images and saved annotations.

    Attributes:
        images (List[str]): The list contains all the image paths.
        targets (List[str]): The list contains all the annotation file paths.

    """

    def __init__(
            self,
            root_dir: str,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            transforms: Optional[Callable] = None,
    ):
        """ Initialize the CustomDataset instance

        Args:
            root_dir (str): The string represents the root (data) directory.
            transform (Optional[Callable]): The callable for transforming the images.
            target_transform (Optional[Callable]): The callable for transforming the targets.
            transforms (Optional[Callable]): The callable for transforming both the images and targets.
        """
        super().__init__(root_dir, transforms, transform, target_transform)

        image_dir = Path(root_dir).joinpath('images')
        self.images = []
        for extension in IMAGE_EXTENSIONS:
            self.images.extend(glob.glob(os.path.join(image_dir, extension)))

        target_dir = Path(root_dir).joinpath('annotations')
        self.targets = glob.glob(os.path.join(target_dir, '*.xml'))

        assert len(self.images) == len(self.targets)

    def __len__(self) -> int:
        """ The overwrite method __len__.

        The user can use, for example:
            ```
            my_dataset = CustomDataset(root, transform, target_transform, transforms)
            # To get the length of the dataset
            len(my_dataset)
            ```

        Returns:
            length (int): The length of the dataset.
        """
        return len(self.images)

    @property
    def annotations(self) -> List[str]:
        """ Get the annotations file paths.

        Returns:
            target_list (List[str]): The list containing the annotations file paths.
        """
        return self.targets

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        """ The overwrite method __getitem__

        The user can use, for example:
            ```
            my_dataset = CustomDataset(root, transform, target_transform, transforms)
            # To get the images and labels, you can use indexing
            images, labels = my_dataset[3]
            # image, labels = my_dataset[5:8]
            ```

        Args:
            index (int): The index

        Returns:
            images, labels (Tuple[Any, Any]): The images and labels of the dataset.
        """
        img = Image.open(self.images[index]).convert("RGB")
        target = self.parse_xml(ET.parse(self.annotations[index]).getroot())

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    @staticmethod
    def parse_xml(node: ET.Element) -> Dict[str, Any]:
        """ Parse the xml of the given node

        Args:
            node (ET.Element): An element of the xml tree.

        Returns:
            result_dict (Dict[str, Any]): The dictionary of node tags as keys and it texts as values.
        """
        result_dict: Dict[str, Any] = {}
        children = list(node)
        if children:
            def_dic: Dict[str, Any] = collections.defaultdict(list)
            for dc in map(CustomDataset.parse_xml, children):
                for ind, v in dc.items():
                    def_dic[ind].append(v)
            if node.tag == "annotation":
                def_dic["object"] = [def_dic["object"]]
            result_dict = {node.tag: {ind: v[0] if len(v) == 1 else v for ind, v in def_dic.items()}}
        if node.text:
            text = node.text.strip()
            if not children:
                result_dict[node.tag] = text
        return result_dict
