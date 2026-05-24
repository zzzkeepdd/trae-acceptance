---
name: trae-acceptance
description: Harness 楠屾敹寮曟搸 鈥?鐙珛鐨勯」鐩獙鏀?skill銆侾laywright 娴忚鍣ㄨ嚜鍔ㄥ寲鎴浘 + 瑙嗚鍒嗘瀽 + 鍙岃建澶嶇洏璇勫垎銆傚彲琚?Harness 璋冪敤锛屼篃鍙嫭绔嬩娇鐢ㄣ€?version: 1.0.0
phase: stable
---

# Trae Acceptance v1.0

Harness 鐨勯獙鏀跺悗绔€備笉璐熻矗娴佺▼鎺у埗鈥斺€斿彧璐熻矗**楠岃瘉缁撴灉**銆?
## 涓夌楠屾敹妯″紡

| 妯″紡 | 瑙﹀彂璇?| 閫傜敤椤圭洰 | 浜у嚭 |
|------|------|------|------|
| **娴忚鍣ㄨ嚜鍔ㄥ寲** | `uat-browser` | GUI 搴旂敤 | 鎴浘 + 浜や簰璁板綍 |
| **浠ｇ爜楠屾敹** | `uat-code` | CLI/API/搴?| 娴嬭瘯鎶ュ憡 + lint |
| **瑙嗚楠屾敹** | `uat-visual` | 瑙嗛/璁捐 | 甯ф埅鍥?+ 涓€鑷存€ф姤鍛?|

## 蹇€熶娇鐢?
```powershell
# 娴忚鍣ㄩ獙鏀讹紙GUI 椤圭洰锛?python scripts/run_uat.py browser --project <椤圭洰鐩綍> --url http://localhost:3000

# 浠ｇ爜楠屾敹锛堥潪 GUI 椤圭洰锛?python scripts/run_uat.py code --project <椤圭洰鐩綍>

# 瑙嗚楠屾敹锛堣棰?璁捐椤圭洰锛?python scripts/run_uat.py visual --project <椤圭洰鐩綍>

# 鍙岃建澶嶇洏锛堟墍鏈夐」鐩被鍨嬮€氱敤锛?python scripts/run_review.py --project <椤圭洰鐩綍>
```

## 琚?Harness 璋冪敤

Harness 鐨?`project-profile.json` 閫氳繃 `tools` 瀛楁璋冪敤锛?
```yaml
tools:
  - skill: trae-acceptance
    mode: browser
    args: {url: "http://localhost:3000"}
```

## 鐩綍缁撴瀯

```
trae-acceptance/
鈹溾攢鈹€ SKILL.md
鈹溾攢鈹€ README.md
鈹溾攢鈹€ scripts/
鈹?  鈹溾攢鈹€ run_uat.py          # 缁熶竴鍏ュ彛
鈹?  鈹溾攢鈹€ browser_uat.py      # Playwright 娴忚鍣ㄨ嚜鍔ㄥ寲
鈹?  鈹溾攢鈹€ code_uat.py         # 浠ｇ爜楠屾敹锛堟祴璇?lint锛?鈹?  鈹溾攢鈹€ visual_uat.py       # 瑙嗚楠屾敹锛堝抚鍒嗘瀽锛?鈹?  鈹斺攢鈹€ review.py           # 鍙岃建澶嶇洏璇勫垎
```

## 渚濊禆

```bash
pip install playwright
playwright install chromium
```
