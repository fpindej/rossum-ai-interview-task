from dataclasses import dataclass, asdict
from typing import List, Optional


@dataclass
class Detail:
    Amount: Optional[float] = None
    AccountId: Optional[str] = None
    Quantity: Optional[int] = None
    Notes: Optional[str] = None

    def to_dict(self):
        return asdict(self)


@dataclass
class Payable:
    InvoiceNumber: Optional[str] = None
    InvoiceDate: Optional[str] = None
    DueDate: Optional[str] = None
    TotalAmount: Optional[float] = None
    Notes: Optional[str] = None
    Iban: Optional[str] = None
    Amount: Optional[float] = None
    Currency: Optional[str] = None
    Vendor: Optional[str] = None
    VendorAddress: Optional[str] = None
    Details: Optional[List[Detail]] = None

    def to_dict(self):
        data = asdict(self)
        if self.Details:
            data['Details'] = [detail.to_dict() for detail in self.Details]
        return data


@dataclass
class Invoices:
    Payable: Optional[Payable] = None

    def to_dict(self):
        data = asdict(self)
        if self.Payable:
            data['Payable'] = self.Payable.to_dict()
        return data


@dataclass
class InvoiceRegisters:
    Invoices: Optional[Invoices] = None

    def to_dict(self):
        data = asdict(self)
        if self.Invoices:
            data['Invoices'] = self.Invoices.to_dict()
        return {'InvoiceRegisters': data}
