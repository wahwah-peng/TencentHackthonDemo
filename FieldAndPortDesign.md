## 核心数据结构设计
- User&Persona
  - 用途：记录用户身份信息和个性化人设，用于信息流推荐、收藏库分类、AI决策上下文。
  - ```
    User {
    id: string             // 用户唯一ID
    username: string       // 昵称
    email: string
    passwordHash: string   // 安全存储
    createdAt: datetime
    personas: [Persona]    // 每个用户最多3个人设
}

Persona {
    id: string             // 人设ID
    userId: string         // 所属用户ID
    name: string           // 人设名称（可自定义）
    grade: string          // 学段
    major: string          // 专业方向
    interests: [string]    // 兴趣标签
    goals: [string]        // AI采集的目标描述
    description: string    // AI生成的人设简短描述
    createdAt: datetime
    updatedAt: datetime
    entries: [Entry]       // 收藏信息条目列表
}
  ```
- Entry
  - 用途：存储公告、比赛、科研活动信息，用于首页信息流、详情页展示、收藏库、AI搜索/决策。
  - ```
Entry {
    id: string               // 唯一ID
    title: string            // 公告标题
    summary: string          // AI生成的一句话摘要
    content: string          // 可选：完整文本
    source: string           // 来源（公众号/校园公告）
    url: string              // 原文链接
    type: string             // 分类：竞赛/科研/讲座/奖学金/活动
    tags: [string]           // AI或用户生成的标签
    time: datetime           // 活动或公告时间
    createdAt: datetime      // 数据创建时间
    updatedAt: datetime
    isFuturePlan: boolean    // 是否未来计划库
    personaId: string        // 所属人设ID（收藏到哪个库）
    embedding?: [float]      // AI向量化表示，用于语义检索
}
    ```
- AIInteraction
  - 用途：决策辅助、记录用户输入目标、AI输出建议，不直接存储搜索历史。
  - ```
AIInteraction {
    id: string
    userId: string
    personaId: string
    input: string           // 用户输入的需求/冲突问题
    output: string          // AI生成的建议/方案
    contextEntries: [string] // 参考条目ID列表（用于生成回答）
    createdAt: datetime
}
```
- ManualEntry
  - 可以复用 Entry 结构，但区分来源：
  - ```
    ManualEntry extends Entry {
    createdBy: string       // 用户ID
    createdAt: datetime
}
```
---
## 前后端API端口设计
- 用户与人设
  - | 方法     | 路径                 | 输入                                  | 输出                  | 功能            |
| ------ | ------------------ | ----------------------------------- | ------------------- | ------------- |
| POST   | /api/users/        | {username,email,password}           | {id,username,email} | 用户注册          |
| POST   | /api/users/login   | {email,password}                    | {token,user}        | 用户登录          |
| GET    | /api/personas/     | token                               | \[{Persona}]        | 获取用户人设列表      |
| POST   | /api/personas/     | token,{grade,major,interests,goals} | Persona             | 创建人设并触发AI生成描述 |
| PUT    | /api/personas/{id} | token,{name,interests,goals}        | Persona             | 编辑人设          |
| DELETE | /api/personas/{id} | token                               | success             | 删除人设          |
- 信息流 & 公告条目
  - | 方法   | 路径                   | 输入                                       | 输出       | 功能                  |
| ---- | -------------------- | ---------------------------------------- | -------- | ------------------- |
| GET  | /api/entries/today   | token, personaId, filters?               | \[Entry] | 获取今日推送信息流           |
| GET  | /api/entries/{id}    | token                                    | Entry    | 获取详情页（半结构化摘要+原文+标签） |
| POST | /api/entries/collect | token, entryId, personaId, isFuturePlan  | success  | 收藏信息条目到指定人设库/未来计划库  |
| POST | /api/entries/manual  | token, personaId, title, url, type, tags | Entry    | 手动录入条目              |
- 数据库搜索 / AI检索
| 方法   | 路径               | 输入                      | 输出                                        | 功能            |
| ---- | ---------------- | ----------------------- | ----------------------------------------- | ------------- |
| POST | /api/search      | token, personaId, query | \[Entry]                                  | 基于AI语义检索已收藏条目 |
| POST | /api/ai/decision | token, personaId, input | {output\:string, contextEntries:\[Entry]} | AI 决策建议       |
- 辅助与系统管理
| 方法     | 路径                        | 输入    | 输出        | 功能                   |
| ------ | ------------------------- | ----- | --------- | -------------------- |
| GET    | /api/tags                 | token | \[string] | 获取可用标签列表（AI生成或用户自定义） |
| GET    | /api/sources              | token | \[string] | 获取信息来源列表             |
| GET    | /api/persona/{id}/entries | token | \[Entry]  | 获取某个人设库所有条目          |
| DELETE | /api/entries/{id}         | token | success   | 删除收藏条目               |
---
## 数据流设计 & 注意点
- 首页信息流
  - 输入：personaId、时间/类型筛选
  - 后端：从模拟数据库或公众号接口抓取条目 → AI生成摘要/标签 → 输出JSON给前端卡片流
- 收藏到数据库
  - 前端点击收藏 → POST /api/entries/collect
  - 后端检查重复（title+url） → 写入指定人设库
- AI搜索 / 决策
  - 前端输入自然语言 → POST /api/search 或 /api/ai/decision
  - 后端加载 persona 库条目 embedding，做语义匹配/向量检索 → 生成结果 → 返回前端
- 手动录入
  - 前端表单提交 → 后端生成摘要 → 写入指定人设库/未来计划库
- 安全
  - token认证（JWT）
  - API 限制只访问本人数据
  - 只读模拟数据，合法安全
---
非常关键 👍，不然后续 API、模型、数据库对不上号会很乱。下面我帮你梳理一个 **统一字段命名规范对照表**（三层：**API 参数 → Pydantic/SQLModel 模型属性 → 数据库列名**）。

---

## 🌐 字段命名统一规范

* **命名风格**：

  * API 参数：`camelCase`（前端 JSON 常用）
  * Python 模型：`snake_case`（符合 Python 习惯）
  * 数据库列：`snake_case`（SQL 标准）

---

## 📑 对照表示例（以 `AIInteraction` 为核心）

| 含义/业务字段     | API 参数 (camelCase) | Python 模型属性 (snake\_case) | 数据库列名 (snake\_case) | 备注                      |
| ----------- | ------------------ | ------------------------- | ------------------- | ----------------------- |
| 交互ID        | `interactionId`    | `interaction_id`          | `interaction_id`    | 主键 UUID/自增ID            |
| 用户输入内容      | `content`          | `content`                 | `content`           | 原始文本                    |
| 摘要          | `summary`          | `summary`                 | `summary`           | AI提取结果                  |
| 标签列表        | `tags`             | `tags`                    | `tags`              | 可存储为 JSON/数组            |
| 向量Embedding | `embedding`        | `embedding`               | `embedding`         | 一般存储为 `VECTOR` 类型或 JSON |
| 创建时间        | `createdAt`        | `created_at`              | `created_at`        | 默认 `NOW()`              |
| 更新时间        | `updatedAt`        | `updated_at`              | `updated_at`        | 可选，方便追踪                 |

---

## 📌 规范总结

1. **前端/接口层（API 参数）**

   * `camelCase`，符合前端 JSON/JS 常见风格
   * 例：`interactionId`, `createdAt`

2. **Python 代码层（模型属性）**

   * `snake_case`，符合 Python 代码规范
   * 使用 **Pydantic/SQLModel** 的 `Field(..., alias="xxx")` 来保证 API/DB 对齐

3. **数据库层（列名）**

   * `snake_case`，与 Python 模型保持一致
   * 数据库永远用小写下划线，避免大小写问题

---


* **前端传 JSON** → `{"interactionId": "...", "content": "...", "createdAt": "..."}`
* **后端模型属性** → `interaction_id`, `content`, `created_at`
* **数据库列名** → `interaction_id`, `content`, `created_at`

三层完全对齐。

---

要不要我帮你直接输出一个完整的 **`models.py`（带 alias 映射 + 数据库定义）**，这样你可以直接拿去用？



