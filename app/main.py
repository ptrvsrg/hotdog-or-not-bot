def run_app():
    # Configure logger
    import logging as sys_logging
    from app.logger import configure_logging

    configure_logging()

    # Load config
    from app.config import config

    sys_logging.getLogger().setLevel(
        sys_logging.DEBUG if config.server.debug else sys_logging.INFO
    )

    # Configure i18n
    from app.i18n import configure_locale as configure_locales

    configure_locales()

    # Start server
    try:
        import uvicorn
        from app.http_server import app

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=config.server.port,
            log_config=None,
        )
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run_app()
