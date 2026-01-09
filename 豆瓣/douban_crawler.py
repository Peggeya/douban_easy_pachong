import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
from config import Config
from redis_storage import RedisStorage

class DoubanCrawler:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.storage = RedisStorage()
        self.setup_driver()
    
    def setup_driver(self):
        self.driver.delete_all_cookies()
        
        self.driver.get('https://movie.douban.com/top250')
        time.sleep(2)
        
        cookie_dict = {}
        for item in Config.COOKIE.split('; '):
            if '=' in item:
                key, value = item.split('=', 1)
                cookie_dict[key] = value
        
        for key, value in cookie_dict.items():
            self.driver.add_cookie({'name': key, 'value': value})
        
        self.driver.execute_script(f"Object.defineProperty(navigator, 'userAgent', {{get: function() {{ return '{Config.USER_AGENT}'; }}}});")
        self.driver.execute_script(f"Object.defineProperty(navigator, 'referer', {{get: function() {{ return '{Config.REFERER}'; }}}});")
    
    def get_page_source(self):
        return self.driver.page_source
    
    def parse_html(self, html):
        return etree.HTML(html)
    
    def get_movie_links_from_list(self):
        html = self.get_page_source()
        tree = self.parse_html(html)
        
        movie_links = tree.xpath('//div[@class="item"]/div[@class="pic"]/a/@href')
        return movie_links
    
    def get_movie_detail(self, movie_url):
        self.driver.get(movie_url)
        time.sleep(Config.REQUEST_DELAY)
        
        html = self.get_page_source()
        tree = self.parse_html(html)
        
        movie_data = {}
        
        movie_id = movie_url.split('/')[-2]
        movie_data['id'] = movie_id
        movie_data['url'] = movie_url
        
        movie_data['name'] = self.get_text(tree, '//h1/span[@property="v:itemreviewed"]/text()')
        movie_data['director'] = self.get_text(tree, '//div[@id="info"]//span[1]/span[@class="attrs"]/a/text()')
        movie_data['writer'] = self.get_text(tree, '//div[@id="info"]//span[2]/span[@class="attrs"]/a/text()')
        movie_data['actors'] = self.get_text(tree, '//div[@id="info"]//span[3]/span[@class="attrs"]/a/text()')
        movie_data['type'] = self.get_text(tree, '//span[@property="v:genre"]/text()')
        movie_data['country'] = self.get_text(tree, '//div[@id="info"]/text()[contains(., "制片国家")]')
        movie_data['language'] = self.get_text(tree, '//div[@id="info"]/text()[contains(., "语言")]')
        movie_data['release_date'] = self.get_text(tree, '//span[@property="v:initialReleaseDate"]/text()')
        movie_data['duration'] = self.get_text(tree, '//span[@property="v:runtime"]/text()')
        movie_data['aka'] = self.get_text(tree, '//div[@id="info"]/text()[contains(., "又名")]')
        movie_data['imdb'] = self.get_text(tree, '//div[@id="info"]/text()[contains(., "IMDb")]')
        movie_data['rating'] = self.get_text(tree, '//strong[@property="v:average"]/text()')
        movie_data['summary'] = self.get_text(tree, '//div[@id="link-report"]/span[@property="v:summary"]/text()')
        
        comments = self.get_comments(movie_url)
        movie_data['comments'] = comments
        
        if not movie_data['name']:
            print(f"未爬取到数据: {movie_url}")
            return None
        
        return movie_data
    
    def get_text(self, tree, xpath_expr):
        elements = tree.xpath(xpath_expr)
        if isinstance(elements, list):
            if len(elements) == 1:
                return str(elements[0]).strip()
            elif len(elements) > 1:
                return ' / '.join([str(e).strip() for e in elements])
        return ''
    
    def get_comments(self, movie_url):
        comments_url = f"{movie_url}comments?status=P"
        self.driver.get(comments_url)
        time.sleep(3)
        
        html = self.get_page_source()
        tree = self.parse_html(html)
        
        total_comments_element = tree.xpath('//*[@id="comments-section"]/div[1]/h2/span/a/text()')
        total_comments = 0
        if total_comments_element:
            total_text = total_comments_element[0]
            try:
                total_comments = int(''.join(filter(str.isdigit, total_text)))
            except:
                total_comments = 0
        
        print(f"  短评总数: {total_comments}")
        
        comments = []
        page = 0
        max_pages = (total_comments // 20) + 1 if total_comments > 0 else 5
        
        while True:
            html = self.get_page_source()
            tree = self.parse_html(html)
            
            comment_items = tree.xpath('//div[@class="comment-item"]')
            
            if not comment_items:
                break
            
            for item in comment_items:
                comment = self.get_text(item, './/span[@class="short"]/text()')
                if comment:
                    comments.append(comment)
            
            print(f"  已爬取 {len(comments)} 条短评")
            
            try:
                next_button = self.driver.find_element(By.XPATH, '//*[@id="paginator"]/a[3]')
                next_button.click()
                time.sleep(3)
                page += 1
                if page >= max_pages:
                    break
            except Exception as e:
                break
        
        return comments
    
    def crawl_movies(self):
        self.driver.get(Config.BASE_URL)
        time.sleep(2)
        
        total_movies = 0
        
        while True:
            movie_links = self.get_movie_links_from_list()
            
            if not movie_links:
                print("未找到电影链接，爬取结束")
                break
            
            print(f"当前页找到 {len(movie_links)} 部电影")
            
            for i, link in enumerate(movie_links):
                print(f"正在爬取第 {i+1}/{len(movie_links)} 部电影: {link}")
                
                movie_data = self.get_movie_detail(link)
                
                if movie_data:
                    self.storage.save_movie(movie_data)
                    total_movies += 1
                    print(f"成功保存电影: {movie_data['name']}")
                else:
                    print(f"爬取失败: {link}")
                
                self.driver.get('https://movie.douban.com/top250')
                time.sleep(Config.REQUEST_DELAY)
            
            next_button = self.driver.find_elements(By.XPATH, '//*[@id="content"]/div/div[1]/div[2]/span[3]/a')
            if not next_button:
                print("没有后页，爬取结束")
                break
            
            try:
                next_button[0].click()
                time.sleep(Config.REQUEST_DELAY)
            except Exception as e:
                print(f"点击后页失败: {e}")
                break
        
        print(f"爬取完成，共爬取 {total_movies} 部电影")
        return total_movies
    
    def close(self):
        self.driver.quit()