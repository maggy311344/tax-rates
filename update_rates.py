import json
from datetime import datetime
    
def convert_to_table_format(raw_data):
    """
    將計算用的稅率結構，全自動轉換為好讀的『表格 JSON 格式』
    """
    calc_json = {}
    for fy, identities in raw_data.items():
        # 網頁選單格式為 "2025/26"，將 Python 的 "2025-26" 轉換為 "2025/26"
        web_fy_key = fy.replace("-", "/")
        
        calc_json[web_fy_key] = {
            "resident": [],
            "foreign": [] # 對齊網頁前端使用的 "foreign" 屬性名
        }
        
        # 轉換居民稅率級距
        prev_limit = 0
        for item in identities["resident"]:
            calc_json[web_fy_key]["resident"].append({
                "min": prev_limit,
                "max": item["limit"],
                "rate": item["rate"]
            })
            if item["limit"] is not None:
                prev_limit = item["limit"]
                
        # 轉換外國居民稅率級距
        prev_limit = 0
        for item in identities["foreign_resident"]:
            calc_json[web_fy_key]["foreign"].append({
                "min": prev_limit,
                "max": item["limit"],
                "rate": item["rate"]
            })
            if item["limit"] is not None:
                prev_limit = item["limit"]
                
    return calc_json
    
    table_json = {
        "description": "澳洲歷年稅率級距表 (全自動表格化產出)",
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tables": []
    }
    
    for fy, identities in raw_data.items():
        fy_table = {
            "financial_year": fy,
            "columns": ["identity", "income_range_aud", "marginal_rate"],
            "rows": []
        }
        
        # 1. 處理居民部分
        prev_limit = 0
        for item in identities["resident"]:
            limit = item["limit"]
            rate = f"{item['rate'] * 100}%" if item['rate'] > 0 else "0%"
            
            if limit is None:
                income_range = f"${prev_limit + 1:,.0f} 以上"
            else:
                income_range = f"${prev_limit:,.0f} – ${limit:,.0f}"
                prev_limit = limit
                
            fy_table["rows"].append({
                "identity": "Resident (稅務居民)",
                "income_range_aud": income_range,
                "marginal_rate": rate
            })
            
        # 2. 處理非居民部分
        prev_limit = 0
        for item in identities["foreign_resident"]:
            limit = item["limit"]
            rate = f"{item['rate'] * 100}%"
            
            if limit is None:
                income_range = f"${prev_limit + 1:,.0f} 以上"
            else:
                income_range = f"${prev_limit:,.0f} – ${limit:,.0f}"
                prev_limit = limit
                
            fy_table["rows"].append({
                "identity": "Foreign Resident (非居民)",
                "income_range_aud": income_range,
                "marginal_rate": rate
            })
            
        table_json["tables"].append(fy_table)
        
    return table_json


def fetch_and_update():
    current_year = datetime.now().year
    
    # 核心原始資料 (便於程式比對與動態計算)
    rates_data = {
        "2023-24": {
            "resident": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.19 }, { "limit": 120000, "rate": 0.325 }, { "limit": 180000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
            "foreign_resident": [{ "limit": 120000, "rate": 0.325 }, { "limit": 180000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }]
        },
        "2024-25": {
            "resident": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.16 }, { "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
            "foreign_resident": [{ "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }]
        },
        "2025-26": {
            "resident": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.16 }, { "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
            "foreign_resident": [{ "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }]
        },
        "2026-27": {
            "resident": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.15 }, { "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
            "foreign_resident": [{ "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }]
        }
    }
    
    # 【自動推進邏輯】
    next_fy_start = current_year if datetime.now().month >= 7 else current_year - 1
    next_fy_str = f"{next_fy_start}-{str(next_fy_start+1)[2:]}"
    
    if next_fy_str not in rates_data:
        rates_data[next_fy_str] = {
            "resident": [{ "limit": 18200, "rate": 0 }, { "limit": 45000, "rate": 0.15 }, { "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }],
            "foreign_resident": [{ "limit": 135000, "rate": 0.30 }, { "limit": 190000, "rate": 0.37 }, { "limit": None, "rate": 0.45 }]
        }

    # 🌟 關鍵步驟：在寫入檔案前，呼叫轉換器將其變成表格格式 JSON
    final_table_json = convert_to_table_format(rates_data)

    # 將結果寫入檔案
    with open('tax-rates-table.json', 'w', encoding='utf-8') as f:
        json.dump(final_table_json, f, indent=2, ensure_ascii=False)
        
    print(f"表格化 JSON 檔案已全自動更新成功！目前判定財年區間為: {next_fy_str}")

    # 🌟 關鍵新步驟：產生計算機專用的 JSON 資料結構
    final_calc_json = convert_to_calculator_format(rates_data)

    # 將計算機專用格式寫入 'tax-rates.json' (這就是你網頁 fetch 的那個檔案)
    with open('tax-rates.json', 'w', encoding='utf-8') as f:
        json.dump(final_calc_json, f, indent=2, ensure_ascii=False)
        
    print("計算機專用 tax-rates.json 檔案也同步產出完成！")

if __name__ == "__main__":
    fetch_and_update()
