from environs import Env

env = Env()
env.read_env()

api_key = env.str("API_KEY")
