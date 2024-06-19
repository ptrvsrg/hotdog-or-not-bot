"""
Create user table
"""

from yoyo import step

steps = [
    step(
        "CREATE TABLE IF NOT EXISTS subscriptions ("
        "id UUID PRIMARY KEY DEFAULT gen_random_uuid(), "
        "name VARCHAR(255) NOT NULL UNIQUE, "
        "total_daily_predictions INTEGER NOT NULL DEFAULT -1, "
        "created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), "
        "updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()"
        ")",
        "DROP TABLE IF EXISTS subscriptions",
    )
]
