import collections
import glob
import os
from typing import Any, Callable, Dict, List, Optional, Tuple
from xml.etree.ElementTree import \
    Element, \
    parse as ET_parse

from PIL import Image
from torchvision.datasets import VisionDataset

from config import *


class CustomDataset(VisionDataset):
    """My custom dataset."""

    def __init__(
            self,
            root_dir: str,
            transform: Optional[Callable] = None,
            target_transform: Optional[Callable] = None,
            transforms: Optional[Callable] = None,
    ):
        super().__init__(root_dir, transforms, transform, target_transform)

        image_dir = Path(root_dir).joinpath('images')
        self.images = []
        for extension in IMAGE_EXTENSIONS:
            self.images.extend(glob.glob(os.path.join(image_dir, extension)))

        target_dir = Path(root_dir).joinpath('annotations')
        self.targets = glob.glob(os.path.join(target_dir, '*.xml'))

        print(len(self.images), len(self.targets))
        assert len(self.images) == len(self.targets)

    def __len__(self) -> int:
        return len(self.images)

    @property
    def annotations(self) -> List[str]:
        return self.targets

    def __getitem__(self, index: int) -> Tuple[Any, Any]:
        img = Image.open(self.images[index]).convert("RGB")
        target = self.parse_xml(ET_parse(self.annotations[index]).getroot())

        if self.transforms is not None:
            img, target = self.transforms(img, target)

        return img, target

    @staticmethod
    def parse_xml(node: Element) -> Dict[str, Any]:
        dict: Dict[str, Any] = {}
        children = list(node)
        if children:
            def_dic: Dict[str, Any] = collections.defaultdict(list)
            for dc in map(CustomDataset.parse_xml, children):
                for ind, v in dc.items():
                    def_dic[ind].append(v)
            if node.tag == "annotation":
                def_dic["object"] = [def_dic["object"]]
            dict = {node.tag: {ind: v[0] if len(v) == 1 else v for ind, v in def_dic.items()}}
        if node.text:
            text = node.text.strip()
            if not children:
                dict[node.tag] = text
        return dict
