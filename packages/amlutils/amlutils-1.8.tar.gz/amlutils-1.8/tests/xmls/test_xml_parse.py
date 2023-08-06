from unittest.mock import patch
import numpy as np
import os
import random
import tempfile
import unittest

# project imports
from amlutils.xmls import (
    create,
    parse,
)


class TestXMLCreateParse(unittest.TestCase):

    def _get_bounding_boxes(self, num_boxes=5):
        return [[random.random() for j in range(4)] for i in range(num_boxes)]

    def _get_unnormalized_bounding_boxes(self, width, height, bounding_boxes):
        unnormalized_bounding_boxes = []
        for box in bounding_boxes:
            unnormalized_bounding_boxes.append([
                int(box[0] * width),
                int(box[1] * height),
                int(box[2] * width),
                int(box[3] * height),
            ])
        return unnormalized_bounding_boxes

    @patch('amlutils.xmls.create.cv2.imread')
    def test_create_xml(self, mock_imread):
        label_to_box_annotations = {
            "label_{}".format(i): self._get_bounding_boxes(3)
            for i in range(5)
        }
        image_file_path = "/directory/does/not/exist/dummy_image.jpeg"
        width = 100
        height = 100
        mock_imread.return_value = np.ndarray((height, width, 3))
        xml_file_path = tempfile.NamedTemporaryFile(suffix=".xml").name
        create.store_od_annotations_to_xml(image_file_path, xml_file_path, label_to_box_annotations, normalized_coordinates=True)
        xml_parser = parse.XMLParser(xml_file_path)
        parsed_boxes = xml_parser.get_object_labels_to_bounding_boxes()
        self.assertEqual(
            parsed_boxes,
            {
                label: self._get_unnormalized_bounding_boxes(width, height, bounding_boxes)
                for label, bounding_boxes in label_to_box_annotations.items()
            }
        )
        self.assertEqual(os.path.basename(image_file_path), xml_parser.get_file_name())
        self.assertEqual({"label_{}".format(i) for i in range(5)}, xml_parser.get_object_labels())


if __name__ == '__main__':
    unittest.main()
