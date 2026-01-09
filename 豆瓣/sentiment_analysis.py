import jieba
from snownlp import SnowNLP
from redis_storage import RedisStorage

class SentimentAnalysis:
    def __init__(self):
        self.storage = RedisStorage()
    
    def analyze_comment(self, comment):
        if not comment or len(comment.strip()) == 0:
            return None
        
        s = SnowNLP(comment)
        sentiment_score = s.sentiments
        
        if sentiment_score >= 0.6:
            sentiment = 'positive'
        elif sentiment_score <= 0.4:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'comment': comment,
            'sentiment_score': sentiment_score,
            'sentiment': sentiment
        }
    
    def analyze_movie_comments(self, movie_id):
        movie = self.storage.get_movie(movie_id)
        if not movie:
            return None
        
        comments = movie.get('comments', [])
        if not comments:
            return None
        
        results = []
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        total_score = 0
        
        for comment in comments:
            result = self.analyze_comment(comment)
            if result:
                results.append(result)
                total_score += result['sentiment_score']
                
                if result['sentiment'] == 'positive':
                    positive_count += 1
                elif result['sentiment'] == 'negative':
                    negative_count += 1
                else:
                    neutral_count += 1
        
        if len(results) == 0:
            return None
        
        avg_score = total_score / len(results)
        
        return {
            'movie_id': movie_id,
            'movie_name': movie.get('name', ''),
            'total_comments': len(comments),
            'analyzed_comments': len(results),
            'positive_count': positive_count,
            'negative_count': negative_count,
            'neutral_count': neutral_count,
            'positive_ratio': positive_count / len(results) if len(results) > 0 else 0,
            'negative_ratio': negative_count / len(results) if len(results) > 0 else 0,
            'neutral_ratio': neutral_count / len(results) if len(results) > 0 else 0,
            'avg_sentiment_score': avg_score,
            'detailed_results': results
        }
    
    def analyze_all_movies(self):
        movies = self.storage.get_all_movies()
        all_results = []
        
        for movie in movies:
            movie_id = movie.get('id', '')
            if movie_id:
                result = self.analyze_movie_comments(movie_id)
                if result:
                    all_results.append(result)
        
        return all_results
    
    def get_type_sentiment_summary(self, results):
        type_stats = {}
        
        for result in results:
            movie = self.storage.get_movie(result['movie_id'])
            if not movie:
                continue
            
            movie_type = movie.get('type', '未知')
            
            if movie_type not in type_stats:
                type_stats[movie_type] = {
                    'count': 0,
                    'total_positive': 0,
                    'total_negative': 0,
                    'total_neutral': 0,
                    'total_score': 0,
                    'avg_score': 0
                }
            
            type_stats[movie_type]['count'] += 1
            type_stats[movie_type]['total_positive'] += result['positive_count']
            type_stats[movie_type]['total_negative'] += result['negative_count']
            type_stats[movie_type]['total_neutral'] += result['neutral_count']
            type_stats[movie_type]['total_score'] += result['avg_sentiment_score']
        
        for movie_type in type_stats:
            stats = type_stats[movie_type]
            stats['avg_score'] = stats['total_score'] / stats['count'] if stats['count'] > 0 else 0
        
        return type_stats