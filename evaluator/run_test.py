import traceback

def run_test(user_code: str, test_code: str) -> dict:
    try:
        # 创建独立的命名空间
        local_env = {}

        # 执行用户代码
        exec(user_code, {}, local_env)

        # 执行测试代码
        exec(test_code, {}, local_env)

        return {"passed": True}

    except Exception as e:
        return {
            "passed": False,
            "error": traceback.format_exc(limit=3)
        }
