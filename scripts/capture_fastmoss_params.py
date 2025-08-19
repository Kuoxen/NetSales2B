#!/usr/bin/env python3
import asyncio
from playwright.async_api import async_playwright
import json
import re

async def capture_api_params():
    """使用浏览器捕获真实的API请求参数"""
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        
        # 存储捕获的请求
        captured_requests = []
        
        # 监听网络请求
        async def handle_request(request):
            if 'api/shop/v3/search' in request.url:
                captured_requests.append({
                    'url': request.url,
                    'headers': dict(request.headers),
                    'method': request.method
                })
                print(f"捕获到API请求: {request.url}")
        
        page.on('request', handle_request)
        
        try:
            # 访问网站
            print("正在访问fastmoss网站...")
            await page.goto('https://www.fastmoss.com', wait_until='networkidle')
            
            # 等待页面加载完成
            await page.wait_for_timeout(3000)
            
            # 尝试触发搜索请求
            print("尝试触发搜索...")
            
            # 查找搜索相关元素
            search_elements = await page.query_selector_all('input, button')
            for element in search_elements:
                try:
                    text = await element.inner_text()
                    if 'search' in text.lower() or 'find' in text.lower():
                        await element.click()
                        await page.wait_for_timeout(2000)
                        break
                except:
                    continue
            
            # 等待更多请求
            await page.wait_for_timeout(5000)
            
            # 分析捕获的请求
            if captured_requests:
                print(f"\n捕获到 {len(captured_requests)} 个API请求:")
                for req in captured_requests:
                    print(f"URL: {req['url']}")
                    
                    # 解析URL参数
                    url_parts = req['url'].split('?')
                    if len(url_parts) > 1:
                        params = {}
                        for param in url_parts[1].split('&'):
                            if '=' in param:
                                key, value = param.split('=', 1)
                                params[key] = value
                        
                        print("参数:")
                        for key, value in params.items():
                            print(f"  {key}: {value}")
                        
                        # 分析cnonce和_time的关系
                        if 'cnonce' in params and '_time' in params:
                            cnonce = int(params['cnonce'])
                            time_val = int(params['_time'])
                            
                            print(f"\n分析:")
                            print(f"  cnonce: {cnonce}")
                            print(f"  _time: {time_val}")
                            print(f"  差值: {cnonce - time_val}")
                            print(f"  cnonce长度: {len(str(cnonce))}")
                            
                            # 检查是否是随机数
                            if len(str(cnonce)) == 8:
                                print("  可能是8位随机数")
                            elif cnonce > time_val * 1000:
                                print("  可能是毫秒时间戳")
                            else:
                                print("  可能是其他算法生成")
            else:
                print("未捕获到API请求，尝试手动触发...")
                
                # 在控制台执行JS来查看网络请求
                js_code = """
                // 监听fetch请求
                const originalFetch = window.fetch;
                window.fetch = function(...args) {
                    console.log('Fetch请求:', args[0]);
                    return originalFetch.apply(this, args);
                };
                
                // 查找可能的搜索函数
                console.log('当前页面的全局变量:', Object.keys(window));
                """
                
                await page.evaluate(js_code)
                await page.wait_for_timeout(3000)
        
        except Exception as e:
            print(f"错误: {e}")
        
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(capture_api_params())