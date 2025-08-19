import csv
import time
import random
from playwright.sync_api import sync_playwright

# 配置
input_file = "shop_links.csv"
message_content = """
尊敬的卖家朋友们，Ksher开时支付携手 TIktok Shop 收款全线升级，东南亚（菲/泰/越/马/印）本土收款极速到账！新用户首月更可享0手续费，私信回复即可参与！

Dear sellers, 
Ksher Payment has partnered with TIktok Shop to streamline your fund collection process from local shops! Local payment collection in Southeast Asia (Philippines/Thailand/Vietnam/Malaysia/Indonesia) is now fast and cost less! New merchants can enjoy zero fees for the first month. Simply reply to this message to participate our offering and our relationship manager will contact you soon.
"""  # 修改这里的私信内容

def wait_for_user_input(prompt):
    """等待用户输入继续"""
    return input(f"{prompt} (输入回车继续): ")

def random_delay():
    """随机延迟 30-120 秒"""
    delay = random.randint(3, 12)
    print(f"随机等待 {delay} 秒...")
    time.sleep(delay)

# 启动浏览器
print("步骤 1: 启动浏览器")
p = sync_playwright().start()
# browser = p.chromium.launch(channel="chrome", headless=False)
browser = p.chromium.launch(
    headless=False,
    executable_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
)

browser = p.chromium.launch(headless=False)
context = browser.new_context()
page = context.new_page()

# 登录 TikTok
print("步骤 2: 打开 TikTok 登录页面")
page.goto('https://www.tiktok.com')
wait_for_user_input("请完成 TikTok 登录")

# 读取账户链接
print("步骤 3: 读取账户链接")
accounts = []
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        accounts = list(reader)
    print(f"共找到 {len(accounts)} 个账户")
except FileNotFoundError:
    print(f"文件 {input_file} 不存在")
    exit()

wait_for_user_input("准备开始发送私信")

# 遍历账户发送私信
for i, account in enumerate(accounts, 1):
    link = account.get('extracted_link', '')
    seller_name = account.get('seller_name', '')
    
    if not link:
        print(f"账户 {i}: {seller_name} - 无链接，跳过")
        continue
        
    print(f"\n账户 {i}/{len(accounts)}: {seller_name}")
    print(f"链接: {link}")
    
    try:
        # 访问账户页面
        page.goto(link, timeout=30000)
        time.sleep(3)
        
        # 查找私信按钮 (常见的选择器)
        message_selectors = [
            '[data-e2e="user-page-message-button"]',
            'button[data-e2e="message-button"]',
            'button:has-text("Message")',
            'button:has-text("私信")',
            '[aria-label="Message"]'
        ]
        
        message_button = None
        for selector in message_selectors:
            message_button = page.query_selector(selector)
            if message_button:
                break
                
        if message_button:
            print("找到私信按钮，点击...")
            message_button.click()
            time.sleep(2)
            
            # 查找消息输入框
            input_selectors = [
                '[data-e2e="message-input"]',
                'textarea[placeholder*="message"]',
                'textarea[placeholder*="私信"]',
                '[contenteditable="true"]'
            ]
            
            input_box = None
            for selector in input_selectors:
                input_box = page.query_selector(selector)
                if input_box:
                    break
                    
            if input_box:
                print("输入私信内容...")
                input_box.fill(message_content)
                time.sleep(1)
                
                # 查找发送按钮
                send_selectors = [
                    '[data-e2e="send-button"]',
                    'button:has-text("Send")',
                    'button:has-text("发送")',
                    '[aria-label="Send"]'
                ]
                
                send_button = None
                for selector in send_selectors:
                    send_button = page.query_selector(selector)
                    if send_button:
                        break
                        
                if send_button:
                    wait_for_user_input("确认发送私信？")
                    send_button.click()
                    print("私信已发送")
                else:
                    print("未找到发送按钮")
            else:
                print("未找到输入框")
        else:
            print("未找到私信按钮")
            
    except Exception as e:
        print(f"处理失败: {e}")
    
    # 随机延迟
    if i < len(accounts):
        random_delay()

print("\n所有账户处理完成")
wait_for_user_input("按回车关闭浏览器")

# 关闭浏览器
context.close()
browser.close()
p.stop()