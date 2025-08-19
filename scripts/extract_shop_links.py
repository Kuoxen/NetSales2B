#!/usr/bin/env python3
import csv
import asyncio
from playwright.async_api import async_playwright

# 读取echotik_sellers.csv
input_file = "echotik_sellers.csv"
output_file = "shop_links.csv"

# 目标地区
target_regions = ['TH', 'VN', 'MY', 'PH', 'SG']

results = []

async def extract_links():
    async with async_playwright() as p:
        browser = await p.chromium.launch(channel="chrome",headless=False)
        page = await browser.new_page()
        
        # 先打开登录页面
        print("正在打开登录页面...")
        await page.goto('https://echotik.live/board')
        
        # 等待用户手动登录
        print("请在浏览器中完成登录，然后在终端输入 'ok' 继续...")
        user_input = input("输入 'ok' 继续: ")
        
        if user_input.lower() != 'ok':
            print("取消操作")
            await browser.close()
            return
            
        print("开始处理CSV文件...")
        
        # 读取CSV文件
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                region_id = row.get('region_id', '')
                seller_id = row.get('seller_id', '')
                seller_name = row.get('seller_name', '')
                
                # 检查是否为目标地区
                if region_id in target_regions and seller_id:
                    print(f"处理商家: {seller_name} ({region_id})")
                    
                    # 构建URL
                    shop_url = f"https://echotik.live/shops/{seller_id}"
                    
                    try:
                        # 访问页面
                        await page.goto(shop_url)
                        await page.wait_for_load_state('networkidle')
                        
                        # 使用XPath查找元素
                        xpath = '/html/body/div[1]/section/section/div/main/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[2]/span/a'
                        link_element = await page.query_selector(f'xpath={xpath}')
                        
                        if link_element:
                            href = await link_element.get_attribute('href')
                            if href:
                                print(f"  找到链接: {href}")
                                
                                results.append({
                                    'seller_id': seller_id,
                                    'seller_name': seller_name,
                                    'region_id': region_id,
                                    'shop_url': shop_url,
                                    'extracted_link': href
                                })
                            else:
                                print(f"  链接为空")
                        else:
                            print(f"  未找到链接元素")
                            
                    except Exception as e:
                        print(f"  处理失败: {e}")
                        
                    # 延迟避免请求过快
                    await asyncio.sleep(1)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(extract_links())
    
    print(f"处理完成，共获取 {len(results)} 条链接")
    
    # 保存结果
    if results:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'seller_id', 'seller_name', 'region_id', 'shop_url', 'extracted_link'
            ])
            
            writer.writeheader()
            writer.writerows(results)
        
        print(f"结果已保存到 {output_file}")
    else:
        print("没有获取到任何链接")