#!/usr/bin/env python3
import requests
import re
import time
import random
from bs4 import BeautifulSoup

def analyze_fastmoss_api():
    """分析fastmoss网站的API参数生成规则"""
    
    # 1. 获取主页HTML，查找JS文件
    print("正在获取网站主页...")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        response = requests.get('https://www.fastmoss.com', headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 查找所有script标签
        scripts = soup.find_all('script', src=True)
        js_files = [script['src'] for script in scripts if script.get('src')]
        
        print(f"找到 {len(js_files)} 个JS文件")
        
        # 2. 分析JS文件中的cnonce生成逻辑
        for js_file in js_files[:5]:  # 只检查前5个文件
            if js_file.startswith('//'):
                js_url = 'https:' + js_file
            elif js_file.startswith('/'):
                js_url = 'https://www.fastmoss.com' + js_file
            else:
                js_url = js_file
                
            print(f"分析JS文件: {js_url}")
            
            try:
                js_response = requests.get(js_url, headers=headers)
                js_content = js_response.text
                
                # 搜索cnonce相关代码
                cnonce_patterns = [
                    r'cnonce["\']?\s*[:=]\s*([^,\s}]+)',
                    r'cnonce.*?=.*?(\d+)',
                    r'Math\.random\(\).*?\*.*?(\d+)',
                    r'Date\.now\(\)',
                    r'timestamp.*?cnonce',
                ]
                
                for pattern in cnonce_patterns:
                    matches = re.findall(pattern, js_content, re.IGNORECASE)
                    if matches:
                        print(f"  找到可能的cnonce生成逻辑: {matches}")
                        
            except Exception as e:
                print(f"  无法获取JS文件: {e}")
                
    except Exception as e:
        print(f"获取主页失败: {e}")
    
    # 3. 尝试常见的cnonce生成方法
    print("\n尝试常见的cnonce生成方法:")
    
    methods = {
        "随机8位数": lambda: str(random.randint(10000000, 99999999)),
        "时间戳": lambda: str(int(time.time())),
        "时间戳毫秒": lambda: str(int(time.time() * 1000)),
        "随机数+时间": lambda: str(random.randint(1000, 9999)) + str(int(time.time()))[-4:],
    }
    
    current_time = int(time.time())
    
    for method_name, method_func in methods.items():
        cnonce = method_func()
        test_url = f"https://www.fastmoss.com/api/shop/v3/search?page=1&pagesize=10&order=1,2&region=VN&_time={current_time}&cnonce={cnonce}"
        
        print(f"\n测试方法: {method_name}")
        print(f"生成的cnonce: {cnonce}")
        print(f"测试URL: {test_url}")
        
        try:
            response = requests.get(test_url, headers=headers)
            print(f"响应状态: {response.status_code}")
            if response.status_code == 200:
                print("✓ 可能有效!")
                print(f"响应内容: {response.text[:200]}...")
            else:
                print("✗ 无效")
        except Exception as e:
            print(f"请求失败: {e}")

if __name__ == "__main__":
    analyze_fastmoss_api()