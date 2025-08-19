import sys
import os
import asyncio
from playwright.sync_api import sync_playwright
from typing import List, Dict
import asyncio
import json
import time

p=sync_playwright().start()
browser = p.chromium.launch(channel="chrome",headless=False)  # 显示浏览器便于调试
page = browser.new_page()

BASE_URL = "https://www.fastmoss.com/zh/shop-marketing/search?region=&page=1"
page.goto(BASE_URL)
COUNTRIES = ["印度尼西亚", "越南", "泰国", "马来西亚", "菲律宾"]

country_toggle_button_xpath='/html/body/div[1]/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/button'
country_toggle_button_span_xpath='/html/body/div[1]/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/button/span'
# 查找展开/收起按钮
toggle_button =page.locator(f'xpath={country_toggle_button_xpath}')
span_text_elem =page.locator(f'xpath={country_toggle_button_span_xpath}')

if span_text_elem.count()>0:
    span_text = span_text_elem.first.inner_text()
    if span_text == "展开":
        print("地址栏已收起，正在展开...")
        toggle_button.first.click()
    else:
        print("地址栏已展开")


country_group_xpath='/html/body/div[1]/div/div[2]/div[2]/main/div/div[1]/div/div[2]/div[1]/div[2]/div/div/div/div/div'

def select_country(country: str):
    """选择指定国家"""
    try:
        # 查找国家按钮组
        country_group = page.wait_for_selector(f'xpath={country_group_xpath}')        
        # 查找所有国家按钮
        country_buttons = country_group.query_selector_all('.ant-radio-button-label')
        
        for button in country_buttons:
            button_text = button.inner_text()
            if button_text.strip() == country:
                print(f"找到国家按钮: {country}")
                button.click()
                time.sleep(1)
                return
        
        print(f"未找到国家按钮: {country}")
        
    except Exception as e:
        print(f"选择国家 {country} 失败: {e}")

for country in COUNTRIES:
    print(f"正在爬取国家: {country}")
    try:
        select_country(country)                
        # 这里后续添加数据提取逻辑
        print(f"已选择国家: {country}")
        
    except Exception as e:
        print(f"处理国家 {country} 时出错: {e}")
        continue


