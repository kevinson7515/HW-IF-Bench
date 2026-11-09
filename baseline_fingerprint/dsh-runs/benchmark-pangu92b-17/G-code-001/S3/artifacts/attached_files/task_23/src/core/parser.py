def parse_text(text: str) -> dict:
    """
    解析文本为命令与参数。

    对空输入或仅含空白的输入，返回空命令与空参数，而不是抛出 IndexError。
    """
    tokens = text.split()

    command = tokens[0] if len(tokens) > 0 else ""
    argument = tokens[1] if len(tokens) > 1 else ""

    return {
        "command": command,
        "argument": argument
    }

if __name__ == "__main__":
    # 测试空输入触发 IndexError
    empty_input = ""
    print(f"正在解析空输入: {repr(empty_input)}")
    parse_text(empty_input)