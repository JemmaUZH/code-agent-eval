# 🤖 Code Agent Eval

一个基于 Streamlit 的可视化自动代码评测系统，支持游戏类任务的测试执行、结果显示、结构评分，未来可扩展为结合 LLM 模型的多维评测框架。

---

## 🚀 项目简介

本项目旨在提供一个轻量级的自动化代码评测平台，尤其适用于教学任务、游戏 AI 开发、交互式编程训练等场景。你可以选择任务，提交代码，系统将自动运行测试并返回评估结果。

---

## 🔧 功能特点

- ✅ 支持任务选择与加载（JSON格式定义）
- 🧪 自动执行评测脚本 `run_test.py`
- 🧠 支持结构性得分 `gpt_structure_score.py`（可选）
- 📊 Streamlit 前端界面，交互式展示评测状态
- 📁 易于扩展为支持 LLM、代码解释等功能

---

## 📂 项目结构

code-agent-eval/
├── app.py # 主程序（Streamlit入口）
├── run_test.py # 自定义测试逻辑
├── gpt_structure_score.py # 可选：结构评分逻辑
├── tasks/
│ └── tasks_game_eval.json # JSON格式的所有任务定义
├── evaluator/ # 可选模块扩展
│ └── ...
├── README.md
├── .gitignore


---

## 🧪 示例任务格式

```json
[
  {
    "id": "game_001",
    "description": "实现一个简单的剪刀石头布函数。",
    "input": "opponent: 'rock'",
    "expected_output": "return 'paper'"
  }
]
你可以在 tasks/tasks_game_eval.json 中添加多个任务。

---

##启动前端：
streamlit run app.py
