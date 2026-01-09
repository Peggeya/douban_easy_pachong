from douban_crawler import DoubanCrawler
from sentiment_analysis import SentimentAnalysis
from topic_analysis import TopicAnalysis
from report_generator import ReportGenerator

def main():
    print("=" * 80)
    print("豆瓣电影评论情感与主题分析系统")
    print("=" * 80)
    print()
    
    print("步骤1：开始爬取豆瓣电影数据...")
    print("-" * 80)
    crawler = DoubanCrawler()
    
    try:
        total_movies = crawler.crawl_movies()
        print(f"\n爬取完成！共爬取 {total_movies} 部电影")
    except Exception as e:
        print(f"爬取过程中出现错误: {e}")
    finally:
        crawler.close()
    
    print()
    print("步骤2：开始进行情感分析...")
    print("-" * 80)
    sentiment_analyzer = SentimentAnalysis()
    
    try:
        sentiment_results = sentiment_analyzer.analyze_all_movies()
        type_stats = sentiment_analyzer.get_type_sentiment_summary(sentiment_results)
        print(f"情感分析完成！共分析 {len(sentiment_results)} 部电影")
    except Exception as e:
        print(f"情感分析过程中出现错误: {e}")
        sentiment_results = []
        type_stats = {}
    
    print()
    print("步骤3：开始进行主题分析...")
    print("-" * 80)
    topic_analyzer = TopicAnalysis()
    
    try:
        topic_results = topic_analyzer.analyze_all_movies_topics()
        type_summary = topic_analyzer.get_type_topic_summary(topic_results)
        print(f"主题分析完成！共分析 {len(topic_results)} 部电影")
    except Exception as e:
        print(f"主题分析过程中出现错误: {e}")
        topic_results = []
        type_summary = {}
    
    print()
    print("步骤4：生成分析报告...")
    print("-" * 80)
    report_generator = ReportGenerator()
    
    try:
        combined_report = report_generator.generate_combined_report(
            sentiment_results, type_stats, topic_results, type_summary
        )
        
        report_filename = "豆瓣电影评论情感与主题分析报告.txt"
        report_generator.save_report(combined_report, report_filename)
        print("报告生成完成！")
    except Exception as e:
        print(f"报告生成过程中出现错误: {e}")
    
    print()
    print("=" * 80)
    print("所有任务完成！")
    print("=" * 80)

if __name__ == "__main__":
    main()