import logging.handlers

# Silence SUDS
logging.getLogger('suds.client').setLevel(logging.ERROR)


def configure_logging(app, context='api'):
    app.logger.setLevel(logging.DEBUG)
    level = app.config['LOG_LEVEL']

    file_handler = logging.handlers.TimedRotatingFileHandler(
        app.config['LOG_FILE'], when='midnight', backupCount=1)

    file_handler.setLevel(level)
    app.logger.addHandler(file_handler)

    if app.config.get('USE_GRAYLOG'):
        try:
            import graypy

            facility = 'comptoir.{0}'.format(context)
            grayhandler = graypy.GELFHandler(app.config['GRAYLOG_HOST'],
                                             app.config['GRAYLOG_PORT'],
                                             facility=facility)
            grayhandler.setLevel(level)
            GPFORMAT = '%(name)s[%(process)d]: %(message)s'
            grayhandler.setFormatter(logging.Formatter(fmt=GPFORMAT))
            app.logger.addHandler(grayhandler)
        except Exception:
            app.logger.exception('Graylog not configured on this machine')
