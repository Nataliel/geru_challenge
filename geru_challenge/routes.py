def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # Quote API
    config.add_route('get_quotes', '/quotes')
    config.add_route('get_quote_random', '/quotes/random')
    config.add_route('get_quote', '/quotes/{quote_number}')

    # Request
    config.add_route('get_requests', '/get_requests')
    config.add_route('get_requests_by_session', '/get_requests_by_session/{session_key}')

    # Session
    config.add_route('get_sessions', '/get_sessions')
    config.add_route('get_session', '/get_session/{session_key}')

