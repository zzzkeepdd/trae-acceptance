# Trae Acceptance

> Harness 楠屾敹寮曟搸 鈥?鐙珛鐨勯」鐩獙鏀?skill銆?
涓嶈礋璐ｆ祦绋嬫帶鍒讹紝鍙礋璐?*楠岃瘉缁撴灉**銆?
[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

---

## 涓夌楠屾敹妯″紡

| 妯″紡 | 鍛戒护 | 閫傜敤椤圭洰 | 浜у嚭 |
|------|------|------|------|
| **娴忚鍣ㄨ嚜鍔ㄥ寲** | `browser` | GUI 搴旂敤 | 閫愰〉鎴浘 + 娣辨祬涓婚 + 绉诲姩绔?|
| **浠ｇ爜楠屾敹** | `code` | CLI/API/搴?| pytest 娴嬭瘯鎶ュ憡 + flake8 lint |
| **瑙嗚楠屾敹** | `visual` | 瑙嗛/璁捐 | 鐢婚潰甯ф暟 + 鍒嗛暅瀹屾暣鎬?|

---

## 蹇€熷紑濮?
```powershell
# 娴忚鍣ㄩ獙鏀?python scripts/run_uat.py browser --project <椤圭洰鐩綍> --url http://localhost:3000

# 浠ｇ爜楠屾敹
python scripts/run_uat.py code --project <椤圭洰鐩綍>

# 瑙嗚楠屾敹
python scripts/run_uat.py visual --project <椤圭洰鐩綍>

# 鍙岃建澶嶇洏锛堟祦绋嬪悎瑙?+ 浜у搧鍙敤璇勫垎锛?python scripts/review.py --project <椤圭洰鐩綍>
```

### 渚濊禆

```bash
pip install playwright
playwright install chromium
```

---

## 琚?Harness 璋冪敤

鍦?Harness 鐨?`project-profile.json` 涓€氳繃 `tools` 瀛楁寮曠敤锛?
```yaml
tools:
  - skill: trae-acceptance
    mode: browser
    args: {url: "http://localhost:3000"}
  - skill: trae-acceptance
    mode: code
```

---

## 涓?Harness 鐨勫叧绯?
| | Harness | Acceptance |
|------|------|------|
| 鑱岃矗 | 娴佺▼鎺у埗锛堣京璁?璐ㄩ噺闂?缂栨帓鍣級 | 缁撴灉楠岃瘉 |
| 浠€涔堟椂鍊欑敤 | 鏁翠釜寮€鍙戞祦绋?| 姣忎釜 Gate 鍚庨獙鏀?|
| 璋佽皟鐢?| 鐢ㄦ埛 | Harness 鎴栫敤鎴?|

---

## 鐩綍缁撴瀯

```
trae-acceptance/
鈹溾攢鈹€ SKILL.md
鈹溾攢鈹€ README.md
鈹溾攢鈹€ scripts/
鈹?  鈹溾攢鈹€ run_uat.py          # 缁熶竴鍏ュ彛
鈹?  鈹溾攢鈹€ browser_uat.py      # Playwright 娴忚鍣ㄨ嚜鍔ㄥ寲
鈹?  鈹溾攢鈹€ code_uat.py         # 浠ｇ爜楠屾敹
鈹?  鈹溾攢鈹€ visual_uat.py       # 瑙嗚楠屾敹
鈹?  鈹斺攢鈹€ review.py           # 鍙岃建澶嶇洏璇勫垎
```

---

## License

MIT
