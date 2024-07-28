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
class InvoiceRegisters:
    Invoices: Invoices
