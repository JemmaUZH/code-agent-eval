import openai
import os
import traceback
import zipfile

openai.api_key = "sk-7e52bb6e47c1414f88430c93c5113def"
openai.api_base = "https://api.deepseek.com/v1"

def extract_code_from_zip(zip_path: str) -> str:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for name in zip_ref.namelist():
            if name.endswith('.py'):
                with zip_ref.open(name) as file:
                    return file.read().decode('utf-8')
    return ""

def score_structure(user_code: str) -> dict:
    prompt = f"""
你是一位严谨的代码审阅专家，请对以下 Python 函数的结构性进行专业评分和改进建议，
重点基于代码本身的写法而非模板化输出。

代码如下：
```
{user_code}
```

请严格根据以下三个维度进行 1-10 分评分，并尽量依据代码真实质量评估，不要总是给出固定示例分：
1. clarity（结构清晰度）：代码的逻辑是否清晰，缩进是否合理，有无混乱堆叠或重复逻辑
2. naming（命名规范）：函数名和变量名是否语义明确、符合 Python 风格，避免使用 a1、b2 之类无意义命名
3. modularity（模块化程度）：是否使用函数封装逻辑，是否具备复用性，是否存在过度耦合

请返回 JSON 格式的评分和建议，如下所示（注意：请根据真实质量灵活评分，不要机械照搬）：
{{
  "clarity": 6,
  "naming": 5,
  "modularity": 4,
  "suggestions": "建议将重复逻辑封装成函数，并改善变量命名的表达性。"
}}
"""

    try:
        print("🟡 正在调用 DeepSeek...")
        response = openai.ChatCompletion.create(
            model="deepseek-chat",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        )
        content = response["choices"][0]["message"]["content"]
        print("🔁 LLM 回复内容：", content)

        # 清理 markdown 包裹的 ```json 块
        cleaned = content.strip()
        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        # 安全解析结构评分 JSON
        if cleaned.startswith("{") and cleaned.endswith("}"):
            try:
                result = eval(cleaned)
                required_keys = {"clarity", "naming", "modularity", "suggestions"}
                if required_keys.issubset(result.keys()):
                    # 如果建议是列表，转为 markdown
                    if isinstance(result["suggestions"], list):
                        result["suggestions"] = "\n".join(f"- {s}" for s in result["suggestions"])
                    return result
            except Exception as parse_error:
                print("⚠️ JSON 解析失败：", parse_error)

        # fallback 返回结构（评分失败）
        return {
            "clarity": 0,
            "naming": 0,
            "modularity": 0,
            "suggestions": "DeepSeek 返回内容无法解析为结构评分，请检查 prompt 或模型回复格式。"
        }

    except Exception as e:
        print("❌ DeepSeek 错误详情：", traceback.format_exc())
        return {
            "clarity": 0,
            "naming": 0,
            "modularity": 0,
            "suggestions": "DeepSeek 评分失败，请检查模型名称和 base_url 设置。"
        }
