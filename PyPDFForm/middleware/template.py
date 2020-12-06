# -*- coding: utf-8 -*-

from typing import Dict, List

import pdfrw

from .constants import Template as TemplateConstants
from .element import Element, ElementType
from .exceptions.template import InvalidTemplateError


class Template(object):
    @staticmethod
    def validate_stream(pdf_stream: bytes) -> None:
        """Validate if a template stream is indeed a PDF stream."""

        if b"%PDF" not in pdf_stream:
            raise InvalidTemplateError

    @staticmethod
    def iterate_elements(pdf_stream: bytes) -> List["pdfrw.PdfDict"]:
        """Iterates through a PDF and returns all elements found."""

        pdf = pdfrw.PdfReader(fdata=pdf_stream)

        result = []

        for i in range(len(pdf.pages)):
            elements = pdf.pages[i][TemplateConstants().annotation_key]
            if elements:
                for element in elements:
                    if (
                        element[TemplateConstants().subtype_key]
                        == TemplateConstants().widget_subtype_key
                        and element[TemplateConstants().annotation_field_key]
                    ):
                        result.append(element)

        return result

    @staticmethod
    def get_element_key(element: "pdfrw.PdfDict") -> str:
        """Returns its annotated key given a PDF form element."""

        return element[TemplateConstants().annotation_field_key][1:-1]

    def build_elements(self, pdf_stream: bytes) -> Dict[str, "Element"]:
        """Builds an element list given a PDF form stream."""

        element_type_mapping = {
            "/Btn": ElementType.checkbox,
            "/Tx": ElementType.text,
        }
        results = {}

        for element in self.iterate_elements(pdf_stream):
            key = self.get_element_key(element)

            results[key] = Element(
                element_name=key,
                element_type=element_type_mapping.get(
                    str(element[TemplateConstants().element_type_key])
                ),
            )

        return results