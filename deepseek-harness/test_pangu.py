#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 openPangu 模型 API（OpenAI 兼容接口）
"""

import argparse
import json
import sys
import time

import requests

# ============ 配置 ============
API_BASE = "http://101.245.71.190:9080/v1"
API_KEY = "sk-q0y9YuDs2d879uVEcEp19SSj4t48aKqj1GAz1QTw1iwFQO4T"
MODEL = "openPangu-v21-pro"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
}

TIMEOUT = (5, 120)


# ============ 1. 连通性测试 ============
def test_list_models():
    print("=" * 60)
    print("[1] GET /models  (连通性检查)")
    print("=" * 60)
    url = f"{API_BASE}/models"
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        print(f"HTTP {r.status_code}")
        if r.ok:
            data = r.json()
            ids = [m.get("id") for m in data.get("data", [])]
            print(f"可用模型 ({len(ids)} 个): {ids}")
        else:
            print(r.text[:500])
        return r.ok
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {type(e).__name__}: {e}")
        return False


# ============ 2. 普通（非流式）对话 ============
def test_chat(prompt="帮我讲个笑话"):
    print("=" * 60)
    print("[2] POST /chat/completions  (非流式)")
    print("=" * 60)
    url = f"{API_BASE}/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": False,
    }
    t0 = time.time()
    try:
        r = requests.post(url, headers=HEADERS, json=payload, timeout=TIMEOUT)
        cost = time.time() - t0
        print(f"HTTP {r.status_code}  耗时 {cost:.2f}s")
        if not r.ok:
            print("错误响应:", r.text[:800])
            return False

        data = r.json()
        content = data["choices"][0]["message"]["content"]
        print("-" * 60)
        print(content)
        print("-" * 60)
        usage = data.get("usage")
        if usage:
            print(f"用量: {usage}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {type(e).__name__}: {e}")
        return False


# ============ 3. 流式对话（SSE） ============
def test_chat_stream(prompt="帮我讲个笑话"):
    print("=" * 60)
    print("[3] POST /chat/completions  (流式 SSE)")
    print("=" * 60)
    url = f"{API_BASE}/chat/completions"
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "stream": True,
    }
    t0 = time.time()
    try:
        with requests.post(
            url, headers=HEADERS, json=payload, timeout=TIMEOUT, stream=True
        ) as r:
            print(f"HTTP {r.status_code}")
            if not r.ok:
                print("错误响应:", r.text[:800])
                return False

            # 【关键修正 1】强制按 UTF-8 解码，避免 iter_lines 用 Latin-1 导致中文乱码
            r.encoding = "utf-8"

            first_token_at = None
            got_content = False
            last_usage = None

            for raw in r.iter_lines(decode_unicode=True):
                if not raw:
                    continue
                line = raw.strip()
                if not line.startswith("data:"):
                    continue
                data_str = line[len("data:"):].strip()
                if data_str == "[DONE]":
                    break

                try:
                    chunk = json.loads(data_str)
                except json.JSONDecodeError:
                    continue

                # 【关键修正 2】choices 可能为空（如尾部的 usage chunk），必须判空
                choices = chunk.get("choices") or []
                if not choices:
                    # 记录一下可能的 usage
                    if chunk.get("usage"):
                        last_usage = chunk["usage"]
                    continue

                delta = choices[0].get("delta") or {}
                piece = delta.get("content")
                if piece:
                    if first_token_at is None:
                        first_token_at = time.time() - t0
                    got_content = True
                    sys.stdout.write(piece)
                    sys.stdout.flush()

                # 有些实现在最后一个 choices chunk 里带 finish_reason，不必特殊处理

            print()
            print("-" * 60)
            if first_token_at is not None:
                print(f"首字耗时: {first_token_at:.2f}s  总耗时: {time.time() - t0:.2f}s")
            else:
                print("未收到任何内容片段")
            if last_usage:
                print(f"用量: {last_usage}")
            return got_content
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {type(e).__name__}: {e}")
        return False


# ============ main ============
def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser()
    parser.add_argument("--plain", action="store_true", help="只测非流式对话")
    parser.add_argument("--stream", action="store_true", help="只测流式对话")
    parser.add_argument("--prompt", default="帮我讲个笑话")
    args = parser.parse_args()

    results = {}
    if args.plain:
        results["chat"] = test_chat(args.prompt)
    elif args.stream:
        results["stream"] = test_chat_stream(args.prompt)
    else:
        results["models"] = test_list_models()
        results["chat"] = test_chat(args.prompt)
        results["stream"] = test_chat_stream(args.prompt)

    print("\n" + "=" * 60)
    print("结果汇总:", results)
    ok = all(results.values()) if results else False
    print("全部通过 ✅" if ok else "存在失败项 ❌")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())