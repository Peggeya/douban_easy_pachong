import json
from datetime import datetime

class ReportGenerator:
    def __init__(self):
        pass
    
    def generate_sentiment_report(self, sentiment_results, type_stats):
        report = []
        report.append("=" * 80)
        report.append("豆瓣电影评论情感分析报告")
        report.append("=" * 80)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("一、总体统计")
        report.append("-" * 80)
        total_movies = len(sentiment_results)
        total_comments = sum(r['total_comments'] for r in sentiment_results)
        total_analyzed = sum(r['analyzed_comments'] for r in sentiment_results)
        
        report.append(f"电影总数: {total_movies}")
        report.append(f"评论总数: {total_comments}")
        report.append(f"已分析评论数: {total_analyzed}")
        report.append("")
        
        report.append("二、按电影类型统计")
        report.append("-" * 80)
        for movie_type, stats in type_stats.items():
            report.append(f"\n类型: {movie_type}")
            report.append(f"  电影数量: {stats['count']}")
            report.append(f"  正面评论数: {stats['total_positive']}")
            report.append(f"  负面评论数: {stats['total_negative']}")
            report.append(f"  中性评论数: {stats['total_neutral']}")
            report.append(f"  平均情感得分: {stats['avg_score']:.3f}")
        
        report.append("")
        report.append("三、各电影详细情感分析")
        report.append("-" * 80)
        for result in sentiment_results:
            report.append(f"\n电影: {result['movie_name']} (ID: {result['movie_id']})")
            report.append(f"  评论总数: {result['total_comments']}")
            report.append(f"  已分析评论数: {result['analyzed_comments']}")
            report.append(f"  正面评论: {result['positive_count']} ({result['positive_ratio']*100:.2f}%)")
            report.append(f"  负面评论: {result['negative_count']} ({result['negative_ratio']*100:.2f}%)")
            report.append(f"  中性评论: {result['neutral_count']} ({result['neutral_ratio']*100:.2f}%)")
            report.append(f"  平均情感得分: {result['avg_sentiment_score']:.3f}")
        
        report.append("")
        report.append("=" * 80)
        report.append("报告结束")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_topic_report(self, topic_results, type_summary):
        report = []
        report.append("=" * 80)
        report.append("豆瓣电影评论主题分析报告")
        report.append("=" * 80)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("一、总体统计")
        report.append("-" * 80)
        total_movies = len(topic_results)
        total_comments = sum(r['total_comments'] for r in topic_results)
        
        report.append(f"电影总数: {total_movies}")
        report.append(f"评论总数: {total_comments}")
        report.append("")
        
        report.append("二、按电影类型主题统计")
        report.append("-" * 80)
        for movie_type, keywords in type_summary.items():
            report.append(f"\n类型: {movie_type}")
            report.append(f"  热门关键词:")
            for i, (keyword, freq) in enumerate(keywords[:5], 1):
                report.append(f"    {i}. {keyword} (出现次数: {freq})")
        
        report.append("")
        report.append("三、各电影详细主题分析")
        report.append("-" * 80)
        for result in topic_results:
            report.append(f"\n电影: {result['movie_name']} (ID: {result['movie_id']})")
            report.append(f"  评论总数: {result['total_comments']}")
            report.append(f"  主题分布:")
            for i, topic in enumerate(result['topics'], 1):
                report.append(f"    主题{i}: {topic[1]}")
            report.append(f"  热门关键词:")
            for i, (keyword, freq) in enumerate(result['top_keywords'][:5], 1):
                report.append(f"    {i}. {keyword} (出现次数: {freq})")
        
        report.append("")
        report.append("=" * 80)
        report.append("报告结束")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def generate_combined_report(self, sentiment_results, type_stats, topic_results, type_summary):
        report = []
        report.append("=" * 80)
        report.append("豆瓣电影评论情感与主题分析综合报告")
        report.append("=" * 80)
        report.append(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        report.append("第一部分：情感分析")
        report.append("-" * 80)
        total_movies = len(sentiment_results)
        total_comments = sum(r['total_comments'] for r in sentiment_results)
        total_analyzed = sum(r['analyzed_comments'] for r in sentiment_results)
        
        report.append(f"电影总数: {total_movies}")
        report.append(f"评论总数: {total_comments}")
        report.append(f"已分析评论数: {total_analyzed}")
        report.append("")
        
        report.append("按电影类型情感统计:")
        for movie_type, stats in type_stats.items():
            report.append(f"\n类型: {movie_type}")
            report.append(f"  电影数量: {stats['count']}")
            report.append(f"  正面评论数: {stats['total_positive']}")
            report.append(f"  负面评论数: {stats['total_negative']}")
            report.append(f"  中性评论数: {stats['total_neutral']}")
            report.append(f"  平均情感得分: {stats['avg_score']:.3f}")
        
        report.append("")
        report.append("第二部分：主题分析")
        report.append("-" * 80)
        report.append(f"电影总数: {len(topic_results)}")
        report.append(f"评论总数: {sum(r['total_comments'] for r in topic_results)}")
        report.append("")
        
        report.append("按电影类型主题统计:")
        for movie_type, keywords in type_summary.items():
            report.append(f"\n类型: {movie_type}")
            report.append(f"  热门关键词:")
            for i, (keyword, freq) in enumerate(keywords[:5], 1):
                report.append(f"    {i}. {keyword} (出现次数: {freq})")
        
        report.append("")
        report.append("第三部分：各电影综合分析")
        report.append("-" * 80)
        
        sentiment_dict = {r['movie_id']: r for r in sentiment_results}
        topic_dict = {r['movie_id']: r for r in topic_results}
        
        for result in sentiment_results:
            movie_id = result['movie_id']
            report.append(f"\n电影: {result['movie_name']} (ID: {movie_id})")
            report.append(f"  情感分析:")
            report.append(f"    评论总数: {result['total_comments']}")
            report.append(f"    正面评论: {result['positive_count']} ({result['positive_ratio']*100:.2f}%)")
            report.append(f"    负面评论: {result['negative_count']} ({result['negative_ratio']*100:.2f}%)")
            report.append(f"    平均情感得分: {result['avg_sentiment_score']:.3f}")
            
            if movie_id in topic_dict:
                topic_result = topic_dict[movie_id]
                report.append(f"  主题分析:")
                report.append(f"    热门关键词:")
                for i, (keyword, freq) in enumerate(topic_result['top_keywords'][:3], 1):
                    report.append(f"      {i}. {keyword} (出现次数: {freq})")
        
        report.append("")
        report.append("=" * 80)
        report.append("报告结束")
        report.append("=" * 80)
        
        return "\n".join(report)
    
    def save_report(self, report, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"报告已保存到: {filename}")