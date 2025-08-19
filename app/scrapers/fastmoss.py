from .base import BaseScraper
from typing import List, Dict
import asyncio
import json

class FastmossScraper(BaseScraper):
    BASE_URL = "https://www.fastmoss.com/zh/shop-marketing/search?region=&page=1"
    COUNTRIES = ["印度尼西亚", "越南", "泰国", "马来西亚", "菲律宾"]
    

    
    async def scrape_merchants(self, filters: Dict) -> List[Dict]:
        """遍历东南亚国家爬取商家数据"""
        all_merchants = []
        
        # 访问网站
        await self.page.goto(self.BASE_URL)
        await asyncio.sleep(3)
        
        # 确保地址栏展开
        await self._ensure_region_expanded()
        
        # 遍历每个国家
        for country in self.COUNTRIES:
            print(f"正在爬取国家: {country}")
            try:
                await self._select_country(country)
                await asyncio.sleep(2)
                
                # 这里后续添加数据提取逻辑
                print(f"已选择国家: {country}")
                
            except Exception as e:
                print(f"处理国家 {country} 时出错: {e}")
                continue
        
        return all_merchants
    
    async def _ensure_region_expanded(self):
        """确保地址栏展开"""
        try:
            # 查找展开/收起按钮
            toggle_button = await self.page.wait_for_selector(
                'xpath=/html/body/div[1]/div/div[2]/div[2]/main/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div/button',
                timeout=5000
            )
            
            # 检查按钮状态
            span_text_elem = await self.page.query_selector(
                'xpath=/html/body/div[1]/div/div[2]/div[2]/main/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div/button/span[1]'
            )
            
            if span_text_elem:
                span_text = await span_text_elem.inner_text()
                if span_text == "展开":
                    print("地址栏已收起，正在展开...")
                    await toggle_button.click()
                    await asyncio.sleep(1)
                else:
                    print("地址栏已展开")
            
        except Exception as e:
            print(f"检查地址栏状态失败: {e}")
    
    async def _select_country(self, country: str):
        """选择指定国家"""
        try:
            # 查找国家按钮组
            country_group = await self.page.wait_for_selector(
                'xpath=/html/body/div[1]/div/div[2]/div[2]/main/div/div[1]/div[2]/div[1]/div[2]/div/div/div/div/div',
                timeout=5000
            )
            
            # 在国家按钮组内查找所有国家按钮
            country_buttons = await country_group.query_selector_all('.ant-radio-button-label')
            
            for button in country_buttons:
                button_text = await button.inner_text()
                if button_text.strip() == country:
                    print(f"找到国家按钮: {country}")
                    await button.click()
                    await asyncio.sleep(1)
                    return
            
            print(f"未找到国家按钮: {country}")
            
        except Exception as e:
            print(f"选择国家 {country} 失败: {e}")
    
    async def _extract_merchant_data(self) -> List[Dict]:
        """从页面提取商家数据"""
        merchants = []
        
        try:
            # 等待商家列表加载
            await self.page.wait_for_selector('.merchant-item, .shop-item, [data-testid="merchant"]', timeout=10000)
            
            # 提取商家信息
            merchant_elements = await self.page.query_selector_all('.merchant-item, .shop-item, [data-testid="merchant"]')
            
            for element in merchant_elements:
                try:
                    # 提取基本信息
                    name_elem = await element.query_selector('.name, .title, h3, h4')
                    name = await name_elem.inner_text() if name_elem else "Unknown"
                    
                    # 提取其他信息
                    merchant_data = {
                        'name': name.strip(),
                        'url': await self._extract_merchant_url(element),
                        'platform': await self._extract_platform(element),
                        'region': await self._extract_region(element),
                        'gmv': await self._extract_gmv(element)
                    }
                    
                    merchants.append(merchant_data)
                    
                except Exception as e:
                    print(f"提取单个商家数据失败: {e}")
                    continue
                    
        except Exception as e:
            print(f"提取商家数据失败: {e}")
        
        return merchants
    
    async def _extract_merchant_url(self, element) -> str:
        """提取商家URL"""
        try:
            link = await element.query_selector('a')
            if link:
                href = await link.get_attribute('href')
                return href if href.startswith('http') else f"{self.BASE_URL}{href}"
        except:
            pass
        return ""
    
    async def _extract_platform(self, element) -> str:
        """提取平台信息"""
        try:
            platform_elem = await element.query_selector('.platform, [data-platform]')
            if platform_elem:
                return await platform_elem.inner_text()
        except:
            pass
        return ""
    
    async def _extract_region(self, element) -> str:
        """提取地区信息"""
        try:
            region_elem = await element.query_selector('.region, .country')
            if region_elem:
                return await region_elem.inner_text()
        except:
            pass
        return ""
    
    async def _extract_gmv(self, element) -> str:
        """提取GMV信息"""
        try:
            gmv_elem = await element.query_selector('.gmv, .revenue, .sales')
            if gmv_elem:
                return await gmv_elem.inner_text()
        except:
            pass
        return ""