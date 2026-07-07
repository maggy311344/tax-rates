import json
from datetime import datetime

def fetch_and_update():
    current_year = datetime.now().year
    
    # 重新規劃 JSON 結構，區分居民與非居民
    rates_data = {
        "2023-24": {
            "resident": [
                { "limit": 18200, "rate": 0 }, 
                { "limit": 45000, "rate": 0.19 }, 
                { "limit": 120000, "rate": 0.325 }, 
                { "limit": 180000, "rate": 0.37 }, 
                { "limit": None, "rate": 0.45 }
            ],
            "foreign_resident": [
                { "limit": 120000, "rate": 0.325 },
                { "limit": 180000, "rate": 0.37 },
                { "limit": None, "rate": 0.45 }
            ]
        },
        "2024-25": {
            "resident": [
                { "limit": 18200, "rate": 0 }, 
                { "limit": 45000, "rate": 0.16 }, 
                { "limit": 135000, "rate": 0.30 }, 
                { "limit": 190000, "rate": 0.37 }, 
                { "limit": None, "rate": 0.45 }
            ],
            "foreign_resident": [
                { "limit": 135000, "rate": 0.30 },
                { "limit": 190000, "rate": 0.37 },
                { "limit": None, "rate": 0.45 }
            ]
        },
        "2025-26": {
            "resident": [
                { "limit": 18200, "rate": 0 }, 
                { "limit": 45000, "rate": 0.16 }, 
                { "limit": 135000, "rate": 0.30 }, 
                { "limit": 190000, "rate": 0.37 }, 
                { "limit": None, "rate": 0.45 }
            ],
            "foreign_resident": [
                { "limit": 135000, "rate": 0.30 },
                { "limit": 190000, "rate": 0.37 },
                { "limit": None, "rate": 0.45 }
            ]
        },
        "2026-27": {
            "resident": [
                { "limit": 18200, "rate": 0 }, 
                { "limit": 45000, "rate": 0.15 }, # 2026-27 居民第一級降至 15%
                { "limit": 135000, "rate": 0.30 }, 
                { "limit": 190000, "rate": 0.37 }, 
                { "limit": None, "rate": 0.45 }
            ],
            "foreign_resident": [
                { "limit": 135000, "rate": 0.30 },
                { "limit": 190000, "rate": 0.37 },
                { "limit": None, "rate": 0.45 }
            ]
        }
    }
    
    # 【自動推進邏輯】
    next_fy_start = current_year if datetime.now().month >= 7 else current_year - 1
    next_fy_str = f"{next_fy_start}-{str(next_fy_start+1)[2:]}"
    
    if next_fy_str not in rates_data:
        # 未來年度自動沿用 Stage 3 減稅後的最新基本稅率
        rates_data[next_fy_str] = {
            "resident": [
                { "limit": 18200, "rate": 0 },
                { "limit": 45000, "rate": 0.15 },
                { "limit": 135000, "rate": 0.30 },
                { "limit": 190000, "rate": 0.37 },
                { "limit": None, "rate": 0.45 }
            ],
            "foreign_resident": [
                { "limit": 135000, "rate": 0.30 },
                { "limit": 190000, "rate": 0.37 },
                { "limit": None, "rate": 0.45 }
            ]
        }

    # 將結果寫入檔案
    with open('tax-rates.json', 'w', encoding='utf-8') as f:
        json.dump(rates_data, f, indent=2, ensure_ascii=False)
    print(f"稅率檔案（包含非居民稅率）已全自動更新成功！目前判定財年區間為: {next_fy_str}")

if __name__ == "__main__":
    fetch_and_update()
