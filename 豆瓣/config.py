import time

class Config:
    BASE_URL = "https://movie.douban.com/top250"
    
    COOKIE = 'll="108257"; bid=WsXXm96_VIM; _pk_id.100001.4cf6=a765ff9dd361f295.1766117100.; _vwo_uuid_v2=D3F921254FE1DF3D223D8A69B8E6426F6|bb2e47638938e1f9c7098e33082b4c3f; __yadk_uid=VGuLDoNLgFjfrJvJMgOtkaQKUonnIT60; __utmz=30149280.1767705180.2.2.utmcsr=gdufemooc.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmz=223695111.1767705180.2.2.utmcsr=gdufemooc.cn|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1767768135%2C%22https%3A%2F%2Fwww.gdufemooc.cn%2F%22%5D; _pk_ses.100001.4cf6=1; __utma=30149280.207456266.1766117101.1767705180.1767768135.3; __utmb=30149280.0.10.1767768135; __utmc=30149280; __utma=223695111.527966569.1766117101.1767705180.1767768135.3; __utmb=223695111.0.10.1767768135; __utmc=223695111; ap_v=0,6.0'
    
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36'
    
    REFERER = 'https://www.gdufemooc.cn/'
    
    REQUEST_DELAY = 10
    
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    
    REDIS_KEY_PREFIX = 'douban:movie:'