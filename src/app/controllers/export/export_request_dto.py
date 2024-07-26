from dataclasses import dataclass


@dataclass(frozen=True)
class ExportRequestDto:
    annotation_id: str
    queue_id: str

    @classmethod
    def deserialize(cls, data):
        return cls(
            annotation_id=data.get('annotation_id'),
            queue_id=data.get('queue_id')
        )
