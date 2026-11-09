def parse_text(text: str) -> dict:
    """
    解析文本输入，返回命令与参数；缺失的 token 对应字段为 None。
    """
    # split() 在面对空字符串或纯空白字符时，会返回一个空列表 []
    tokens = text.split()
    
    # tokens 可能为空或不足两个元素，直接索引会抛出 IndexError；缺失字段取 None
    command = tokens[0] if tokens else None
    argument = tokens[1] if len(tokens) > 1 else None
    
    return {
        "command": command,
        "argument": argument
    }

if __name__ == "__main__":
    # 测试空输入触发 IndexError
    empty_input = ""
    print(f"正在解析空输入: {repr(empty_input)}")
    parse_text(empty_input)