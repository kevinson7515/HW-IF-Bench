def parse_text(text: str) -> dict:
    """
    解析文本输入，提取命令与参数。

    空输入或仅含空白字符时，command 与 argument 均为 None；
    只有命令而没有参数时，argument 为 None。
    """
    tokens = text.split()

    if not tokens:
        return {"command": None, "argument": None}

    command = tokens[0]
    argument = tokens[1] if len(tokens) > 1 else None

    return {
        "command": command,
        "argument": argument
    }

if __name__ == "__main__":
    # 验证空输入与缺失参数不再抛出 IndexError
    for sample in ("", "   ", "help", "run job"):
        print(f"正在解析输入: {repr(sample)}")
        print(parse_text(sample))
