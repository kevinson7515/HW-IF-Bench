def parse_text(text: str) -> dict:
    """
    将文本解析为命令与参数。
    空输入或纯空白输入返回空的 command 与 argument，而不抛出异常。
    """
    # split() 在面对空字符串或纯空白字符时，会返回一个空列表 []
    tokens = text.split()

    # 缺少对应 token 时回退为空字符串，避免索引越界
    command = tokens[0] if tokens else ""
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