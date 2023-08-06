import cv2
import os
import typing
import xml.etree.ElementTree as ET


def get_xml_name_for_image(image_identifier: str) -> str:
    """generate the xml name for the given image identifier(full_path or only file_name)
    useful for generating OD annotations file name for the image

    Parameters
    ----------
    image_identifier: str
        can be the full image path or just the image name for which the xml name needs to be generated

    Returns
    -------
    str
        The xml file name only ending in .xml extension
    """
    _, image_name = os.path.split(image_identifier)
    image_name, _ = os.path.splitext(image_name)
    return image_name + ".xml"


def store_od_annotations_to_xml(
    image_file_path: str,
    xml_file_path: str,
    label_to_box_annotations: typing.Dict[str, typing.List[typing.List[float]]],
    normalized_coordinates: typing.Optional[bool] = False,
):
    """
    given the Object Detection bounding box coordinates and labels, generate
    a XML file for Object Detection Training

    Parameters
    ----------
    image_file_path: str
        full path to image for which the xml annotations need to be stored
    xml_file_path: str
        full path to where new xml file should be created
    class_to_box_annotations: Dict[str, List[(int, int, int, int)]]
        A dictionary of containing the object_label and coordinates of bounding box
        coordinate format [xmin, ymin, xmax, ymax]
    normalized_coordinates: Optional[bool], default=False
        whether the bounding box coordinates are normalized or not, if normalized they
        will be multiplied by the width and height of the image.
    """
    folder, filename = os.path.split(image_file_path)
    annotation = ET.Element("annotation")
    ET.SubElement(annotation, "folder").text = folder
    ET.SubElement(annotation, "filename").text = filename
    ET.SubElement(annotation, "path").text = os.path.join(folder, filename)

    source = ET.SubElement(annotation, "source")
    ET.SubElement(source, "database").text = "Unknown"

    size = ET.SubElement(annotation, "size")
    height, width = cv2.imread(image_file_path).shape[:2]
    ET.SubElement(size, "width").text = str(width)
    ET.SubElement(size, "height").text = str(height)
    ET.SubElement(size, "depth").text = "3"

    ET.SubElement(annotation, "segmented").text = "0"

    for class_name, bbs in label_to_box_annotations.items():
        for bb in bbs:
            e_object = ET.SubElement(annotation, "object")
            ET.SubElement(e_object, "name").text = str(class_name)
            ET.SubElement(e_object, "pose").text = "Unspecified"
            ET.SubElement(e_object, "truncated").text = "0"
            ET.SubElement(e_object, "difficult").text = "0"
            bnd_box = ET.SubElement(e_object, "bndbox")
            if normalized_coordinates:
                ET.SubElement(bnd_box, "xmin").text = str(int(bb[0] * width))
                ET.SubElement(bnd_box, "ymin").text = str(int(bb[1] * height))
                ET.SubElement(bnd_box, "xmax").text = str(int(bb[2] * width))
                ET.SubElement(bnd_box, "ymax").text = str(int(bb[3] * height))
            else:
                ET.SubElement(bnd_box, "xmin").text = str(int(bb[0]))
                ET.SubElement(bnd_box, "ymin").text = str(int(bb[1]))
                ET.SubElement(bnd_box, "xmax").text = str(int(bb[2]))
                ET.SubElement(bnd_box, "ymax").text = str(int(bb[3]))

    tree = ET.ElementTree(annotation)
    tree.write(xml_file_path)
