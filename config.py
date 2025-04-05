import tomllib

with open('config.toml', 'rb') as f:
    config = tomllib.load(f)

# API
# TODO: Modify the endpoint so that other venues and activities can be selected
BETTER_ENDPOINT = config['api']['better_endpoint']
HEADERS = {
    'Accept': config['headers']['accept'],
    'Origin': config['headers']['origin'],
    'Referer': config['headers']['referer'],
    'User-Agent': config['headers']['user_agent'],
}
