import environ

env = environ.Env()
environ.Env.read_env()

REDDIS_PORT=env('REDDIS_PORT')
API_KEY=env('API_KEY')