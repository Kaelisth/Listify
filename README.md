# 清单 · Listify

> 一款极简待办清单 —— 像纸质笔记本一样安静，像数字工具一样高效。

---

## 文件说明

| 文件 | 说明 |
|------|------|
| `todo-app.html` | **主程序**：浏览器运行的完整 Web 应用（推荐） |
| `index.html` | 宣传首页 / Landing Page |
| `todo_app.py` | Python 桌面版源代码（需要 Python 3.8+） |
| `README.md` | 本文件 |
| `intro.txt` | 纯文字简介 |

---

## 快速开始

### 方式一：直接用浏览器打开（推荐）

```bash
# 双击 todo-app.html 即可，无需安装任何东西
open todo-app.html       # macOS
start todo-app.html      # Windows
xdg-open todo-app.html   # Linux
```

### 方式二：运行 Python 桌面版

```bash
# 确保已安装 Python 3.8+
python todo_app.py
```

### 方式三：打包为 exe / app

```bash
# 安装 PyInstaller
pip install pyinstaller

# Windows → 生成 .exe
pyinstaller --onefile --windowed --name "Listify" todo_app.py

# macOS → 生成 .app
pyinstaller --onefile --windowed --name "Listify" todo_app.py

# 打包结果在 dist/ 目录
```

---

## 功能特性

- **任务管理**：添加 / 删除 / 标记完成 / 编辑任务
- **优先级**：普通 / 重要（橙色）/ 紧急（红色）三级
- **筛选**：全部 / 待完成 / 已完成
- **进度追踪**：顶部进度条 + 统计数字
- **深浅色模式**：一键切换，偏好自动保存
- **多语言**：简体中文 / English / 日本語 / Français / Español / 한국어
- **数据持久化**：浏览器版自动保存到 localStorage；桌面版保存到 `~/.listify_data.json`
- **导入 / 导出**：JSON 格式，数据完全由你掌控
- **无需注册**：无账号、无追踪、无广告

---

## 技术栈

### Web 版（todo-app.html）
- 纯 HTML5 + CSS3 + Vanilla JavaScript
- 零依赖，单文件，可完全离线运行
- Google Fonts：Cormorant Garamond + DM Mono

### 桌面版（todo_app.py）
- Python 3.8+ 标准库 Tkinter
- 无第三方依赖
- 跨平台：Windows / macOS / Linux

---

## 数据格式

导出文件为标准 JSON，结构如下：

```json
{
  "version": "1.0",
  "exportedAt": "2025-01-01T12:00:00.000Z",
  "tasks": [
    {
      "id": "1700000000000",
      "text": "买咖啡豆",
      "done": false,
      "priority": "normal",
      "created_at": "2025-01-01"
    }
  ]
}
```

---

## 截图预览

```
┌─────────────────────────────────────────┐
│  清单·list            🇨🇳 中文  🌙      │
│  你的日子，从这里开始整理               │
│                                         │
│  [ 5 全部 ]  [ 3 待完成 ]  [ 2 已完成 ] │
│  ████████░░░░░░░░░░░░ 40%              │
│                                         │
│  [ 添加一件事...               ] [添加] │
│  优先级: [普通] [重要] [紧急]           │
│                                         │
│  [全部] [待完成] [已完成]               │
│                                         │
│  ▌ □ 向设计师确认方案细节  [紧急]  ✕   │
│  ▌ □ 准备产品评审          [重要]  ✕   │
│    □ 整理桌面文件夹                 ✕   │
│    ✓ 给妈妈打电话                   ✕   │
│                                         │
│  [导出文件] [导入文件] [清除已完成]     │
└─────────────────────────────────────────┘
```

---

## 键盘快捷键

| 按键 | 操作 |
|------|------|
| `Enter` | 添加任务（在输入框中） |
| `Esc` | 取消编辑任务 |

---

## 许可证

MIT License — 自由使用、修改、分发。

---

*清单 · Listify — 把每一天整理得有序。*
