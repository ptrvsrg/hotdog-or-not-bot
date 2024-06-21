from app.service import statistics_service


def clear_daily_prediction_job():
    statistics_service.clear_daily_predictions()
