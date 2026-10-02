import akshare as ak
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data', 'raw')
os.makedirs(DATA_DIR, exist_ok=True)

all_news = []

# 方法1：财联社300条
try:
    cls_df = ak.stock_info_global_cls()
    cls_df = cls_df[['发布时间', '标题', '内容']]
    cls_df.columns = ['publish_time', 'title', 'content']
    all_news.append(cls_df)
    print(f"✅ 财联社：{len(cls_df)} 条")
except Exception as e:
    print(f"财联社失败: {e}")

# 方法2：多只个股新闻各100条（覆盖不同板块）
stocks = ['000001', '600519', '300750', '000858', '600036']
for code in stocks:
    try:
        df = ak.stock_news_em(symbol=code, max_news=100)
        df = df[['发布时间', '新闻标题', '新闻内容']]
        df.columns = ['publish_time', 'title', 'content']
        all_news.append(df)
        print(f"✅ {code}：{len(df)} 条")
    except Exception as e:
        print(f"{code} 失败: {e}")

# 合并去重
final_df = pd.concat(all_news, ignore_index=True)
final_df = final_df.drop_duplicates(subset=['title']).reset_index(drop=True)

save_path = os.path.join(DATA_DIR, 'expanded_news.csv')
final_df.to_csv(save_path, index=False, encoding='utf-8-sig')
print(f"\n✅ 总计 {len(final_df)} 条去重后新闻，已保存至 expanded_news.csv")