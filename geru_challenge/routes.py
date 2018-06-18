def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    # My Quote
    config.add_route('get_my_quotes', '/get_my_quotes')
    config.add_route('get_my_quote_random', '/get_my_quotes/random')
    config.add_route('get_my_quote', '/get_my_quotes/{quote_number}')

    # Request
    config.add_route('get_requests', '/get_requests')
    config.add_route('get_requests_by_session', '/get_requests_by_session/{session_key}')

    # Session
    config.add_route('get_sessions', '/get_sessions')
    config.add_route('get_session', '/get_session/{session_key}')

