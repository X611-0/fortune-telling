import random
from datetime import datetime
from typing import Dict

class FortuneCalculator:
    def __init__(self):
        self.fortune_types = {
            "daily": "今日运势",
            "love": "姻缘运势", 
            "career": "事业运势",
            "wealth": "财运运势",
            "health": "健康运势"
        }
        
        self.fortune_levels = ["大吉", "吉", "中吉", "小吉", "平", "凶", "大凶"]
        
    def calculate_daily_fortune(self, bazi_data: Dict) -> Dict:
        """计算今日运势"""
        fortune_level = random.choice(self.fortune_levels)
        return {
            "type": "daily",
            "level": fortune_level,
            "description": self._generate_daily_description(fortune_level),
            "lucky_color": self._get_lucky_color(),
            "lucky_number": random.randint(1, 9),
            "advice": self._get_advice(fortune_level)
        }
    
    def calculate_love_fortune(self, bazi_data: Dict) -> Dict:
        """计算姻缘运势"""
        fortune_level = random.choice(self.fortune_levels[:4])  # 姻缘只取吉运
        return {
            "type": "love",
            "level": fortune_level,
            "description": self._generate_love_description(fortune_level),
            "meeting_chance": f"{random.randint(30, 90)}%",
            "compatibility": self._get_compatibility()
        }
    
    def _generate_daily_description(self, level: str) -> str:
        descriptions = {
            "大吉": "今日运势极佳，诸事顺利，宜把握机会",
            "吉": "运势良好，做事顺心，可尝试新事物",
            "中吉": "运势平稳，小有收获，保持积极心态",
            "小吉": "略有小运，需努力争取，不可懈怠",
            "平": "运势平常，按部就班，稳中求进",
            "凶": "运势不佳，谨慎行事，避免冲动",
            "大凶": "运势极差，宜静不宜动，保守为上"
        }
        return descriptions.get(level, "运势平稳")
    
    def _generate_love_description(self, level: str) -> str:
        descriptions = {
            "大吉": "桃花运旺盛，有机会遇到心仪对象",
            "吉": "感情运势良好，关系和谐发展",
            "中吉": "姻缘平稳，需主动把握机会",
            "小吉": "略有桃花，但需谨慎选择"
        }
        return descriptions.get(level, "感情运势平稳")
    
    def _get_lucky_color(self) -> str:
        colors = ["红色", "黄色", "蓝色", "绿色", "白色", "黑色", "紫色"]
        return random.choice(colors)
    
    def _get_advice(self, level: str) -> str:
        advice = {
            "大吉": "大胆行动，把握良机",
            "吉": "积极进取，会有收获",
            "中吉": "稳扎稳打，循序渐进",
            "小吉": "保持耐心，等待时机",
            "平": "按部就班，不宜冒进",
            "凶": "谨慎行事，避免风险",
            "大凶": "以静制动，保守为上"
        }
        return advice.get(level, "保持平常心")
    
    def _get_compatibility(self) -> str:
        signs = ["鼠", "牛", "虎", "兔", "龙", "蛇", "马", "羊", "猴", "鸡", "狗", "猪"]
        return f"与{random.choice(signs)}相配"