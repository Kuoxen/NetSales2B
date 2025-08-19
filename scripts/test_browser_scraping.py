#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import asyncio
from playwright.async_api import async_playwright
from app.scrapers.fastmoss import FastmossScraper

async def test_browser_scraping():
    """测试浏览器自动化爬取"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome",headless=False)  # 显示浏览器便于调试
        page = await browser.new_page()
        
        # 创建爬虫实例
        scraper = FastmossScraper()
        scraper.page = page
        
        print("开始测试fastmoss东南亚国家选择...")
        print(f"目标国家: {scraper.COUNTRIES}")
        print("正在访问网站并执行国家选择操作...")
        
        try:
            # 测试基本访问
            await page.goto('https://fastmoss.com')
            print("✓ 成功访问fastmoss网站")
            
            # 测试国家选择功能
            results = await scraper.scrape_merchants({})
            print(f"✓ 完成爬取，获得 {len(results) if results else 0} 条数据")
            
            # 显示部分结果
            if results:
                print("\n前3条数据示例:")
                for i, item in enumerate(results[:3]):
                    print(f"{i+1}. {item}")
                
        except Exception as e:
            print(f"❌ 测试失败: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # 保持浏览器开启以便观察结果
            input("按回车键关闭浏览器...")
            await browser.close()

if __name__ == "__main__":
    asyncio.run(test_browser_scraping())