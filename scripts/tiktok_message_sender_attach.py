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
    delay = random.randint(30, 120)
    print(f"随机等待 {delay} 秒...")
    time.sleep(delay)

print("步骤 1: 准备连接到现有 Chrome 浏览器")
print("请确保 Chrome 已启动并使用以下命令行参数：")
print("--remote-debugging-port=9222")
print("或者运行：/Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222")

wait_for_user_input("Chrome 已准备好")

# 连接到现有浏览器
print("步骤 2: 连接到 Chrome")
p = sync_playwright().start()
try:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    contexts = browser.contexts
    if contexts:
        context = contexts[0]
        pages = context.pages
        if pages:
            page = pages[0]
        else:
            page = context.new_page()
    else:
        context = browser.new_context()
        page = context.new_page()
    
    print("成功连接到 Chrome")
except Exception as e:
    print(f"连接失败: {e}")
    print("请确保 Chrome 使用 --remote-debugging-port=9222 启动")
    exit()

# 检查是否在 TikTok
current_url = page.url
if "tiktok.com" not in current_url:
    print("步骤 3: 导航到 TikTok")
    page.goto('https://www.tiktok.com')
    wait_for_user_input("请确保已登录 TikTok")
else:
    print("步骤 3: 已在 TikTok 页面")
    wait_for_user_input("请确保已登录 TikTok")

# 读取账户链接
print("步骤 4: 读取账户链接")

 = []
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
        
        # 查找私信按钮
        
        dm_xpath='/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[1]/div[2]/a/button/div/div'
        dm_xpath='/html/body/div[1]/div[2]/div[2]/div/div/div[1]/div[2]/div[2]/a/button
        dm_button =page.locator(f'xpath={dm_xpath}')
        if dm_button.count()>0:
            dm_button.click()
            time.sleep(2)
            
            # 查找消息输入框
            input_xpath='/html/body/div[1]/div[2]/div[2]/div/div[3]/div[4]/div/div[1]/div/div[2]/div[2]'
            input_elem=page.locator(f'xpath={input_xpath}')                                
            if input_elem.count()>0:
                print("找到输入框")
                input_elem.click()
                input_elem.type(message_content, delay=100)
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
                    wait_for_user_input("手动发送后继续")
            else:
                print("未找到输入框")
                wait_for_user_input("手动操作后继续")
        else:
            print("未找到私信按钮")
            wait_for_user_input("手动操作后继续")
            
    except Exception as e:
        print(f"处理失败: {e}")
        wait_for_user_input("处理下一个账户？")
    
    # 随机延迟
    if i < len(accounts):
        random_delay()

print("\n所有账户处理完成")
wait_for_user_input("脚本结束")

# 断开连接（不关闭浏览器）
p.stop()