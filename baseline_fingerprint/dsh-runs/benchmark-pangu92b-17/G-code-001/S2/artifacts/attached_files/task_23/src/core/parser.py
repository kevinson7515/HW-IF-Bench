def parse_text(text: str) -> dict:
    """
    一个存在缺陷的文本解析器
    """
    # split() 在面对空字符串或纯空白字符时，会返回一个空列表 []
    tokens = text.split()

    # 空输入（空字符串或纯空白）时返回空命令与空参数，避免 IndexError
    if not tokens:
        return {
            "command": "",
            "argument": ""
        }

    command = tokens[0]
    argument = tokens[1] if len(tokens) > 1 else ""

    return {
        "command": command,
        "argument": argument
    }

if __name__ == "__main__":
    # 验证空输入不再抛出 IndexError
    for empty_input in ("", "   ", "\t\n"):
        print(f"正在解析空输入: {repr(empty_input)}")
        print(parse_text(empty_input))