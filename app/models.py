from pydantic import BaseModel

class FrameMessage(BaseModel):
    image_b64: str  # base64-encoded JPEG
