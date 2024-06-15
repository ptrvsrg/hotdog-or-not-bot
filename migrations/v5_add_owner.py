"""
Add owner
"""
import os

from yoyo import step

owner_username = os.getenv("OWNER_USERNAME")
if owner_username is None:
    raise ValueError("OWNER_USERNAME is not set")

steps = [
    step("INSERT INTO users(username, is_admin, subscription_id) " +
         "VALUES ('" + owner_username + "', true, " +
         "(SELECT id FROM subscriptions WHERE name = 'Unlimited')) " +
         "ON CONFLICT DO NOTHING", "")
]
