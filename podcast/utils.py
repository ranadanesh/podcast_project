
def elk_log_format(request, response, exception=None):
    user_id = request.user.id if request.user.is_authenticate else None
    username = request.user.username if request.user.is_authenticate else None
    email = request.user.email if request.user.is_authenticate else None

    user_info = {
        'user_id': user_id,
        'username': username,
        'email': email,
    }

    remote_host = request.META.get("REMOTE_ADDR", '-')
    request_line = request.method
    status_code = response.status_code if not exception else 500
    response_size = response.get('Content-Length', ' ') if response else ' '
    referrer = request.META.get('HTTP_REFERRER', '-')
    elapsed_time = response.elapsed.total_seconds() if hasattr(response, 'elapsed') else None
    user_agent = request.headers.get("user-agent")
    event = f"{request.get_full_path()} HTTP/1.1"

    message = str(exception) if exception else "Request Is Successful..."

    return {
        'user_info': user_info,
        'remote_host': remote_host,
        'request_line': request_line,
        'status_code': status_code,
        'response_size': response_size,
        'referrer': referrer,
        'elapsed_time': elapsed_time,
        'user_agent': user_agent,
        'event': event,
        'message': message,
    }
