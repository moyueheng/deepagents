# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

DeepAgents 是一个基于 LangGraph 构建的通用"深度代理"Python包。它实现了四个关键组件：
- **规划工具** (Planning Tool)
- **子代理** (Sub Agents)
- **虚拟文件系统** (Mock File System)
- **详细提示** (Detailed Prompt)

## 常用命令

### 开发环境设置
```bash
# 安装开发依赖
pip install -e ".[dev]"

# 安装特定示例的依赖
cd examples/research
pip install -r requirements.txt
```

### 测试
```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_deepagents.py

# 带覆盖率报告运行测试
pytest --cov=deepagents
```

### 构建
```bash
# 构建包
python -m build

# 检查包
twine check dist/*
```

## 代码架构

### 核心组件

1. **Agent 创建** (`src/deepagents/graph.py`)
   - `create_deep_agent()`: 创建同步深度代理
   - `async_create_deep_agent()`: 创建异步深度代理
   - `agent_builder()`: 内部构建函数

2. **中间件系统** (`src/deepagents/middleware.py`)
   - `PlanningMiddleware`: 提供待办事项管理
   - `FilesystemMiddleware`: 提供虚拟文件系统
   - `SubAgentMiddleware`: 提供子代理调用能力

3. **状态管理** (`src/deepagents/state.py`)
   - `DeepAgentState`: 主要状态结构
   - `PlanningState`: 待办事项状态
   - `FilesystemState`: 文件系统状态

4. **内置工具** (`src/deepagents/tools.py`)
   - `write_todos`: 管理待办事项列表
   - `ls`: 列出虚拟文件
   - `read_file`: 读取文件内容
   - `write_file`: 写入文件
   - `edit_file`: 编辑文件

### 关键设计模式

1. **中间件架构**: 使用 LangChain 的 AgentMiddleware 系统，每个功能模块都是独立的中间件
2. **虚拟文件系统**: 使用 LangGraph State 对象模拟文件系统，不操作真实文件
3. **子代理系统**: 支持创建专门用途的子代理，实现"context quarantine"
4. **工具配置**: 支持人为干预(HITL)配置，可设置工具执行前需要人工批准

## 开发指南

### 添加新的中间件
1. 继承 `AgentMiddleware` 类
2. 定义 `state_schema` 和 `tools`
3. 实现 `modify_model_request` 方法（可选）
4. 在 `create_deep_agent` 的 `middleware` 参数中添加

### 创建子代理
子代理有两种类型：
- `SubAgent`: 使用提示和工具定义的标准子代理
- `CustomSubAgent`: 使用预构建 LangGraph 图的自定义子代理

### 工具开发
所有工具都应该：
- 使用 LangChain 的 `@tool` 装饰器
- 正确处理 `InjectedState` 和 `InjectedToolCallId`
- 返回 `Command` 对象进行状态更新
- 提供清晰的错误信息

### 测试策略
- 单元测试位于 `tests/` 目录
- 使用 pytest 框架
- 测试覆盖核心功能和边界情况
- 集成测试验证中间件之间的交互

## 配置文件

- `pyproject.toml`: 项目配置和依赖管理
- 开发依赖包括 pytest、pytest-cov、build、twine
- 支持 Python 3.11+

## 示例代码

参考 `examples/research/research_agent.py` 了解完整的使用示例，包括：
- 如何配置工具
- 如何设置子代理
- 如何使用文件系统
- 如何处理待办事项