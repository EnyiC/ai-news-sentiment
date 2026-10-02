import pandas as pd
import os
import time
from openai import OpenAI

# 1. 初始化 DeepSeek 客户端（记得替换你的 API Key）
client = OpenAI(api_key="sk-70e114a33ee74989a49945506c54ecc9", base_url="https://api.deepseek.com/v1")

# 2. 读取新闻数据
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data', 'raw')
news_df = pd.read_csv(os.path.join(DATA_DIR, 'financial_news.csv'))

# 【新增】数据清洗：丢弃标题或内容为空的行
news_df = news_df.dropna(subset=['title', 'content']).reset_index(drop=True)

# 3. 定义情感打分函数
def get_sentiment(text):
    prompt = f"""
    你是一名专业的金融分析师。请判断以下新闻对A股市场是利好还是利空。
    请只输出一个数字，介于 -1 到 1 之间：
    -1 表示极度利空，0 表示中性，1 表示极度利好。
    不要输出任何其他文字。
    
    新闻标题：{text}
    """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        return float(response.choices[0].message.content.strip())
    except Exception as e:
        print(f"打分失败: {e}")
        return 0.0

# 4. 循环打分并加入进度条
scores = []
print(f"开始 AI 情感打分，共 {len(news_df)} 条新闻...")
for idx, row in news_df.iterrows():
    # 用标题+内容的前100字作为输入，节省 Token
    # 【修正】用 str() 强转，防止空值报错
    title = str(row['title'])[:100]
    content = str(row['content'])[:100]
    text = f"{title}。{content}"
    
    score = get_sentiment(text)
    scores.append(score)
    
    # 【修正】打印时也强制转字符串
    print(f"进度: {idx+1}/{len(news_df)} | 标题: {title[:20]}... | 得分: {score}")
    time.sleep(0.5) # 防止请求过快被限流

# 5. 保存结果
news_df['sentiment_score'] = scores
news_df.to_csv(os.path.join(DATA_DIR, 'news_with_sentiment.csv'), index=False, encoding='utf-8-sig')
print("✅ 情感打分完成，结果已保存至 news_with_sentiment.csv")