"""
Create subscription table
"""

from yoyo import step

steps = [
    step("CREATE TABLE IF NOT EXISTS users ("
         "id UUID PRIMARY KEY DEFAULT gen_random_uuid(), "
         "username VARCHAR(255) NOT NULL UNIQUE, "
         "is_enabled BOOLEAN NOT NULL DEFAULT true, "
         "is_admin BOOLEAN NOT NULL DEFAULT false, "
         "subscription_id UUID REFERENCES subscriptions (id) ON DELETE SET NULL ON UPDATE CASCADE, "
         "created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(), "
         "updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()"
         ")",
         "DROP TABLE IF EXISTS users")
]
