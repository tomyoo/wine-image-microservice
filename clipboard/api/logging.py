from __future__ import absolute_import

import logging

from datetime import datetime
from flask import current_app, request, g, has_request_context
import json

from .utilities import request_ids, redact_sensitive_data, get_form_data

sensitive_fields = ['client_secret', 'token', 'access_token', 'password']


def setup_logging(app):
    class ApiFilter(logging.Filter):
        def filter(self, record):
            record.environment = app.config.get('ENVIRONMENT')
            if has_request_context():
                request_id, original_request_id = request_ids()
                record.request_id = request_id
                record.original_request_id = original_request_id
                record.request_url = request.url
                record.request_method = request.method
                record.remote_addr = request.remote_addr
                record.endpoint = request.endpoint
                if (getattr(request, 'oauth', None) and
                        getattr(request.oauth, 'user', None)):
                    record.user = request.oauth.user.username
                else:
                    record.user = 'N/A'
            return True

    app.logger.addFilter(ApiFilter())

    @app.before_request
    def log_request_info():
        g.start = datetime.now()

        request_id, original_request_id = request_ids()
        log_data = {'request-id': str(request_id),
                    'original-request-id': original_request_id,
                    'user-agent': request.headers.get('User-Agent'),
                    'url': request.url}

        json_data = request.json or {}
        form_data = get_form_data()

        if current_app.config['REDACT']:
            json_data = redact_sensitive_data(json_data, sensitive_fields)
            form_data = redact_sensitive_data(form_data, sensitive_fields)

        log_data['json_data'] = json_data
        log_data['form_data'] = form_data

        current_app.logger.info('Request Data: {0}'.format(log_data))

    @app.after_request
    def log_response_info(response):
        time = datetime.now() - g.start
        request_id, original_request_id = request_ids()
        log_data = {'url': request.url,
                    'response_code': response.status_code,
                    'time': time.seconds + time.microseconds / 10. ** 6,
                    'request-id': str(request_id),
                    'original-request-id': original_request_id,
                    'data': json.loads(response.data)}

        data = json.loads(response.data or {})

        if not isinstance(data, list) and current_app.config['REDACT']:
            data = redact_sensitive_data(data, sensitive_fields)

        log_data['data'] = data

        current_app.logger.info('Response Data: {0}'.format(log_data))
        return response
