def parse_text(text: str) -> dict:
    """
    一个存在缺陷的文本解析器
    """
    # split() 在面对空字符串或纯空白字符时，会返回一个空列表 []
    tokens = text.split()
    
    # 错误点：没有检查 tokens 是否为空，直接访问索引 0
    # 当输入为空时，会抛出：IndexError: list index out of range
    command = tokens[0]
    argument = tokens[1]
    
    return {
        "command": command,
        "argument": argument
    }

if __name__ == "__main__":
    # 测试空输入触发 IndexError
    empty_input = ""
    print(f"正在解析空输入: {repr(empty_input)}")
    parse_text(empty_input)