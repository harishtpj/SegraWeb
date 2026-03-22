import base64
import binascii
import hashlib
import math
import os
from typing import List, Optional, Tuple, Union

from accounts.models import UserFaceEmbedding


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


def build_embedding(image_data: Union[str, bytes, bytearray]) -> List[float]:
    image_bytes = _get_image_bytes(image_data)
    digest = hashlib.sha256(image_bytes).digest()
    return [round(value / 255.0, 6) for value in digest]


def _cosine_similarity(vec_a: List[float], vec_b: List[float]) -> float:
    if len(vec_a) != len(vec_b):
        return -1.0

    dot_product = sum(a * b for a, b in zip(vec_a, vec_b))
    norm_a = math.sqrt(sum(a * a for a in vec_a))
    norm_b = math.sqrt(sum(b * b for b in vec_b))

    if norm_a == 0 or norm_b == 0:
        return -1.0

    return dot_product / (norm_a * norm_b)


def identify_user_from_face(face_image: Union[str, bytes, bytearray], threshold: float = 0.90) -> Optional[Tuple[object, float]]:
    incoming_embedding = build_embedding(face_image)

    best_user = None
    best_score = -1.0

    for face_record in UserFaceEmbedding.objects.select_related("user").all():
        score = _cosine_similarity(incoming_embedding, face_record.embedding)
        if score > best_score:
            best_score = score
            best_user = face_record.user

    if best_user is None or best_score < threshold:
        return None

    return best_user, round(best_score, 4)


def classify_waste_image(waste_image: Union[str, bytes, bytearray]) -> str:
    _get_image_bytes(waste_image)

    override_type = os.getenv("DEFAULT_WASTE_TYPE")
    if override_type:
        return override_type.strip().lower()

    raise VisionServiceError(
        "Waste classification backend is not configured. Set DEFAULT_WASTE_TYPE for now or integrate OpenAI classifier."
    )
