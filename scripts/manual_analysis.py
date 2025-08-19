#!/usr/bin/env python3
import requests
import time
import random

def test_different_cnonce_methods():
    """测试不同的cnonce生成方法"""
    
    base_url = "https://www.fastmoss.com/api/shop/v3/search"
    current_time = int(time.time())
    
    # 不同的cnonce生成方法
    methods = {
        "8位随机数": str(random.randint(10000000, 99999999)),
        "当前时间戳": str(current_time),
        "毫秒时间戳": str(int(time.time() * 1000)),
        "时间戳后8位": str(current_time)[-8:],
        "固定值88547127": "88547127",  # 从原始URL中的值
        "时间戳+随机": str(current_time) + str(random.randint(100, 999)),
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.fastmoss.com/',
        'Origin': 'https://www.fastmoss.com',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }
    
    for method_name, cnonce in methods.items():
        params = {
            'page': 1,
            'pagesize': 10,
            'order': '1,2',
            'region': 'VN',
            '_time': current_time,
            'cnonce': cnonce
        }
        
        print(f"\n测试方法: {method_name}")
        print(f"cnonce: {cnonce}")
        print(f"_time: {current_time}")
        
        try:
            response = requests.get(base_url, params=params, headers=headers, timeout=10)
            print(f"状态码: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    print("✓ 成功! 响应数据:")
                    print(f"  数据类型: {type(data)}")
                    if isinstance(data, dict):
                        print(f"  键: {list(data.keys())}")
                        if 'data' in data:
                            print(f"  data类型: {type(data['data'])}")
                except:
                    print("✓ 成功但非JSON响应")
                    print(f"  响应内容: {response.text[:200]}...")
            else:
                print(f"✗ 失败 - 状态码: {response.status_code}")
                if response.text:
                    print(f"  错误信息: {response.text[:200]}")
                    
        except requests.exceptions.RequestException as e:
            print(f"✗ 请求异常: {e}")
        
        time.sleep(1)  # 避免请求过快

if __name__ == "__main__":
    print("开始测试fastmoss API的cnonce参数...")
    test_different_cnonce_methods()