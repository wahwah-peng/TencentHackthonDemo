## TechSelection
| 模块      | 技术/工具                         | 说明                         |
| ------- | ----------------------------- | -------------------------- |
| 前端框架    | React + React Router          | 单页面应用、路由控制                 |
| UI 库    | AntD + TailwindCSS            | 快速搭建表单、卡片、列表、流式布局          |
| 前端状态    | useState/useContext 或 Zustand | 小项目足够                      |
| 后端框架    | FastAPI                       | REST API + 自动文档 + AI接口     |
| 数据库 ORM | SQLModel                      | Python类映射 SQLite 表，零基础易用   |
| 数据库     | SQLite                        | 零配置，Demo 足够，未来可迁移 Supabase |
| AI 调用   | CLoudStudio内置LLM              | 摘要、标签、决策助手                 |
| 部署环境    | CloudStudio                   | 腾讯提供，一站式运行前后端 + SQLite     |
| 数据录入    | 爬虫                | 避免高风险爬虫，仅爬自己公众号安全可控        |
---
## 技术流动图
```
[用户入口] 登录/注册
  技术：React + React Router + AntD 表单
  ↓
[填写身份表单] 学段/专业
  技术：React 表单 + local state
  ↓
[AI需求采集对话]
  技术：前端输入 → FastAPI 后端 API → AI 调用（OpenAI API）
  输出：用户需求分类
  ↓
[人设卡片生成（最多3个）]
  技术：FastAPI + SQLModel/SQLite 保存
  前端显示：React + AntD Card
  ↓
[用户确认 & 保存]
  技术：SQLite（本地数据库） + FastAPI API
  ↓
[首页信息流入口]
  技术：React 页面 + AntD List/Flow
  ↓
[人设卡片流] ←左右滑动切换人设
  技术：React Carousel/Flow + local state
  ↓
[信息列表流] 今日推送
  技术：API 获取 SQLite 数据 → 前端渲染列表
  ↓
[信息条目点击]
  ↓
[信息详情]
  - 半结构化摘要（AI生成）
      技术：OpenAI API 调用
  - 原文链接
  - 标签展示（AI生成）
  - 收藏操作
      技术：FastAPI + SQLModel 更新 SQLite 数据
  ↓
[收藏到人设库 / 未来计划库]
  技术：SQLite + SQLModel ORM

[数据库模块]
  - 人设库首页 / 单个数据库
      技术：FastAPI + SQLModel/SQLite
  - 信息列表（自然顺序/最近优先）
      技术：SQL 查询排序
  - 搜索框（自然语言检索）
      技术：前端输入 → FastAPI API → AI语义匹配 → 返回列表
  - 未来计划库
      技术：同上，isFuturePlan=true 条件查询

[AI助手模块]
  - 对话页面输入需求 / 冲突问题
      技术：React 输入框 + FastAPI API
  - 输出建议
      技术：AI 调用数据库数据 + 联网搜索 → 返回 JSON → 前端渲染

[手动录入模块]
  - 表单输入链接+标签
      技术：React 表单
  - 系统爬虫生成摘要（可只爬自己公众号）
      技术：Python requests / BeautifulSoup → FastAPI API → SQLite
  - 保存至数据库
      技术：SQLModel ORM 操作 SQLite
```
---

# Workflow**
---
## **Step 0：环境准备（约1h）**

1. 安装 Node.js（前端）
2. 安装 Python（3.11+）
3. 在 CloudStudio 或本地建文件夹：

```
/project
  /frontend
  /backend
  /database
```

4. 初始化前端：

```bash
cd frontend
npx create-react-app myproject
npm install react-router-dom zustand antd tailwindcss
```

5. 初始化后端：

```bash
cd backend
pip install fastapi uvicorn sqlmodel requests beautifulsoup4 openai
```

6. 创建 SQLite 数据库文件：

```bash
touch database/mydatabase.db
```

---

## **Step 1：后端基础搭建（约3h）**

### **1.1 数据库表设计（SQLModel）**

> 核心字段提前规划好，便于前端渲染

* **人设表（Character）**

```python
id: int
name: str
stage: str
major: str
```

* **信息条目表（InfoItem）**

```python
id: int
character_id: int
title: str
link: str
summary: str  # AI生成
tags: str     # 多标签用逗号分隔
isFuturePlan: bool
created_at: datetime
```

* **收藏表（Favorite）**

```python
id: int
info_id: int
user_id: int
target_db: str  # 'person' or 'future'
```

### **1.2 FastAPI接口设计**

| 接口               | 方法   | 参数                                             | 返回字段                   | 说明        |
| ---------------- | ---- | ---------------------------------------------- | ---------------------- | --------- |
| `/add_character` | POST | name, stage, major                             | id, name, stage, major | 增加人设      |
| `/characters`    | GET  | none                                           | list\[Character]       | 获取所有人设    |
| `/add_info`      | POST | character\_id, title, link, tags, isFuturePlan | info\_id               | 手动录入/爬虫数据 |
| `/info_list`     | GET  | character\_id, sort='recent'                   | list\[InfoItem]        | 信息列表      |
| `/favorite`      | POST | info\_id, target\_db                           | success                | 收藏        |
| `/ai_summary`    | POST | text                                           | summary                | AI生成摘要/标签 |

> ✅ 建议：先用 **本地 JSON** 模拟数据，确认接口返回格式再连数据库

### **1.3 运行测试**

```bash
uvicorn main:app --reload
```

* 打开浏览器访问 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* 这是 FastAPI 自动生成的接口文档，能直接测试 POST/GET

---

## **Step 2：前端骨架搭建（约4h）**

### **2.1 页面结构（React Router）**

* `/login` → 登录 / 填写身份表单
* `/home` → 信息流首页（人设卡片+列表）
* `/database/:id` → 单个人设库 / 未来计划库
* `/ai` → AI助手对话页面
* `/manual` → 手动录入

### **2.2 状态管理**

* 小项目：直接用 `useState` / `useContext`
* 保存：

  * 当前选择的人设
  * 收藏列表
  * AI生成摘要/标签临时缓存

### **2.3 Mock 数据**

* 先用本地 JSON 模拟人设、信息条目、收藏

```json
// characters.json
[
  {"id":1, "name":"张三", "stage":"大二", "major":"大数据"}
]
```

### **2.4 UI组件**

* **AntD 卡片**：信息条目、人物卡片
* **列表**：今日信息推送
* **表单**：手动录入
* **Modal / Drawer**：显示 AI 生成摘要

---

## **Step 3：前后端联调（约5h）**

1. 前端 fetch 调用 FastAPI 接口：

```javascript
fetch("/characters").then(res => res.json()).then(setCharacters)
```

2. 信息列表页：

* 点击条目 → 弹出 Modal → 展示 `summary`, `link`, `tags`
* 收藏按钮 → 调接口 `/favorite`

3. AI助手：

* 输入问题 → 调 `/ai_summary` → 显示结果

4. 确认数据流：

```
前端输入 → FastAPI处理 → SQLite存储 → 返回JSON → 前端渲染
```

---

## **Step 4：AI摘要 & 标签生成（约3h）**

1. 对“手动录入表单/爬虫数据”使用 AI 生成摘要
2. 调用接口 `/ai_summary` 返回一行文本或标签数组
3. 前端显示，并允许用户修改（可选）

> ✅ 注意：不做长期记忆 / 跨会话存储

---

## **Step 5：手动补充 + 数据补全（约2h）**

1. 公众号内容抓取：只抓自己开的公众号 → 放入 InfoItem
2. 手动录入表单 → FastAPI保存 → AI补全 → 前端更新列表

---

## **Step 6：Demo打磨 & 部署（约4h）**

1. 确认前端 UI 流畅：按钮可点、Modal正确显示
2. 处理异常：

* 空列表 → 提示“暂无信息”
* 重复收藏 → 返回提示

3. 部署：

* CloudStudio → 上传 frontend + backend
* 运行 `uvicorn main:app --host 0.0.0.0 --port 8080`
* 前端 `npm run build` → 指向 FastAPI 静态文件或 CloudStudio 托管

---

## **Step 7：赛前测试（约1h）**

* 核心流程走一遍：

  1. 登录 → 填身份 → AI生成卡片 → 确认
  2. 首页信息流 → 点击 → 收藏
  3. 数据库查看 → 搜索 → AI助手决策
  4. 手动录入 → AI生成摘要 → 收藏
* 保证 Demo 流程顺滑

---

## **额外小白友好提示**

* **不要一开始就搞爬虫**：用手动录入 + AI补全就够
* **SQLite**：文件直接放，迁移到 Supabase 可赛后考虑
* **SQLModel**：只是让你写 Python 类就能操作数据库，不必写 SQL
* **FastAPI docs**：直接在浏览器调接口，零基础也能看懂返回值

---
