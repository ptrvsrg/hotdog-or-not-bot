def configure_logging() -> None:
    import logging
    import sys

    logging.basicConfig(
        format="%(asctime)s.%(msecs)03d %(levelname)-8s %(process)d --- [%(threadName)s] %(filename)s:%(lineno)d: %("
               "message)s",
        datefmt='%Y-%m-%d %H:%M:%S',
        stream=sys.stdout,
    )
