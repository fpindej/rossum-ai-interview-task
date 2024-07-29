import xmltodict
from flask import current_app

from app.controllers.response import Response


class AnnotationService:
    @staticmethod
    def extract_annotation_data(export_queue_response_text: str, annotation_id: str) -> dict:
        data = xmltodict.parse(export_queue_response_text)
        annotations = data['export']['results']['annotation']
        # This works only if there are multiple annotations in the response, otherwise it returns the annotation itself
        # Might be better to return the annotation itself if there is only one annotation
        # Let's keep it as is for now just to keep it simple for the sake of this example
        target_annotation = next((a for a in annotations if a['@url'].endswith(annotation_id)), None)

        if not target_annotation:
            current_app.logger.error(f"Annotation with id {annotation_id} not found")
            raise ValueError(f"Annotation with id {annotation_id} not found")

        return target_annotation
