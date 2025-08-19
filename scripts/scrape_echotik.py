#!/usr/bin/env python3
import requests
import csv
import time

# 基础URL和请求头
base_url = "https://echotik.live/api/v1/data/sellers/leaderboard/border-seller"
params = {
    "time_type": "daily",
    "time_range": "20250719", 
    "per_page": 50,
    "product_categories": ""
}

# headers = {
#     "accept": "application/json, text/plain, */*",
#     "authorization": "Bearer 2022862|oE2VUwO6GrgNtMK2hEbPkAPBRQrAQV3j69hMbSaj",
#     "x-region": "MY",
#     "x-currency": "MYR",
#     "x-lang": "zh-CN",
#     "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
# }

# 存储所有数据
all_sellers = []

print("开始爬取echotik数据...")

# 爬取1-50页
for page in range(1, 101):
    params["page"] = page
    
    try:
        # response = requests.get(base_url, params=params, headers=headers)
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if "data" in data:
            sellers = data["data"]
            all_sellers.extend(sellers)
            print(f"第{page}页: 获取{len(sellers)}条数据")
        else:
            print(f"第{page}页: 响应异常 - {data}")
            
    except Exception as e:
        print(f"第{page}页请求失败: {e}")
        
    # 延迟避免请求过快
    time.sleep(0.5)

print(f"总共获取 {len(all_sellers)} 条数据")

# 保存到CSV
if all_sellers:
    csv_file = "echotik_sellers.csv"
    
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'seller_id', 'seller_name', 'cover_url', 'category', 
            'region_id', 'region_name', 'avg_price', 'total_sale_gmv_amt',
            'total_sale_count', 'total_product_cnt', 'is_s_shop'
        ])
        
        writer.writeheader()
        
        for seller in all_sellers:
            writer.writerow({
                'seller_id': seller.get('seller_id', ''),
                'seller_name': seller.get('seller_name', ''),
                'cover_url': seller.get('cover_url', ''),
                'category': seller.get('category', ''),
                'region_id': seller.get('region', {}).get('id', ''),
                'region_name': seller.get('region', {}).get('name', ''),
                'avg_price': seller.get('avg_price', ''),
                'total_sale_gmv_amt': seller.get('total_sale_gmv_amt', ''),
                'total_sale_count': seller.get('total_sale_count', ''),
                'total_product_cnt': seller.get('total_product_cnt', ''),
                'is_s_shop': seller.get('is_s_shop', 0)
            })
    
    print(f"数据已保存到 {csv_file}")
else:
    print("没有获取到数据")

    