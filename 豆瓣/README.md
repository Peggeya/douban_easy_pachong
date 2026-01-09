# 豆瓣电影评论情感与主题分析系统

## 项目简介
这是一个基于Python的豆瓣电影评论爬虫系统，可以爬取豆瓣Top250电影的详细信息、短评，并进行情感分析和主题分析。

## 功能特性
- ✅ 使用Selenium自动化爬取豆瓣Top250电影数据
- ✅ 使用xpath和lxml解析HTML
- ✅ 爬取电影详细信息（名称、导演、演员、类型等）
- ✅ 爬取电影短评（支持翻页）
- ✅ 使用Redis数据库存储数据
- ✅ 使用jieba进行中文分词
- ✅ 使用SnowNLP进行情感分析
- ✅ 使用sklearn的LDA进行主题分析
- ✅ 生成详细的分析报告

## 环境要求
- Python 3.8+
- Chrome浏览器
- Redis数据库（Docker）

## 安装依赖
```bash
pip install -r requirements.txt
```

## 配置说明
修改 `config.py` 文件中的配置：
- COOKIE: 豆瓣cookie
- USER_AGENT: 浏览器User-Agent
- REFERER: Referer
- REQUEST_DELAY: 爬取延迟（秒）
- REDIS_HOST: Redis主机地址
- REDIS_PORT: Redis端口
- REDIS_DB: Redis数据库编号

## 使用方法

### 1. 启动Redis数据库
```bash
docker run -d --name redis-douban -p 6379:6379 redis:latest
```

### 2. 运行爬虫程序
```bash
python main.py
```

## 项目结构
```
豆瓣/
├── config.py              # 配置文件
├── douban_crawler.py      # 主爬虫程序
├── redis_storage.py       # Redis存储模块
├── sentiment_analysis.py   # 情感分析模块
├── topic_analysis.py      # 主题分析模块
├── report_generator.py    # 报告生成模块
├── main.py              # 主程序入口
├── requirements.txt       # 依赖包列表
└── README.md            # 项目说明
```

## 爬取流程
1. 访问豆瓣Top250首页
2. 获取电影列表
3. 逐个爬取电影详情
4. 爬取电影短评
5. 翻页继续爬取
6. 保存到Redis数据库
7. 进行情感分析
8. 进行主题分析
9. 生成分析报告

## 注意事项
- 爬取速度较慢，每条数据延迟10秒（避免反爬）
- 短评每页延迟3秒
- 需要配置正确的cookie才能正常爬取
- Redis数据库必须正常运行

## 输出结果
- 豆瓣电影评论情感与主题分析报告.txt

## 技术栈
- Selenium: 浏览器自动化
- lxml + xpath: HTML解析
- Redis: 数据存储
- jieba: 中文分词
- SnowNLP: 情感分析
- scikit-learn: 主题模型（LDA）

## 许可证
MIT License