from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Datapoint:
    rir_confidence: float
    schema_id: str
    type: str
    text: Optional[str] = None


@dataclass
class Multivalue:
    schema_id: str
    tuple: List[Datapoint]


@dataclass
class Section:
    schema_id: str
    datapoint: List[Datapoint]
    multivalue: Optional[Multivalue] = None


@dataclass
class Document:
    url: str
    file_name: str
    file: str


@dataclass
class Annotation:
    url: str
    status: str
    arrived_at: str
    document: Document
    modifier: Optional[str]
    schema: str
    metadata: Optional[str]
    content: List[Section]
    automated: bool
