def parse_text(text: str) -> dict:
    """
    一个文本解析器，将输入拆分为命令与参数
    """
    # split() 在面对空字符串或纯空白字符时，会返回一个空列表 []
    tokens = text.split()
    
    # 空输入或纯空白字符时没有可解析的内容，直接返回空结果
    if not tokens:
        return {
            "command": None,
            "argument": None
        }

    command = tokens[0]
    # 只有一个词时不存在参数，避免 tokens[1] 越界
    argument = tokens[1] if len(tokens) > 1 else None
    
    return {
        "command": command,
        "argument": argument
    }

if __name__ == "__main__":
    # 验证空输入不再抛出 IndexError
    empty_input = ""
    print(f"正在解析空输入: {repr(empty_input)}")
    print(f"解析结果: {parse_text(empty_input)}")