import redis
import json
from config import Config

class RedisStorage:
    def __init__(self):
        self.redis_client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            db=Config.REDIS_DB,
            decode_responses=True
        )
    
    def save_movie(self, movie_data):
        movie_id = movie_data.get('id', '')
        if not movie_id:
            return False
        
        key = f"{Config.REDIS_KEY_PREFIX}{movie_id}"
        self.redis_client.set(key, json.dumps(movie_data, ensure_ascii=False))
        return True
    
    def get_movie(self, movie_id):
        key = f"{Config.REDIS_KEY_PREFIX}{movie_id}"
        data = self.redis_client.get(key)
        if data:
            return json.loads(data)
        return None
    
    def get_all_movies(self):
        keys = self.redis_client.keys(f"{Config.REDIS_KEY_PREFIX}*")
        movies = []
        for key in keys:
            data = self.redis_client.get(key)
            if data:
                movies.append(json.loads(data))
        return movies
    
    def delete_movie(self, movie_id):
        key = f"{Config.REDIS_KEY_PREFIX}{movie_id}"
        self.redis_client.delete(key)
    
    def clear_all(self):
        keys = self.redis_client.keys(f"{Config.REDIS_KEY_PREFIX}*")
        if keys:
            self.redis_client.delete(*keys)