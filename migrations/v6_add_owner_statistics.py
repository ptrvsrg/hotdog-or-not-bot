"""
Add owner statistics
"""

import os

from yoyo import step

owner_username = os.getenv("OWNER_USERNAME")
if owner_username is None:
    raise ValueError("OWNER_USERNAME is not set")

steps = [
    step(
        "INSERT INTO statistics(user_id) "
        + "VALUES ((SELECT id FROM users WHERE username = '"
        + owner_username
        + "')) "
        + "ON CONFLICT DO NOTHING",
        "",
    )
]
