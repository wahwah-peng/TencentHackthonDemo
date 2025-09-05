# Wireframe

## 1. 首页 Wireframe（信息流入口 + 人设卡片承载的今日推送）

- **顶部导航栏**
  - Logo（左上）
  - AI助手入口按钮（右上）
  - 个人中心图标（右上）

- **核心功能区**
  - 人设卡片流（左右滑动切换人设）
    - 每张卡片承载：
      - 今日信息列表条目（标题 + 标签 + 时间 + 简短摘要）
      - 点击条目 → 信息详情页
      - 收藏按钮（选择存入人设库/未来计划库）

- **底部信息**
  - 历史记录入口（可选）
  - 版权信息（可选）

---

## 2. AI生成页 Wireframe（人设管理 & 决策助手交互）

- **顶部**
  - 返回按钮（←）
  - 页面标题（如“AI生成”/“人设生成”/“决策助手”）

- **操作区**
  - 输入框：用户输入总需求 / 冲突问题
  - 参数选择（可选单选/下拉）：
    - 人设生成类型（如“学习目标/竞赛/活动”）
    - AI处理模式（如“摘要/推荐/决策”）
  - 生成按钮（突出显示）

- **结果区**
  - 空白框（标注“生成结果将显示在此”）
  - 操作按钮：
    - 保存 → 存入人设库/未来计划库
    - 重新生成

---

## 3. 信息详情页 Wireframe（列表条目展开）

- **顶部**
  - 返回按钮（←）
  - 页面标题（如“信息详情”）

- **内容区**
  - 半结构化摘要（AI生成）
  - 原文链接
  - 标签展示（活动类型/来源）
  - 收藏按钮（选择存入人设库/未来计划库）

---

## 4. 数据库页 Wireframe（人设库 & 未来计划库）

- **顶部**
  - 返回按钮（←）
  - 页面标题（如“人设库”）

- **功能区**
  - 人设列表（每个人设可进入对应数据库）
  - 单个人设数据库：
    - 信息列表（时间排序：最近/自然时间）
    - 每条条目 → 点击查看详情
    - 搜索框（自然语言检索，AI语义匹配结果列表）

- **未来计划库**
  - 仅显示标记 isFuturePlan=true 条目
  - 列表条目同上

---

## 5. 我的页 Wireframe（手动录入 & 人设管理）

- **顶部**
  - 返回按钮（←）
  - 页面标题（“个人中心”）

- **功能卡片**
  1. 人设管理
     - 查看 / 编辑 / 删除已保存人设
     - 重新发起 AI 交互 → 更新人设
  2. 手动录入
     - 表单：
       - 链接输入框
       - 活动分类标签选择
     - 生成摘要按钮（系统爬虫 + AI）
     - 保存到指定数据库（人设库 / 未来计划库）
  3. （可选）基础设置：
     - 修改密码
     - 退出登录

---

## 注解 & 使用说明
< 首页信息流的「人设卡片 + 列表条目」逻辑拆开标注
	AI生成页、信息详情页、数据库页、我的页的核心操作区域、输入区、按钮区都明确化
	控制元素数量 ≤8，便于 Figma 直接拉节点和交互线
1. 所有页面核心元素均控制在 5-8 个以内；
2. 元素仅用矩形 + 文本标注表示，可在 Figma 直接绘制为节点；
3. 页面跳转遵循用户动线：
   - 初次使用 → 人设生成 → 首页信息流
   - 首页浏览 → 信息详情 → 收藏
   - 数据库 → 搜索 → 信息详情
   - AI助手 → 输入需求 → 生成决策
   - 我的 → 手动录入 → 保存
4. 所有操作按钮需标注用途（生成/保存/收藏/重新生成/查看）；
5. 非核心功能（帮助中心、详细设置、偏好设置）全部省略。
---
# Figma 节点命名表格（AIcoding 产品）

## 1. 首页 Page: Home

- Home/TopNav/Logo
- Home/TopNav/AIButton
- Home/TopNav/ProfileIcon
- Home/Core/HumanProfileCardFlow
  - Home/Core/HumanProfileCardFlow/Card_1
    - Home/Core/HumanProfileCardFlow/Card_1/InfoList
      - Home/Core/HumanProfileCardFlow/Card_1/InfoList/Item_1
        - Home/Core/HumanProfileCardFlow/Card_1/InfoList/Item_1/Title
        - Home/Core/HumanProfileCardFlow/Card_1/InfoList/Item_1/Tags
        - Home/Core/HumanProfileCardFlow/Card_1/InfoList/Item_1/Time
        - Home/Core/HumanProfileCardFlow/Card_1/InfoList/Item_1/Summary
        - Home/Core/HumanProfileCardFlow/Card_1/InfoList/Item_1/ViewButton
        - Home/Core/HumanProfileCardFlow/Card_1/InfoList/Item_1/CollectButton
- Home/Bottom/HistoryEntry
- Home/Bottom/Copyright

---

## 2. AI生成页 Page: AIGenerate

- AIGenerate/TopNav/BackButton
- AIGenerate/TopNav/Title
- AIGenerate/Operation/InputBox
- AIGenerate/Operation/ParamSelect
- AIGenerate/Operation/GenerateButton
- AIGenerate/Result/ResultBox
- AIGenerate/Result/SaveButton
- AIGenerate/Result/RegenerateButton

---

## 3. 信息详情页 Page: InfoDetail

- InfoDetail/TopNav/BackButton
- InfoDetail/TopNav/Title
- InfoDetail/Content/Summary
- InfoDetail/Content/OriginalLink
- InfoDetail/Content/Tags
- InfoDetail/Content/CollectButton

---

## 4. 数据库页 Page: Database

- Database/TopNav/BackButton
- Database/TopNav/Title
- Database/Core/HumanProfileList
  - Database/Core/HumanProfileList/Profile_1
    - Database/Core/HumanProfileList/Profile_1/InfoList
      - Database/Core/HumanProfileList/Profile_1/InfoList/Item_1
        - Database/Core/HumanProfileList/Profile_1/InfoList/Item_1/Title
        - Database/Core/HumanProfileList/Profile_1/InfoList/Item_1/Tags
        - Database/Core/HumanProfileList/Profile_1/InfoList/Item_1/Time
        - Database/Core/HumanProfileList/Profile_1/InfoList/Item_1/ViewButton
- Database/Core/FuturePlanList
  - Database/Core/FuturePlanList/Item_1
    - Database/Core/FuturePlanList/Item_1/Title
    - Database/Core/FuturePlanList/Item_1/Tags
    - Database/Core/FuturePlanList/Item_1/Time
    - Database/Core/FuturePlanList/Item_1/ViewButton
- Database/Core/SearchBox

---

## 5. 我的页 Page: Profile

- Profile/TopNav/BackButton
- Profile/TopNav/Title
- Profile/Core/HumanProfileManagement
  - Profile/Core/HumanProfileManagement/ViewEditDelete
  - Profile/Core/HumanProfileManagement/ReGenerateAI
- Profile/Core/ManualEntry
  - Profile/Core/ManualEntry/LinkInput
  - Profile/Core/ManualEntry/CategorySelect
  - Profile/Core/ManualEntry/GenerateSummaryButton
  - Profile/Core/ManualEntry/SaveButton
- Profile/Core/Settings (可选)
  - Profile/Core/Settings/ChangePassword
  - Profile/Core/Settings/Logout
