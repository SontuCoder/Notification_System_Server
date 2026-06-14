import firebase_admin    # type: ignore[import]
from firebase_admin import credentials  # type: ignore[import]

cred = credentials.Certificate(
    "app/credentials/firebase-service-account.json"
)

firebase_admin.initialize_app(cred)