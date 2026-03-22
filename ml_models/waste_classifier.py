import base64
from io import BytesIO
import os

from PIL import Image


ALLOWED_WASTE_TYPES = {"plastic", "metal", "organic", "ewaste"}
WASTE_TYPE_MAP = {
    "plastic": "plastic",
    "metal": "metal",
    "organic": "bio",
    "ewaste": "ewaste",
}


class WasteClassificationError(Exception):
    pass


def _preprocess_image_bytes(image_bytes: bytes) -> bytes:
    try:
        img = Image.open(BytesIO(image_bytes)).convert("RGB")
    except Exception as exc:
        raise WasteClassificationError("Invalid waste image payload") from exc

    width, height = img.size
    left = width * 0.2
    top = height * 0.2
    right = width * 0.8
    bottom = height * 0.8

    img = img.crop((left, top, right, bottom))
    img = img.resize((512, 512))

    out = BytesIO()
    img.save(out, format="JPEG")
    return out.getvalue()


def classify_waste_from_bytes(image_bytes: bytes) -> str:
    if not image_bytes:
        raise WasteClassificationError("Waste image payload is required")

    try:
        from openai import OpenAI
    except Exception as exc:
        raise WasteClassificationError("openai dependency is missing. Install requirements.txt") from exc

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise WasteClassificationError("OPENAI_API_KEY is not configured")

    processed_bytes = _preprocess_image_bytes(image_bytes)
    base64_image = base64.b64encode(processed_bytes).decode("utf-8")

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model=os.getenv("WASTE_CLASSIFIER_MODEL", "gpt-4o-mini"),
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a strict waste classification AI.\n"
                    "Classify the object into EXACTLY ONE of these labels:\n"
                    "plastic\nmetal\norganic\newaste\n\n"
                    "Respond with ONLY one word from the list above."
                ),
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Classify this waste item."},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        },
                    },
                ],
            },
        ],
        max_tokens=5,
    )

    result = (response.choices[0].message.content or "").strip().lower()
    if result not in ALLOWED_WASTE_TYPES:
        raise WasteClassificationError(
            f"Classifier returned invalid label: '{result}'. Expected one of {sorted(ALLOWED_WASTE_TYPES)}"
        )

    return WASTE_TYPE_MAP[result]
