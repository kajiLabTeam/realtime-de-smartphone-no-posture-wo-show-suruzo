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

## ファイル構成
- `main.py`: FastAPI のエンドポイントと処理を定義
- `src/`
  - `wsManager.py`: WebSocket の管理
  - `filter.py`: フィルタ処理
  - `type.py`: 型定義 & バリデーション
