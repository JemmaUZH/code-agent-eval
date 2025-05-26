import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "evaluator")))

import streamlit as st
import json
from run_test import run_test
from deepseek_structure_score import score_structure, extract_code_from_zip

# Load all tasks from a single JSON array file
def load_task(task_id):
    with open("tasks/tasks_game_eval.json", "r") as f:
        all_tasks = json.load(f)
        for task in all_tasks:
            if task["id"] == task_id:
                return task
    return None

st.set_page_config(page_title="Code Agent 代码评测系统", layout="wide")
st.title("🤖 Code Agent 自动代码评测系统")

# Sidebar for task selection
st.sidebar.header("选择任务")
task_options = ["game_001", "game_002", "game_003", "game_004", "game_005"]
task_id = st.sidebar.selectbox("任务编号", task_options)
task_data = load_task(task_id)

st.subheader(f"任务名称：{task_data['title']}")
st.markdown(task_data["description"])

# 用户上传 .zip 文件
uploaded_zip = st.file_uploader("📦 或上传包含代码的 ZIP 文件", type="zip")
user_code = ""

if uploaded_zip is not None:
    with open("temp_code.zip", "wb") as f:
        f.write(uploaded_zip.read())
    user_code = extract_code_from_zip("temp_code.zip")
    st.success("✅ 已读取 ZIP 中的代码文件")
else:
    user_code = st.text_area("✍️ 粘贴你生成的 Python 函数代码", height=300)

if st.button("🚀 开始评测"):
    if not user_code.strip():
        st.warning("⚠️ 请上传 ZIP 文件或粘贴代码")
    else:
        with st.spinner("评测中，请稍候..."):
            test_result = run_test(user_code, task_data["test_code"])
            structure_score = score_structure(user_code)

            st.success("✅ 评测完成！")

            st.markdown("### 🧪 测试结果")
            st.write("是否通过测试：", "✅ 是" if test_result["passed"] else "❌ 否")
            if not test_result["passed"]:
                st.write("错误信息：", test_result["error"])

            st.markdown("### 📊 结构评分")
            st.write("结构清晰度：", structure_score["clarity"]) 
            st.write("命名规范：", structure_score["naming"]) 
            st.write("模块化程度：", structure_score["modularity"])

            st.markdown("### 💡 优化建议")
            st.markdown(structure_score["suggestions"])
