from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
    OPENMETADATA_HOST: str | None = None
    OPENMETADATA_JWT_TOKEN: str | None = None
    OPENMETADATA_USERNAME: str | None = None
    OPENMETADATA_PASSWORD: str | None = None
    
    @classmethod
    def from_env(cls) -> "Config":
        if not os.getenv("OPENMETADATA_HOST"):
            raise ValueError("OPENMETADATA_HOST is not set")
        if not os.getenv("OPENMETADATA_JWT_TOKEN") and not (
            os.getenv("OPENMETADATA_USERNAME") and os.getenv("OPENMETADATA_PASSWORD")
        ):
            raise ValueError(
                "Either OPENMETADATA_JWT_TOKEN or OPENMETADATA_USERNAME and OPENMETADATA_PASSWORD must be set"
            )

        return cls(
            # OPENMETADATA_HOST=os.getenv("OPENMETADATA_HOST"),
            # OPENMETADATA_JWT_TOKEN=os.getenv("OPENMETADATA_JWT_TOKEN"),
            # OPENMETADATA_USERNAME=os.getenv("OPENMETADATA_USERNAME"),
            # OPENMETADATA_PASSWORD=os.getenv("OPENMETADATA_PASSWORD"),
            
            OPENMETADATA_HOST="http://10.31.4.246:8585",
            OPENMETADATA_JWT_TOKEN="eyJraWQiOiJHYjM4OWEtOWY3Ni1nZGpzLWE5MmotMDI0MmJrOTQzNTYiLCJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJvcGVuLW1ldGFkYXRhLm9yZyIsInN1YiI6Im1jcGFwcGxpY2F0aW9uYm90Iiwicm9sZXMiOltudWxsXSwiZW1haWwiOiJtY3BhcHBsaWNhdGlvbmJvdEBvcGVubWV0YWRhdGEub3JnIiwiaXNCb3QiOnRydWUsInRva2VuVHlwZSI6IkJPVCIsImlhdCI6MTc1MzE1MzU0OSwiZXhwIjpudWxsfQ.LgNuTUgHF_atwA8_q-iHXUMpVdmS9tHfXv9go8T6Z_BiFHv8DsBXWDmiOSSzLOoW3v_B_XjiILgxlXwkDLMq2y77xuQJQuM_GqgRzcwojRrSz9mSML-GC80x0n1Cq54wMufbr0xnhyCRZz8ehbo89ehx16MQ41h8FnefYNCQGvgEhhKcv8bGBauCuzpbvD-FOXZzHSxhGjBZBy4QyKPIwkWQMS8aCHzDh1Gc5AAztNuh6ssL5I5ZXC7vT5E2mHc2d2OySNm6e4weQNEKP-c8-BScRKgSL6JYU7ZfflrJs-DLEp-yren9d2lFfGF77MUzd1af-KoBitWZslWpNj4OZA",
            OPENMETADATA_USERNAME=None,
            OPENMETADATA_PASSWORD=None,
        )
