import base64
import binascii
import os
from typing import Optional, Tuple, Union

from ml_models.face_utils import recognize_face_from_db, FaceRecognitionError


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
    _get_image_bytes(waste_image)

    override_type = os.getenv("DEFAULT_WASTE_TYPE")
    if override_type:
        return override_type.strip().lower()

    raise VisionServiceError(
        "Waste classification backend is not configured. Set DEFAULT_WASTE_TYPE for now or integrate OpenAI classifier."
    )
