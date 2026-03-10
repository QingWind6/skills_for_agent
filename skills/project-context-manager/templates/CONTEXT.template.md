# VideoCut 开发上下文

> **用途**：记录详细的开发上下文、设计思路、代码片段、调试信息等，供跨会话使用。

## 📅 最后更新

**日期**: 2026-03-10
**更新者**: 初始化
**会话 ID**: N/A

---

## 🧠 当前开发上下文

### 正在开发的功能

**功能名称**: 无

**相关文件**:
- 无

**设计思路**:
- 暂无

**实现细节**:
- 暂无

**待解决问题**:
- 暂无

**参考资料**:
- 暂无

---

## 🔍 重要代码片段

### 代码片段 #001: [标题]

**文件**: `路径/文件名`

**用途**: 描述这段代码的作用

**代码**:
```cpp
// 代码示例
```

**注意事项**:
- 注意事项 1
- 注意事项 2

---

## 🐞 调试信息

### 调试记录 #001: [问题描述]

**日期**: YYYY-MM-DD

**问题**:
- 详细描述问题

**尝试的解决方案**:
1. 方案 1 - 结果
2. 方案 2 - 结果

**最终解决方案**:
- 描述最终如何解决的

**经验教训**:
- 学到了什么

---

## 📚 技术研究笔记

### 研究 #001: FFmpeg 解码流程

**日期**: 待补充

**研究目标**:
- 理解 FFmpeg 的解码流程
- 实现高效的帧提取

**关键发现**:
- 待补充

**参考资料**:
- [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)
- [dranger FFmpeg 教程](http://dranger.com/ffmpeg/)

**代码示例**:
```cpp
// 待补充
```

---

### 研究 #002: ImGui 自定义渲染

**日期**: 待补充

**研究目标**:
- 实现复古 Mac 风格的自定义组件
- 理解 ImGui 的 DrawList API

**关键发现**:
- 待补充

**参考资料**:
- [ImGui GitHub](https://github.com/ocornut/imgui)
- [ImGui Demo](https://github.com/ocornut/imgui/blob/master/imgui_demo.cpp)

---

## 🏗️ 架构演进记录

### 变更 #001: [架构变更标题]

**日期**: YYYY-MM-DD

**变更原因**:
- 为什么需要这个变更

**变更内容**:
- 具体改了什么

**影响范围**:
- 哪些模块受到影响

**迁移步骤**:
1. 步骤 1
2. 步骤 2

---

## 💾 数据结构设计

### Timeline 数据结构

**当前版本**: v0.1

**设计思路**:
```cpp
// 参考《开发指南.md》第 3.1 节
class Timeline {
    std::vector<Track> tracks;
    double duration;
    double currentTime;
    int frameRate;
};
```

**待优化点**:
- 暂无

---

### Clip 数据结构

**当前版本**: v0.1

**设计思路**:
```cpp
class Clip {
    MediaAsset* source;
    double startTime;
    double duration;
    double inPoint;
    double outPoint;
    std::vector<Effect*> effects;
};
```

**待优化点**:
- 暂无

---

## 🔗 依赖关系图

### 模块依赖

```
UI Layer (ImGui)
    ↓
Application Layer
    ↓
Core Engine (Timeline, Clip, Track)
    ↓
Video/Audio Processing (FFmpeg, PortAudio)
    ↓
Render Engine (OpenGL)
```

### 文件依赖

```
main.cpp
  ├─> ui/application.h
  │     ├─> ui/theme.h
  │     └─> ui/widgets/*.h
  ├─> core/timeline.h
  │     ├─> core/track.h
  │     └─> core/clip.h
  └─> video/decoder.h
        └─> FFmpeg headers
```

---

## 🎯 性能优化记录

### 优化 #001: [优化标题]

**日期**: YYYY-MM-DD

**优化前性能**:
- 指标 1: 数值
- 指标 2: 数值

**优化方案**:
- 描述优化方案

**优化后性能**:
- 指标 1: 数值
- 指标 2: 数值

**代码变更**:
```cpp
// 优化后的代码
```

---

## 🧪 测试用例

### 测试 #001: 视频解码测试

**测试目标**:
- 验证 FFmpeg 解码器能正确解码常见格式

**测试文件**:
- test_video_1080p.mp4
- test_video_4k.mp4
- test_video_h265.mkv

**测试步骤**:
1. 打开视频文件
2. 读取前 100 帧
3. 验证帧数据正确性

**预期结果**:
- 所有格式都能正确解码
- 无内存泄漏

**实际结果**:
- 待测试

---

## 📦 第三方库集成笔记

### FFmpeg 集成

**版本**: 6.0+

**安装方式**:
- Ubuntu: `apt install libavcodec-dev libavformat-dev libavutil-dev libswscale-dev`
- macOS: `brew install ffmpeg`
- Windows: vcpkg 或手动编译

**CMake 配置**:
```cmake
pkg_check_modules(FFMPEG REQUIRED
    libavcodec
    libavformat
    libavutil
    libswscale
)
```

**常见问题**:
- 问题 1: 待补充
- 解决方案: 待补充

---

### ImGui 集成

**版本**: 1.90+

**集成方式**: Git submodule

**配置**:
```bash
git submodule add https://github.com/ocornut/imgui.git external/imgui
```

**后端选择**:
- GLFW + OpenGL3

**常见问题**:
- 问题 1: 待补充
- 解决方案: 待补充

---

## 🎨 UI 设计资源

### 复古 Mac 配色

**主色调**:
- 背景: `#FFFFFF` (白色)
- 前景: `#000000` (黑色)
- 灰度 1: `#E5E5E5` (浅灰)
- 灰度 2: `#CCCCCC` (中灰)
- 灰度 3: `#808080` (深灰)

### 字体资源

**主字体**: Chicago
- 文件: `resources/fonts/ChicagoFLF.ttf`
- 大小: 12px
- 来源: https://github.com/ChicagoFLF/ChicagoFLF

**备选字体**: Geneva, Monaco

### 图标设计

**风格**: Susan Kare 像素风格
- 尺寸: 16x16, 32x32
- 格式: PNG (透明背景)
- 色彩: 黑白

**图标列表**:
- play.png - 播放按钮
- pause.png - 暂停按钮
- cut.png - 剪切工具
- 待补充...

---

## 🔐 安全注意事项

### 文件操作

- 所有文件路径需要验证（防止路径遍历）
- 大文件使用流式处理（避免内存溢出）
- 临时文件使用安全的临时目录

### 插件系统

- 插件需要签名验证（未来实现）
- 插件运行在沙箱中（进程隔离）
- 限制插件的文件系统访问权限

---

## 📝 会议记录

### 会议 #001: 项目启动

**日期**: 2026-03-10

**参与者**: jojang, Claude Agent

**讨论内容**:
- 确定使用 ImGui 实现复古 Mac 风格
- 技术栈选型
- 开发路线图规划

**决策**:
- UI 框架: Dear ImGui
- 视频处理: FFmpeg
- 构建系统: CMake

**行动项**:
- [x] 编写技术方案书
- [x] 编写开发指南
- [ ] 开始 Phase 1 开发

---

## 🔮 未来计划

### 短期目标（1-3 个月）

- [ ] 完成 Phase 1: 核心框架
- [ ] 完成 Phase 2: 基础剪辑功能
- [ ] 发布 v0.1.0-alpha 版本

### 中期目标（3-6 个月）

- [ ] 完成 Phase 3: 插件系统
- [ ] 完成 Phase 4: 高级功能
- [ ] 发布 v0.2.0-beta 版本

### 长期目标（6-12 个月）

- [ ] 完成 Phase 5: AI 功能插件
- [ ] 完成 Phase 6: API 与集成
- [ ] 发布 v1.0.0 正式版

---

## 📖 学习资源

### 推荐阅读

1. **视频处理**:
   - [FFmpeg 官方文档](https://ffmpeg.org/documentation.html)
   - [Video Encoding Guide](https://trac.ffmpeg.org/wiki/Encode/H.264)

2. **图形编程**:
   - [Learn OpenGL](https://learnopengl.com/)
   - [OpenGL Tutorial](http://www.opengl-tutorial.org/)

3. **UI 设计**:
   - [Macintosh Human Interface Guidelines (1987)](https://archive.org/details/apple-macintosh-human-interface-guidelines)
   - [Susan Kare 图标设计](https://kare.com/)

4. **C++ 最佳实践**:
   - [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/)
   - [Effective Modern C++](https://www.oreilly.com/library/view/effective-modern-c/9781491908419/)

---

## 💬 常见问题 FAQ

### Q1: 如何继续上一个会话的工作？

A:
1. 阅读 `PROJECT_STATUS.md` 了解当前状态
2. 阅读本文件 (`CONTEXT.md`) 了解详细上下文
3. 检查"进行中任务"部分
4. 继续开发或开始新任务

### Q2: 如何记录新的上下文信息？

A:
1. 在相应章节添加新条目
2. 使用清晰的标题和编号
3. 包含日期和相关文件路径
4. 会话结束前保存

### Q3: 遇到问题怎么办？

A:
1. 先查看"调试信息"章节是否有类似问题
2. 查看"常见问题"章节
3. 记录新问题到"调试信息"
4. 在 `PROJECT_STATUS.md` 的"已知问题"表格中记录

---

**文档维护说明**:
- 每次会话结束前更新相关章节
- 保持信息的时效性和准确性
- 删除过时或无用的信息
- 使用清晰的标题和编号系统
