#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from app.scrapers.fastmoss import FastmossScraper

async def test_fastmoss_api():
    """测试fastmoss API调用"""
    
    scraper = FastmossScraper()
    
    # 测试参数
    filters = {
        'region': 'VN',
        'pagesize': 10
    }
    
    print("测试fastmoss API调用...")
    print(f"测试参数: {filters}")
    
    try:
        merchants = await scraper.scrape_merchants_api(filters)
        print(f"获取到 {len(merchants)} 个商家数据")
        
        if merchants:
            print("\n前3个商家数据:")
            for i, merchant in enumerate(merchants[:3]):
                print(f"{i+1}. {merchant}")
        else:
            print("未获取到数据，可能需要调整cnonce生成算法")
            
    except Exception as e:
        print(f"测试失败: {e}")

if __name__ == "__main__":
    asyncio.run(test_fastmoss_api())