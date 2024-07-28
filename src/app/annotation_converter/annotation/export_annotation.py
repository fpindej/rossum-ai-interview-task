from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Detail:
    Amount: float
    Quantity: int
    Notes: str
    AccountId: Optional[str] = None


@dataclass
class Payable:
    InvoiceNumber: str
    InvoiceDate: str
    DueDate: str
    TotalAmount: float
    Iban: str
    Amount: float
    Currency: str
    Vendor: str
    VendorAddress: str
    Details: List[Detail] = field(default_factory=list)
    Notes: Optional[str] = None


@dataclass
class Invoices:
    Payable: Payable


@dataclass
class Document:
    file_name: str
    file_url: str


@dataclass
class Modifier:
    username: str


@dataclass
class Annotation:
    status: str
    arrived_at: str
    exported_at: str
    document: Document
    modifier: Modifier
    automated: bool
    modified_at: str
    assigned_at: str


@dataclass
class ExportAnnotation:
    Invoices: Invoices
    Annotations: List[Annotation]
