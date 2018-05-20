from flask import current_app, request, g
import uuid


# Return an id that lasts the life of the request,
# or create one if this is the first time the value is being returned
def request_ids():
    if getattr(g, 'request_id', None):
        return g.request_id, g.get('original_request_id')

    g.request_id = _generate_request_id()
    g.original_request_id = request.headers.get("Request-Id")

    return g.request_id, g.original_request_id


# Generate a new request ID
def _generate_request_id():
    return uuid.uuid4()


# return the request endpoint
def get_request_endpoint():
    return request.url_rule.endpoint


def redact_sensitive_data(data, sensitive_fields):
    return dict((k, v) if k not in sensitive_fields else (k, '[redacted]')
                for k, v in data.iteritems())

def get_form_data():
    data = {}
    for source in [request.form, request.authorization]:
        if source:
            data.update(dict((k, v) for k, v in source.iteritems()))
    return data
