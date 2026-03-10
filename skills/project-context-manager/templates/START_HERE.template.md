# 开始这里 - VideoCut 项目快速入门

> **5 分钟快速了解项目，立即开始工作**

## 🎯 项目是什么？

**VideoCut** - 一个跨平台的专业视频剪辑工具，采用经典 Macintosh 复古界面风格。

**核心特点**：
- 🎨 复古 Mac 黑白界面（像素字体、单像素边框）
- 🎬 专业剪辑功能（多轨道、时间线、转场）
- 🔌 插件化架构（C++ 和 Python 插件）
- 🤖 AI 功能扩展（语音识别、自动字幕）
- 🌐 REST API 接口

---

## 🛠️ 技术栈（5 秒速览）

| 组件 | 技术 |
|------|------|
| UI | Dear ImGui + 复古主题 |
| 窗口 | GLFW |
| 语言 | C++17/20 |
| 视频 | FFmpeg |
| 渲染 | OpenGL 4.5+ |
| 音频 | PortAudio |
| 插件 | Python 3.10+ |
| 构建 | CMake |

---

## 📍 当前状态

**阶段**: Phase 1 - 核心框架搭建
**版本**: v0.1.0-alpha
**进度**: 刚开始（0%）

**当前目标**: 创建一个能显示复古 Mac 风格界面的最小原型

---

## 🎯 你需要做什么？

### 立即查看

👉 **打开 [PROJECT_STATUS.md](./PROJECT_STATUS.md)** 查看：
- ✅ 已完成什么
- 🚧 正在做什么
- 📝 下一步做什么

### 开始工作

1. **如果有"进行中任务"** → 继续完成它
2. **如果没有** → 从"待办任务"中选择优先级最高的

### 会话结束时

👉 **更新 [PROJECT_STATUS.md](./PROJECT_STATUS.md)**
- 记录完成的工作
- 更新进度
- 给下一个会话留言

---

## 🚨 重要规则

### 1. UI 代码使用 ImGui Skill

所有界面相关代码必须使用 **ImGui skill** 实现，不要手写 ImGui 代码。

**主题要求**：
- 黑白配色（白底黑字）
- 无圆角（完全方形）
- 单像素黑色边框
- 像素字体（Chicago 或 Geneva）

### 2. 遵循文档

- **架构设计** → 参考 `技术方案书.md`
- **实施步骤** → 参考 `开发指南.md`
- **当前状态** → 参考 `PROJECT_STATUS.md`（最重要）

### 3. 小步迭代

- 不要一次做太多
- 每完成一个小模块就测试
- 频繁更新文档

### 4. 记录问题

遇到问题立即记录到：
- `PROJECT_STATUS.md` 的"已知问题"表格
- `CONTEXT.md` 的"调试信息"章节

---

## 📂 项目结构

```
videocut/
├── docs/agent/              ← 你现在在这里
│   ├── README.md            ← Agent 文档中心
│   ├── START_HERE.md        ← 本文件
│   ├── PROJECT_STATUS.md    ← 项目状态（最重要）
│   ├── SESSION_HANDOFF.md   ← 会话交接流程
│   ├── CONTEXT.md           ← 详细上下文
│   ├── 技术方案书.md        ← 架构设计
│   └── 开发指南.md          ← 实施步骤
├── src/                     ← 源代码（待创建）
├── external/                ← 第三方库（待创建）
├── resources/               ← 资源文件（待创建）
└── README.md                ← 用户文档
```

---

## 🎓 开发规范速查

### 代码风格
- 类名: `PascalCase`
- 函数: `camelCase`
- 变量: `snake_case`
- 使用智能指针

### 提交规范
```
[模块] 简短描述

详细说明
```

### 测试要求
- 每个模块完成后立即测试
- 确保跨平台编译通过

---

## 🔗 快速链接

- **当前状态** → [PROJECT_STATUS.md](./PROJECT_STATUS.md) ⭐⭐⭐
- **会话流程** → [SESSION_HANDOFF.md](./SESSION_HANDOFF.md)
- **架构设计** → [技术方案书.md](./技术方案书.md)
- **实施步骤** → [开发指南.md](./开发指南.md)
- **详细上下文** → [CONTEXT.md](./CONTEXT.md)

---

## ✅ 下一步

1. ✅ 你已经读完这个文件
2. 👉 **现在打开 [PROJECT_STATUS.md](./PROJECT_STATUS.md)**
3. 🚀 开始工作！

---

**记住**：
- 📖 每次会话必读 `PROJECT_STATUS.md`
- ✏️ 每次会话结束必更新 `PROJECT_STATUS.md`
- 🎨 所有 UI 代码使用 ImGui skill

**祝你工作顺利！** 🚀

---

**最后更新**: 2026-03-10
