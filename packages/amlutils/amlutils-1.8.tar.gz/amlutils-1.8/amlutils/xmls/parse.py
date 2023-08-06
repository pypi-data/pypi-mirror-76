"""Utility functions for parsing Pascal VOC XML Formats"""

import typing
import xml.etree.ElementTree as ET

from enum import Enum


class TopLevelXMLFields(Enum):
    FOLDER = "folder"
    FILE_NAME = "filename"
    PATH = "path"
    SIZE = "size"
    OBJECT = "object"


class ObjectXMLFields(Enum):
    NAME = "name"
    POSE = "pose"
    TRUNCATED = "truncated"
    DIFFICULT = "difficult"
    BOUNDING_BOX = "bndbox"


class BoundingBoxXMLFields(Enum):
    XMIN = 0
    YMIN = 1
    XMAX = 2
    YMAX = 3


class Annotation:
    def __init__(self, field_to_value: typing.Dict[str, typing.Any]) -> None:
        self.label: str = field_to_value.get("name", None)
        self.bounding_box: typing.List[float] = field_to_value.get("bndbox", [])


class XMLParser:
    def __init__(self, xml_path: str) -> None:
        """Helper class for parsing object detection xml files

        Parameters
        ----------
        xml_path : str
            path to xml file that needs to be parsed
        """
        self.xml_path = xml_path
        self.xml_tree = ET.parse(xml_path)
        self.xml_root = self.xml_tree.getroot()
        self.annotations: typing.List[Annotation] = self._get_object_fields()

    def get_file_name(self) -> str:
        """get image file name corresponding to xml file

        Returns
        -------
        str
            image file name associated with this xml

        Raises
        ------
        ValueError
            incorrectly formatted xml file with multiple image file names
        """
        file_names = set()
        for member in self.xml_root.findall(TopLevelXMLFields.FILE_NAME.value):
            file_names.add(member.text)
        if len(file_names) != 1:
            raise ValueError("Found multiple file names({}) in xml".format(file_names))
        return list(file_names)[0]

    def _get_object_fields(self) -> typing.List[Annotation]:
        """method to get an Annotation representation of all objects in xml file

        Returns
        -------
        typing.List[Annotation]
            list of Annotation's that are present in the xml file
        """
        annotations = []
        bounding_box_field_map = {field.name.lower(): field.value for field in BoundingBoxXMLFields}
        for member in self.xml_root.findall(TopLevelXMLFields.OBJECT.value):
            annotation = {}
            for child in member.getchildren():
                if child.tag == ObjectXMLFields.BOUNDING_BOX.value:
                    bounding_box = [None] * 4
                    for sub_child in child.getchildren():
                        bounding_box[bounding_box_field_map[sub_child.tag]] = int(sub_child.text)
                    annotation[child.tag] = bounding_box
                    continue
                else:
                    field_name = child.tag
                    field_value = child.text
                    annotation[field_name] = field_value

            annotations.append(Annotation(annotation))
        return annotations

    def get_object_labels(self) -> typing.Set[str]:
        """get set of all unique labels present in the xml file

        Returns
        -------
        typing.Set[str]
            set of unique labels from xml file
        """
        return set([annotation.label for annotation in self.annotations])

    def get_object_labels_to_bounding_boxes(self) -> typing.Dict[str, typing.List[typing.List[float]]]:
        """Returns a dictionary of labels to list of bounding boxes for that label

        Returns
        -------
        typing.Dict[str, typing.List[typing.List[float]]]
            dictionary of label and list of its bounding boxes from the xml
        """
        object_to_bounding_boxes = {}
        for annotation in self.annotations:
            if annotation.label not in object_to_bounding_boxes.keys():
                object_to_bounding_boxes[annotation.label] = []
            object_to_bounding_boxes[annotation.label].append(annotation.bounding_box)
        return object_to_bounding_boxes
