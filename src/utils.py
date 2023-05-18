import collections
from typing import Dict, Any, List, Tuple

import xml.etree.ElementTree as ET

try:
    from PyQt6.QtGui import QColor
except ImportError:
    raise ImportError("Requires PyQt6")


def parse_xml(node: ET.Element) -> Dict[str, Any]:
    """ Parse the xml of the given node

    Args:
        node (ET.Element): An element of the xml tree.

    Returns:
        result_dict (Dict[str, Any]): The dictionary of node tags as keys, and it texts as values.
    """
    result_dict: Dict[str, Any] = {}
    children = list(node)
    if children:
        def_dic: Dict[str, Any] = collections.defaultdict(list)
        for dc in map(parse_xml, children):
            for ind, v in dc.items():
                def_dic[ind].append(v)
        if node.tag == "annotation":
            def_dic["object"] = [def_dic["object"]]
        result_dict = {node.tag: {ind: v[0] if len(v) == 1 else v for ind, v in def_dic.items()}}
    if node.text:
        text = node.text.strip()
        if not children:
            result_dict[node.tag] = text
    if node.tag == "color_dict":
        result_dict[node.tag] = node.attrib
    return result_dict


def parse_annotation_dict(result_dict: Dict[str, Any]) -> \
        Tuple[
            List[str],
            List[Tuple[int, int, int, int]],
            Dict[str, QColor]
        ]:
    """ Parse the result_dict of the parse_xml function into labels, bounding boxes, and label_color_dict

    Args:
        result_dict (Dict[str, Any]): The dictionary returned from the parse_xml function

    Returns:
        Tuple[labels, bounding_boxes, label_color_dict]
    """
    # Get the objects
    objects = result_dict["annotation"]["object"]
    dict_list = result_dict["annotation"]["color_dict"]

    # Collect data
    labels = []
    bounding_boxes = []
    label_color_dict = {}

    for obj in objects:
        bounding_box = obj["bndbox"]
        xmin = int(bounding_box["xmin"])
        xmax = int(bounding_box["xmax"])
        ymin = int(bounding_box["ymin"])
        ymax = int(bounding_box["ymax"])

        bounding_boxes.append((xmin, ymin, xmax, ymax))

        labels.append(obj["name"])

    if len(dict_list) > 1:
        for dic in dict_list:
            label_color_dict.update(dic)
    else:
        label_color_dict = dict_list

    return labels, bounding_boxes, label_color_dict
