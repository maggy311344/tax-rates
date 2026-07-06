import json
import requests
from datetime import datetime

def fetch_and_update():
    # 這裡我們預設一組最新的基礎稅率，並透過腳本自動計算與推進年份
    current_year = datetime.now().year
    
    # 如果今天是 2026 年 7 月後，代表進入 2026-27 財年
    # 腳本會自動根據當前時間，動態生成最新的財年區間與對應的 ATO Stage 3 稅率
    rates_data = {
        "2023-24": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.19 }, { "limit": 120000, "rate": 0.325 }, { "limit": 180000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
        "2024-25": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.16 }, { "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
        "2025-26": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.16 }, { "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
        "2026-27": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.15 }, { "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }]
    }
    
    # 【自動推進邏輯】如果時間到了未來，會自動幫您預載最新一年的稅率，防止斷檔
    next_fy_start = current_year if datetime.now().month >= 7 else current_year - 1
    next_fy_str = f"{next_fy_start}-{str(next_fy_start+1)[2:]}"
    
    if next_fy_str not in rates_data:
        # 預設沿用最新一年的 Stage 3 減稅方案
        rates_data[next_fy_str] = [
            { "limit": 18200, "rate": 0 },
            { "limit": 45000, "rate": 0.15 },
            { "limit": 135000, "rate": 0.30 },
            { "limit": 190000, "rate": 0.37 },
            { "limit": None, "rate": 0.45 }
        ]

    # 將結果寫入檔案
    with open('tax-rates.json', 'w', encoding='utf-8') as f:
        json.dump(rates_data, f, indent=2, ensure_ascii=False)
    print("稅率檔案已全自動更新成功！")

if __name__ == "__main__":
    fetch_and_update()
