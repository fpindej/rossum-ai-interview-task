from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Datapoint:
    schema_id: Optional[str] = None
    text: Optional[str] = None

    @staticmethod
    def from_dict(data: dict) -> 'Datapoint':
        return Datapoint(
            schema_id=data.get('@schema_id'),
            text=data.get('#text')
        )


@dataclass
class Multivalue:
    schema_id: str
    tuple: List[Datapoint]

    @staticmethod
    def from_dict(data: dict) -> 'Multivalue':
        return Multivalue(
            schema_id=data.get('@schema_id'),
            tuple=[Datapoint.from_dict(dp) for dp in data.get('tuple', {}).get('datapoint', [])]
        )


@dataclass
class Section:
    schema_id: str
    datapoint: List[Datapoint]
    multivalue: Optional[Multivalue] = None

    @staticmethod
    def from_dict(data: dict) -> 'Section':
        datapoint_data = data.get('datapoint', [])
        if isinstance(datapoint_data, dict):
            datapoint_data = [datapoint_data]
        return Section(
            schema_id=data.get('@schema_id'),
            datapoint=[Datapoint.from_dict(dp) for dp in datapoint_data],
            multivalue=Multivalue.from_dict(data.get('multivalue')) if data.get('multivalue') else None
        )


@dataclass
class Annotation:
    content: List[Section]

    @staticmethod
    def from_dict(data: dict) -> 'Annotation':
        required_sections = {'basic_info_section', 'amounts_section', 'vendor_section', 'payment_info_section',
                             'other_section'}
        sections = [Section.from_dict(section) for section in data.get('content', {}).get('section', []) if
                    section.get('@schema_id') in required_sections]
        return Annotation(content=sections)
