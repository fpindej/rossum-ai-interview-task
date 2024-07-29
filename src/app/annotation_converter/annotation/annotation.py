from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Detail:
    item_total_base: Optional[float] = None
    item_quantity: Optional[int] = None
    item_description: Optional[str] = None


@dataclass
class Annotation:
    details: List[Detail]
    document_id: Optional[str] = None
    date_issue: Optional[str] = None
    date_due: Optional[str] = None
    amount_total: Optional[float] = None
    amount_total_base: Optional[float] = None
    currency: Optional[str] = None
    recipient_name: Optional[str] = None
    recipient_address: Optional[str] = None
    iban: Optional[str] = None
    notes: Optional[str] = None
