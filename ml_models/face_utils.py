from io import BytesIO
import math
from typing import Optional, Tuple

from PIL import Image
from django.conf import settings

from accounts.models import UserFaceEmbedding


_MTCNN = None
_RESNET = None
_NP = None
_TORCH = None


class FaceRecognitionError(Exception):
    pass


def _load_models():
    global _MTCNN, _RESNET, _NP, _TORCH

    if _MTCNN is not None and _RESNET is not None and _NP is not None and _TORCH is not None:
        return _MTCNN, _RESNET, _NP, _TORCH

    try:
        import numpy as np
        import torch
        from facenet_pytorch import MTCNN, InceptionResnetV1
    except Exception as exc:
        raise FaceRecognitionError(
            "Face recognition dependencies are missing. Install requirements and redeploy."
        ) from exc

    _NP = np
    _TORCH = torch
    _MTCNN = MTCNN(image_size=160, margin=20, min_face_size=40)
    _RESNET = InceptionResnetV1(pretrained="vggface2").eval()
    return _MTCNN, _RESNET, _NP, _TORCH


def extract_embedding_from_bytes(image_bytes: bytes):
    if not image_bytes:
        raise FaceRecognitionError("Image payload is required")

    mtcnn, resnet, _, torch = _load_models()

    try:
        image = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise FaceRecognitionError("Invalid image payload") from exc

    face = mtcnn(image)
    if face is None:
        return None

    face = face.unsqueeze(0)
    with torch.no_grad():
        embedding = resnet(face)

    return embedding.detach().cpu().numpy()[0]


def _to_vector(stored_embedding):
    _, _, np, _ = _load_models()
    if stored_embedding is None:
        return None
    return np.asarray(stored_embedding, dtype=np.float32)


def _euclidean_distance(vec_a, vec_b) -> float:
    _, _, np, _ = _load_models()
    if vec_a is None or vec_b is None:
        return float("inf")
    if vec_a.shape != vec_b.shape:
        return float("inf")
    return float(np.linalg.norm(vec_a - vec_b))


def recognize_face_from_db(image_bytes: bytes, threshold: Optional[float] = None) -> Optional[Tuple[object, float]]:
    _, _, np, _ = _load_models()

    user_embedding = extract_embedding_from_bytes(image_bytes)
    if user_embedding is None:
        return None

    if threshold is None:
        threshold = float(getattr(settings, "FACE_DISTANCE_THRESHOLD", 0.9))

    best_user = None
    best_distance = float("inf")

    for face_record in UserFaceEmbedding.objects.select_related("user").all():
        db_embedding = _to_vector(face_record.embedding)
        distance = _euclidean_distance(user_embedding, db_embedding)
        if distance < best_distance:
            best_distance = distance
            best_user = face_record.user

    if best_user is None:
        return None

    if not math.isfinite(best_distance) or best_distance >= threshold:
        return None

    confidence = max(0.0, min(1.0, 1.0 - best_distance))
    return best_user, round(confidence, 4)


def update_user_embedding(user, image_bytes: bytes, model_name: str = "facenet-vggface2"):
    embedding = extract_embedding_from_bytes(image_bytes)
    if embedding is None:
        raise FaceRecognitionError("No face detected in image")

    _, _, np, _ = _load_models()
    embedding_list = np.asarray(embedding, dtype=np.float32).tolist()
    face_record, _ = UserFaceEmbedding.objects.update_or_create(
        user=user,
        defaults={
            "embedding": embedding_list,
            "model_name": model_name,
        },
    )
    return face_record


def register_face(user, image_bytes: bytes, model_name: str = "facenet-vggface2"):
    return update_user_embedding(user=user, image_bytes=image_bytes, model_name=model_name)
