"""
Create statistics table
"""

from yoyo import step

steps = [
    step("CREATE TABLE IF NOT EXISTS statistics ("
         "id UUID PRIMARY KEY DEFAULT gen_random_uuid(), "
         "total_predictions INTEGER NOT NULL DEFAULT 0, "
         "daily_predictions INTEGER NOT NULL DEFAULT 0, "
         "successful_predictions INTEGER NOT NULL DEFAULT 0, "
         "failed_predictions INTEGER NOT NULL DEFAULT 0, "
         "hotdog_predictions INTEGER NOT NULL DEFAULT 0, "
         "not_hotdog_predictions INTEGER NOT NULL DEFAULT 0, "
         "user_id UUID REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE, "
         "created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), "
         "updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()"
         ")",
         "DROP TABLE IF EXISTS statistics")
]
