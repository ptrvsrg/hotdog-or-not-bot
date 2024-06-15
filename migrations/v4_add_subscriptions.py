"""
Add subscriptions
"""

from yoyo import step

steps = [
    step("INSERT INTO subscriptions(name, total_daily_predictions) "
         "VALUES ('Free', 5), ('Unlimited', -1)", "")
]
