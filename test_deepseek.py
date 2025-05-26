import openai

openai.api_key = "sk-7e52bb6e47c1414f88430c93c5113def"
openai.api_base = "https://api.deepseek.com/v1"

prompt = """
请对下面这段代码结构性打分并以 JSON 返回：
```
def add(a,b): return a+b
```
返回格式：
{
  "clarity": 8,
  "naming": 9,
  "modularity": 7,
  "suggestions": "命名可以更具体，逻辑可以扩展"
}
"""

response = openai.ChatCompletion.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": prompt}],
    temperature=0.3
)

print("✅ LLM 返回内容：")
print(response["choices"][0]["message"]["content"])
