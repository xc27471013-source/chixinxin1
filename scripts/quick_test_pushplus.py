#!/usr/bin/env python3
"""
快速测试 PushPlus 连接
直接测试 API 连接，无需复杂配置
"""

import requests
import json


def quick_test():
    """快速测试 PushPlus API 连接"""

    print("=" * 60)
    print("PushPlus API 快速测试")
    print("=" * 60)
    print()

    # 用户输入
    print("请输入以下信息：")
    token = input("1. PushPlus Token (32位字符串): ").strip()
    user_code = input("2. 用户码/好友令牌 (6位字母数字): ").strip()

    if not token or not user_code:
        print()
        print("❌ 错误: Token 和用户码不能为空")
        return False

    # 验证输入
    if len(token) != 32:
        print()
        print(f"⚠️  警告: Token 长度不是 32 位 (当前: {len(token)} 位)")

    if len(user_code) != 6:
        print()
        print(f"⚠️  警告: 用户码长度不是 6 位 (当前: {len(user_code)} 位)")

    print()
    print("=" * 60)
    print("准备发送测试消息...")
    print("=" * 60)
    print()

    # API 地址（注意使用 http）
    url = "http://www.pushplus.plus/send"

    # 请求体
    payload = {
        "token": token,
        "title": "Yang Daily Intelligence - 快速测试",
        "content": """
<h2>🎉 PushPlus API 连接测试成功！</h2>

<p><strong>测试结果：</strong></p>
<ul>
<li>✅ API 地址正确: http://www.pushplus.plus/send</li>
<li>✅ Token 配置正确</li>
<li>✅ 用户码配置正确</li>
<li>✅ HTTP 请求成功</li>
</ul>

<p>如果您在微信中看到这条消息，说明：</p>
<ol>
<li>您的 PushPlus 账号配置正确</li>
<li>您关注了 PushPlus 公众号</li>
<li>API 调用成功</li>
<li>微信服务通知正常</li>
</ol>

<hr>
<p style="color: #666; font-size: 12px;">
此消息由快速测试脚本发送<br>
时间: {time}<br>
用户码: {user_code}
</p>
        """.format(
            time=__import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_code=user_code
        ),
        "template": "html",
        "channel": "wechat",
        "to": user_code
    }

    try:
        print(f"正在请求: {url}")
        print(f"目标用户: {user_code}")
        print()

        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=30
        )

        print(f"HTTP 状态码: {response.status_code}")
        print()

        result = response.json()

        print("API 响应:")
        print(json.dumps(result, ensure_ascii=False, indent=2))
        print()

        if result.get("code") == 200:
            print("✅ 请求成功！")
            print()
            print(f"消息流水号: {result.get('data', 'N/A')}")
            print()
            print("📱 请检查您的微信「服务通知」，应该能收到测试消息。")
            print()
            print("⚠️  注意: code=200 仅表示请求被服务器接收，")
            print("        实际推送是异步处理的，请等待几秒钟。")
            return True
        else:
            print("❌ 请求失败")
            print()
            print(f"错误信息: {result.get('msg', '未知错误')}")
            print()
            print("可能的原因:")
            print("1. Token 无效或已失效")
            print("2. 用户码不正确或用户未关注公众号")
            print("3. API 地址错误（应使用 http，不是 https）")
            return False

    except requests.exceptions.Timeout:
        print("❌ 请求超时")
        print()
        print("请检查网络连接")
        return False

    except requests.exceptions.RequestException as e:
        print(f"❌ 网络请求失败: {str(e)}")
        print()
        print("请检查:")
        print("1. 网络连接是否正常")
        print("2. API 地址是否正确 (http://www.pushplus.plus/send)")
        return False

    except json.JSONDecodeError:
        print("❌ 响应解析失败")
        print()
        print(f"原始响应: {response.text}")
        return False

    except Exception as e:
        print(f"❌ 未知错误: {str(e)}")
        return False


def main():
    """主函数"""
    try:
        print()
        print("=" * 60)
        print("欢迎使用 Yang Daily Intelligence PushPlus 连接测试")
        print("=" * 60)
        print()
        print("本脚本将测试您的 PushPlus API 连接是否正常")
        print()

        success = quick_test()

        print()
        print("=" * 60)
        if success:
            print("✅ 测试完成！")
            print()
            print("下一步:")
            print("1. 在 Coze 工作流中配置环境变量:")
            print("   PUSHPLUS_TOKEN=your_token")
            print("   SUBSCRIPTION_USERS=user_code1,user_code2")
            print()
            print("2. 启动工作流，每天 07:30 自动推送情报")
        else:
            print("❌ 测试失败")
            print()
            print("请参考 PUSHPLUS_API_GUIDE.md 了解详细配置步骤")
        print("=" * 60)
        print()

        return 0 if success else 1

    except KeyboardInterrupt:
        print()
        print()
        print("=" * 60)
        print("⏸️  测试已取消")
        print("=" * 60)
        print()
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
