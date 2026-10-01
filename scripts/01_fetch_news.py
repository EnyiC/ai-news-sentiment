import akshare as ak
import pandas as pd
import os

# 确保数据目录存在
os.makedirs("data/raw", exist_ok=True)

print("开始抓取金融新闻...")

try:
    print("尝试财联社电报（宏观金融新闻）...")
    # 获取财联社电报
    news_df = ak.stock_info_global_cls()
    # 提取需要的列（不同版本接口列名可能微调，这里做一下映射）
    news_df = news_df[['发布时间', '标题', '内容']]
    news_df.columns = ['publish_time', 'title', 'content']
    
    # 保存
    news_df.to_csv("data/raw/financial_news.csv", index=False, encoding='utf-8-sig')
    print(f"✅ 成功抓取 {len(news_df)} 条财联社新闻！")
    print(news_df.head())
    
except Exception as e:
    print(f"⚠️ 财联社接口失败，原因: {e}")
    print("尝试使用东方财富个股新闻（以 000001 平安银行为例）...")
    try:
        # 如果财联社失败，尝试东方财富个股新闻
        news_df = ak.stock_news_em(symbol="000001")
        # 统一列名
        news_df = news_df[['发布时间', '新闻标题', '新闻内容']]
        news_df.columns = ['publish_time', 'title', 'content']
        
        news_df.to_csv("../data/raw/financial_news.csv", index=False, encoding='utf-8-sig')
        print(f"✅ 成功抓取 {len(news_df)} 条东方财富新闻！")
        print(news_df.head())
    except Exception as e2:
        print(f"❌ 所有新闻接口均失败，请检查网络或 Akshare 版本。报错: {e2}")