import base64
import binascii
from typing import Optional, Tuple, Union

from ml_models.face_utils import recognize_face_from_db, FaceRecognitionError
from ml_models.waste_classifier import classify_waste_from_bytes, WasteClassificationError


class VisionServiceError(Exception):
    pass


def _get_image_bytes(image_data: Union[str, bytes, bytearray]) -> bytes:
    if isinstance(image_data, (bytes, bytearray)):
        image_bytes = bytes(image_data)
        if not image_bytes:
            raise VisionServiceError("Image payload is required")
        return image_bytes

    if not image_data:
        raise VisionServiceError("Image payload is required")

    payload = image_data.strip()
    if "," in payload and payload.lower().startswith("data:"):
        payload = payload.split(",", 1)[1]

    try:
        return base64.b64decode(payload, validate=True)
    except (binascii.Error, ValueError):
        raise VisionServiceError("Invalid base64 image payload")


def identify_user_from_face(face_image: Union[str, bytes, bytearray], threshold: float = 0.90) -> Optional[Tuple[object, float]]:
    image_bytes = _get_image_bytes(face_image)
    try:
        return recognize_face_from_db(image_bytes, threshold=threshold)
    except FaceRecognitionError as exc:
        raise VisionServiceError(str(exc)) from exc


def classify_waste_image(waste_image: Union[str, bytes, bytearray]) -> str:
    image_bytes = _get_image_bytes(waste_image)
    try:
        return classify_waste_from_bytes(image_bytes)
    except WasteClassificationError as exc:
        raise VisionServiceError(str(exc)) from exc
