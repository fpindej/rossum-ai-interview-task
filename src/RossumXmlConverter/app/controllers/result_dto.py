﻿from dataclasses import dataclass, asdict
from typing import Optional, Any


@dataclass
class ResultDto:
    success: bool
    data: Optional[Any] = None

    def serialize(self):
        return asdict(self)
