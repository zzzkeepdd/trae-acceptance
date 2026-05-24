# Trae Acceptance

> Harness 验收引擎 — 独立的项目验收 skill。

不负责流程控制，只负责**验证结果**。

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](./SKILL.md)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

---

## 三种验收模式

| 模式 | 命令 | 适用项目 | 产出 |
|------|------|------|------|
| **浏览器自动化** | `browser` | GUI 应用 | 逐页截图 + 深浅主题 + 移动端 |
| **代码验收** | `code` | CLI/API/库 | pytest 测试报告 + flake8 lint |
| **视觉验收** | `visual` | 视频/设计 | 画面帧数 + 分镜完整性 |

---

## 快速开始

```powershell
# 浏览器验收
python scripts/run_uat.py browser --project <项目目录> --url http://localhost:3000

# 代码验收
python scripts/run_uat.py code --project <项目目录>

# 视觉验收
python scripts/run_uat.py visual --project <项目目录>

# 双轨复盘（流程合规 + 产品可用评分）
python scripts/review.py --project <项目目录>
```

### 依赖

```bash
pip install playwright
playwright install chromium
```

---

## 被 Harness 调用

在 Harness 的 `project-profile.json` 中通过 `tools` 字段引用：

```yaml
tools:
  - skill: trae-acceptance
    mode: browser
    args: {url: "http://localhost:3000"}
  - skill: trae-acceptance
    mode: code
```

---

## 与 Harness 的关系

| | Harness | Acceptance |
|------|------|------|
| 职责 | 流程控制（辩论+质量门+编排器） | 结果验证 |
| 什么时候用 | 整个开发流程 | 每个 Gate 后验收 |
| 谁调用 | 用户 | Harness 或用户 |

---

## 目录结构

```
trae-acceptance/
├── SKILL.md
├── README.md
├── scripts/
│   ├── run_uat.py          # 统一入口
│   ├── browser_uat.py      # Playwright 浏览器自动化
│   ├── code_uat.py         # 代码验收
│   ├── visual_uat.py       # 视觉验收
│   └── review.py           # 双轨复盘评分
```

---

## License

MIT
