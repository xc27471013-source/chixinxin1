#!/usr/bin/env python3
"""
PushPlus 配置测试脚本
用于快速测试 Token 和用户码是否配置正确
"""

import os
import sys
import requests
import json


def test_pushplus():
    """测试 PushPlus 配置"""

    print("=" * 60)
    print("PushPlus 配置测试")
    print("=" * 60)
    print()

    # 获取环境变量
    token = os.getenv("PUSHPLUS_TOKEN", "")
    subscription_users = os.getenv("SUBSCRIPTION_USERS", "")

    # 检查 Token
    print("1. 检查 Token 配置...")
    if not token:
        print("   ❌ PUSHPLUS_TOKEN 环境变量未设置")
        print("   请设置环境变量:")
        print("   export PUSHPLUS_TOKEN='your_token_here'")
        return False
    else:
        print(f"   ✅ Token 已配置 (长度: {len(token)})")
        if len(token) != 32:
            print(f"   ⚠️  警告: Token 长度不是 32 位，可能是错误的")
        print()

    # 检查用户码
    print("2. 检查用户码配置...")
    if not subscription_users:
        print("   ❌ SUBSCRIPTION_USERS 环境变量未设置")
        print("   请设置环境变量:")
        print("   export SUBSCRIPTION_USERS='user_code1,user_code2,user_code3'")
        return False
    else:
        user_codes = [u.strip() for u in subscription_users.split(",")]
        print(f"   ✅ 用户码已配置 (数量: {len(user_codes)})")
        for i, code in enumerate(user_codes, 1):
            if len(code) != 6:
                print(f"   ⚠️  警告: 用户码 {code} 长度不是 6 位")
            else:
                print(f"   ✅ 用户码 {i}: {code}")
        print()

    # 选择推送对象
    print("3. 选择推送对象...")
    print(f"   可选用户: {', '.join(user_codes)}")
    print()
    choice = input("   是否推送测试消息? (y/n, 默认: y): ").strip().lower()
    if choice and choice != 'y':
        print("   ⏭️  跳过推送测试")
        print()
        return True

    # 发送测试消息
    print("4. 发送测试消息...")
    print()

    test_user = user_codes[0]  # 使用第一个用户码测试
    url = "http://www.pushplus.plus/send"  # 注意：官方文档使用 http，不是 https

    test_data = {
        "token": token,
        "title": "Yang Daily Intelligence - 测试消息",
        "content": """
<h2>🎉 PushPlus 配置测试成功！</h2>

<p>如果您看到这条消息，说明：</p>
<ul>
<li>✅ Token 配置正确</li>
<li>✅ 用户码配置正确</li>
<li>✅ 微信服务通知正常</li>
</ul>

<p>现在您可以正常接收 <strong>Yang Daily Intelligence</strong> 认知情报了！</p>

<p><strong>发送时间:</strong> {time}</p>
<p><strong>用户码:</strong> {user_code}</p>

<hr>
<p style="color: #666; font-size: 12px;">
此消息由测试脚本自动发送，请勿回复。<br>
如有问题，请检查环境变量配置。
</p>
        """.format(
            time=__import__('datetime').datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            user_code=test_user
        ),
        "template": "html"
    }

    try:
        print(f"   正在发送到用户: {test_user}...")
        response = requests.post(url, json=test_data, timeout=30)
        result = response.json()

        print(f"   API 响应状态码: {response.status_code}")
        print(f"   API 响应内容: {json.dumps(result, ensure_ascii=False, indent=2)}")
        print()

        if result.get("code") == 200:
            print("   ✅ 推送成功！")
            print()
            print("   📱 请检查您的微信，应该在「服务通知」中收到了测试消息。")
            print()
            return True
        else:
            print("   ❌ 推送失败")
            print(f"   错误信息: {result.get('msg', '未知错误')}")
            print()
            print("   可能的原因:")
            print("   1. Token 不正确或已失效")
            print("   2. 用户码不正确或用户未关注公众号")
            print("   3. 网络连接问题")
            print()
            return False

    except requests.exceptions.Timeout:
        print("   ❌ 请求超时")
        print("   请检查网络连接")
        print()
        return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ 网络请求失败: {str(e)}")
        print()
        return False
    except Exception as e:
        print(f"   ❌ 未知错误: {str(e)}")
        print()
        return False


def main():
    """主函数"""
    try:
        success = test_pushplus()

        print("=" * 60)
        if success:
            print("✅ 测试完成 - 配置正确！")
            print()
            print("下一步:")
            print("1. 启动 Yang Daily Intelligence 工作流")
            print("2. 等待每天 07:30 自动推送")
            print("3. 享受高质量认知情报！")
        else:
            print("❌ 测试失败 - 请检查配置")
            print()
            print("请参考以下文档:")
            print("1. PUSHPLUS_TUTORIAL.md - 详细对接教程")
            print("2. ENV_CONFIG_GUIDE.md - 环境变量配置指南")
        print("=" * 60)

        return 0 if success else 1

    except KeyboardInterrupt:
        print("\n\n⏸️  测试已取消")
        return 1
    except Exception as e:
        print(f"\n\n❌ 发生错误: {str(e)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
