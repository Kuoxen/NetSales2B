import csv
import asyncio
from playwright.sync_api import sync_playwright
import time
# 基本设置
input_file = "echotik_sellers.csv"
output_file = "shop_links.csv"
target_regions = ['TH', 'VN', 'MY', 'PH', 'SG']
results = []

# 启动浏览器
p = sync_playwright().start()
browser = p.chromium.launch(channel="chrome", headless=False)

# 创建浏览器上下文来保持登录状态
context = browser.new_context()

# 打开登录页面
page = context.new_page()
page.goto('https://echotik.live/board')
print("请在浏览器中完成登录，然后在终端输入 'ok' 继续...")

# 等待用户输入
user_input = input("输入 'ok' 继续: ")

# 读取CSV并处理
with open(input_file, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        region_id = row.get('region_id', '')
        seller_id = row.get('seller_id', '')
        seller_name = row.get('seller_name', '')
        
        if region_id in target_regions and seller_id:
            print(f"处理商家: {seller_name} ({region_id})")
            shop_url = f"https://echotik.live/shops/{seller_id}"
            
            try:
                # 在同一个上下文中创建新页面，保持登录状态
                page = context.new_page()
                page.goto(shop_url, timeout=30000)  # 30秒超时
                # 使用固定等待时间替代networkidle
                time.sleep(3)
                
                xpath = '/html/body/div[1]/section/section/div/main/div/div[2]/div[2]/div/div/div[2]/div[1]/div/div/div/table/tbody/tr[1]/td[2]/span/a'
                link_element = page.query_selector(f'xpath={xpath}')
                
                if link_element:
                    href = link_element.get_attribute('href')
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
                
            # 关闭当前页面释放内存
            page.close()
            
            # 增加10秒间隔避免被封
            print("  等待 10 秒...")
            time.sleep(10)

# 保存结果
if results:
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['seller_id', 'seller_name', 'region_id', 'shop_url', 'extracted_link'])
        writer.writeheader()
        writer.writerows(results)
    print(f"结果已保存到 {output_file}")
else:
    print("没有获取到任何链接")

# 关闭浏览器
context.close()
browser.close()
p.stop()