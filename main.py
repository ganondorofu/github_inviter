# -*- coding: utf-8 -*-
import os
import sys
import json
import requests

# ==== 設定 ====
TOKEN = "とーくん"  # Personal Access Token
ORG_NAME = "そしき"                            # 招待先組織名
INPUT_FILE = "invite_list.txt"                     # ユーザー一覧ファイル名
ROLE = "direct_member"                             # 招待時のロール ("direct_member" or "admin")
API_BASE = "https://api.github.com"
# ==============

# ユーザー一覧ファイルの存在チェック
if not os.path.exists(INPUT_FILE):
    print(f"エラー: ファイル '{INPUT_FILE}' が見つかりません。")
    sys.exit(1)

# ファイル読み込み：空行を除去してリスト化
with open(INPUT_FILE, encoding="utf-8") as f:
    usernames = [line.strip() for line in f if line.strip()]

# HTTP ヘッダー準備
headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}

# 招待用エンドポイント
invite_url = f"{API_BASE}/orgs/{ORG_NAME}/invitations"

# 全ユーザーをループして招待実行
for username in usernames:
    # ユーザー情報取得 (numeric ID が必要)
    user_resp = requests.get(f"{API_BASE}/users/{username}", headers=headers)
    if user_resp.status_code != 200:
        print(f"[失敗] ユーザー '{username}' の取得に失敗しました (status={user_resp.status_code})")
        continue

    user_id = user_resp.json().get("id")
    payload = {
        "invitee_id": user_id,
        "role": ROLE
    }

    # 招待リクエスト
    resp = requests.post(invite_url, headers=headers, data=json.dumps(payload))
    if resp.status_code in (201, 204):
        print(f"[成功] {username} を '{ORG_NAME}' に招待しました。")
    else:
        # エラーメッセージ取得
        msg = resp.json().get("message", "")
        errs = resp.json().get("errors", "")
        print(f"[失敗] {username} の招待に失敗: {msg} {errs}")
