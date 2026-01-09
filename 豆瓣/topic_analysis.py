import jieba
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from redis_storage import RedisStorage
import jieba.analyse

class TopicAnalysis:
    def __init__(self):
        self.storage = RedisStorage()
    
    def preprocess_text(self, text):
        if not text:
            return ""
        
        words = jieba.cut(text)
        words = [word.strip() for word in words if len(word.strip()) > 1]
        return " ".join(words)
    
    def extract_keywords(self, text, topK=10):
        if not text:
            return []
        
        keywords = jieba.analyse.extract_tags(text, topK=topK, withWeight=True)
        return [keyword[0] for keyword in keywords]
    
    def build_corpus(self, comments):
        texts = []
        for comment in comments:
            processed = self.preprocess_text(comment)
            if processed:
                texts.append(processed)
        
        if not texts:
            return None, None, None
        
        vectorizer = CountVectorizer(max_features=100)
        corpus = vectorizer.fit_transform(texts)
        feature_names = vectorizer.get_feature_names_out()
        
        return vectorizer, corpus, texts
    
    def train_lda_model(self, corpus, num_topics=5):
        if corpus is None:
            return None
        
        lda_model = LatentDirichletAllocation(
            n_components=num_topics,
            max_iter=10,
            random_state=42
        )
        lda_model.fit(corpus)
        
        return lda_model
    
    def get_topics(self, lda_model, feature_names, num_words=5):
        topics = []
        for topic_idx, topic in enumerate(lda_model.components_):
            top_words_idx = topic.argsort()[:-num_words - 1:-1]
            top_words = [feature_names[i] for i in top_words_idx]
            word_probs = [topic[i] for i in top_words_idx]
            topic_str = " + ".join([f"{prob:.3f}*{word}" for word, prob in zip(top_words, word_probs)])
            topics.append((topic_idx, topic_str))
        
        return topics
    
    def analyze_movie_topics(self, movie_id, num_topics=3):
        movie = self.storage.get_movie(movie_id)
        if not movie:
            return None
        
        comments = movie.get('comments', [])
        if not comments:
            return None
        
        vectorizer, corpus, texts = self.build_corpus(comments)
        if corpus is None:
            return None
        
        lda_model = self.train_lda_model(corpus, num_topics=num_topics)
        if lda_model is None:
            return None
        
        feature_names = vectorizer.get_feature_names_out()
        topics = self.get_topics(lda_model, feature_names, num_words=5)
        
        all_keywords = []
        for comment in comments:
            keywords = self.extract_keywords(comment, topK=5)
            all_keywords.extend(keywords)
        
        keyword_freq = {}
        for keyword in all_keywords:
            keyword_freq[keyword] = keyword_freq.get(keyword, 0) + 1
        
        top_keywords = sorted(keyword_freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            'movie_id': movie_id,
            'movie_name': movie.get('name', ''),
            'total_comments': len(comments),
            'topics': topics,
            'top_keywords': top_keywords
        }
    
    def analyze_all_movies_topics(self):
        movies = self.storage.get_all_movies()
        all_results = []
        
        for movie in movies:
            movie_id = movie.get('id', '')
            if movie_id:
                result = self.analyze_movie_topics(movie_id)
                if result:
                    all_results.append(result)
        
        return all_results
    
    def get_type_topic_summary(self, results):
        type_keywords = {}
        
        for result in results:
            movie = self.storage.get_movie(result['movie_id'])
            if not movie:
                continue
            
            movie_type = movie.get('type', '未知')
            
            if movie_type not in type_keywords:
                type_keywords[movie_type] = {}
            
            for keyword, freq in result['top_keywords']:
                if keyword not in type_keywords[movie_type]:
                    type_keywords[movie_type][keyword] = 0
                type_keywords[movie_type][keyword] += freq
        
        type_summary = {}
        for movie_type in type_keywords:
            sorted_keywords = sorted(type_keywords[movie_type].items(), key=lambda x: x[1], reverse=True)[:10]
            type_summary[movie_type] = sorted_keywords
        
        return type_summary