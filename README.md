# リアルタイムでスマホの姿勢を見れる蔵 サーバ
HTTP でセンサデータを受け取り、WebSocket でクライアントに送信するサーバです。

## セットアップ
```bash
pip install -r requirements.txt
```

## 起動
### 開発環境
```bash
uvicorn main:app --reload
```

### 本番環境
```bash
uvicorn main:app
```
