def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('get_quotes', '/quotes')
    config.add_route('get_quote_random', '/quotes/random')
    config.add_route('get_quote', '/quotes/{quote_number}')
