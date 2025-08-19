# 命令行启动
# /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
#   --remote-debugging-port=9222 \
#   --user-data-dir=/tmp/chrome-user

import json
import time
import random
from playwright.sync_api import sync_playwright
# https://www.geekbi.com/shopee/mall/hot-sale
# 配置
input_file = "tests/shopee_shop_url_Singapore.json"
base_url = "https://shopee.sg/"

def wait_for_user_input(prompt):
    """等待用户输入继续"""
    return input(f"{prompt} (输入回车继续): ")

def random_delay():
    """随机延迟 3-12 秒"""
    delay = random.randint(3, 12)
    print(f"随机等待 {delay} 秒...")
    time.sleep(delay)

def parse_shopee_data(json_file):
    """解析Shopee JSON文件，提取店铺信息"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        shops = []
        if 'data' in data and 'list' in data['data']:
            for shop in data['data']['list']:
                if 'username' in shop and 'mallName' in shop:
                    shops.append({
                        'username': shop['username'],
                        'mallName': shop['mallName'],
                        'mallStar': shop.get('mallStar', 0),
                        'reviewNum': shop.get('reviewNum', 0),
                        'goodsNum': shop.get('goodsNum', 0),
                        'followerNum': shop.get('followerNum', 0)
                    })
        
        print(f"共找到 {len(shops)} 个店铺")
        return shops
    except FileNotFoundError:
        print(f"文件 {json_file} 不存在")
        return []
    except json.JSONDecodeError:
        print(f"文件 {json_file} 格式错误")
        return []
    except Exception as e:
        print(f"解析文件时出错: {e}")
        return []

print("步骤 1: 准备连接到现有 Chrome 浏览器")
print("请确保 Chrome 已启动并使用以下命令行参数：")
print("--remote-debugging-port=9222")
print("或者运行：/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")
print("")
print("如果连接失败，脚本将自动启动新的Chrome实例")

wait_for_user_input("Chrome 已准备好")


# 连接到现有浏览器
print("步骤 2: 连接到 Chrome")
p = sync_playwright().start()


browser = p.chromium.connect_over_cdp("http://localhost:9222")
context = browser.contexts[0]  # 使用已有context
pages = context.pages
page = pages[0]
# page = context.new_page()
# page.goto("https://shopee.sg")



# try:
#     browser = p.chromium.connect_over_cdp("http://localhost:9222")
#     contexts = browser.contexts
#     if contexts:
#         context = contexts[0]
#         pages = context.pages
#         if pages:
#             page = pages[0]
#         else:
#             page = context.new_page()
#     else:
#         context = browser.new_context()
#         page = context.new_page()
    
#     print("成功连接到 Chrome")
# except Exception as e:
#     print(f"连接失败: {e}")
#     print("尝试启动新的Chrome实例...")
#     try:
#         browser = p.chromium.launch(
#             headless=False,
#             executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
#             args=["--remote-debugging-port=9222"]
#         )
#         context = browser.new_context()
#         page = context.new_page()
#         print("成功启动新的Chrome实例")
#     except Exception as e2:
#         print(f"启动新实例也失败: {e2}")
#         print("请手动关闭所有Chrome窗口，然后重新运行脚本")
#         exit()


# 检查是否在 Shopee
# current_url = page.url
# if "shopee.com.my" not in current_url:
#     print("步骤 3: 导航到 Shopee")
#     page.goto('https://shopee.com.my/buyer/login')
#     wait_for_user_input("请确保已登录 Shopee")
# else:
#     print("步骤 3: 已在 Shopee 页面")
#     wait_for_user_input("请确保已登录 Shopee")

# 读取店铺数据
print("步骤 4: 读取店铺数据")
shops = parse_shopee_data(input_file)

if not shops:
    print("没有找到店铺数据，退出程序")
    context.close()
    browser.close()
    p.stop()
    exit()

wait_for_user_input("准备开始访问店铺")


message_content="""
尊敬的卖家朋友们，Ksher开时支付携手 TIktok Shop 收款全线升级，东南亚（菲/泰/越/马/印）本土收款极速到账！新用户首月更可享0手续费，私信回复即可参与！

Dear sellers, 
Ksher Payment has partnered with TIktok Shop to streamline your fund collection process from local shops! Local payment collection in Southeast Asia (Philippines/Thailand/Vietnam/Malaysia/Indonesia) is now fast and cost less! New merchants can enjoy zero fees for the first month. Simply reply to this message to participate our offering and our relationship manager will contact you soon.
"""

# 遍历店铺
for i, shop in enumerate(shops, 1):
    username = shop['username']
    mall_name = shop['mallName']
    shop_url = base_url + username
    
    print(f"\n店铺 {i}/{len(shops)}: {mall_name}")
    print(f"用户名: {username}")
    print(f"链接: {shop_url}")
    print(f"评分: {shop['mallStar']:.2f}")
    print(f"评论数: {shop['reviewNum']:,}")
    print(f"商品数: {shop['goodsNum']:,}")
    print(f"粉丝数: {shop['followerNum']:,}")
    
    try:
        # 访问店铺页面
        print("正在访问店铺页面...")
        page.goto(shop_url, timeout=30000)
        time.sleep(3)
        
        # 等待页面加载
        page.wait_for_load_state('networkidle', timeout=10000)
        
        dm_xpath='/html/body/div[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div[1]/div/div[1]/div[3]/div[2]/a[2]/button'

        dm_button =page.locator(f'xpath={dm_xpath}')
        if dm_button.count()>0:
            dm_button.click()
            time.sleep(2)
            
            # 查找消息输入框
            input_xpath='/html/body/div[4]/div/div[2]/div[3]/div[2]/div[2]/div/div/div/div[1]/div/textarea'
            input_elem=page.locator(f'xpath={input_xpath}')                    
            if input_elem.count()>0:
                print("找到输入框")
                input_elem.click()
                input_elem.type(message_content, delay=100)
                time.sleep(1)
            else:
                print("未找到输入框")
        else:
            print("未找到私信按钮")
                    
    except Exception as e:
        print(f"访问失败: {e}")
    
    # 随机延迟
    if i < len(shops):
        random_delay()

print("\n所有店铺访问完成")
wait_for_user_input("脚本结束")

# 断开连接（不关闭浏览器）
p.stop() 