# AI Navigator

AI・自動化・開発ツール領域のニュースを自動収集し、ブラウザで閲覧できるパーソナルニュースリーダー。

**本番URL**: https://ai-news-eev.pages.dev
**リポジトリ**: https://github.com/suzutomo1984/ai-news-hub

---

## 概要

`my-vault` リポジトリの `自動ニュース配信/` フォルダに蓄積されたMarkdownニュース記事を、`parse_news.py` が `articles.json` に変換し、Cloudflare Pagesで静的サイトとして配信する仕組み。

---

## 構成ファイル

```
ai-news-hub/
├── index.html        # メインUI
├── style.css         # スタイル（ダークテーマ・CSS変数管理）
├── app.js            # フィルター・検索・タブ切り替えロジック
├── parse_news.py     # MarkdownファイルをarticlesJSONに変換するパーサー
├── articles.json     # パーサーの出力（自動生成・gitignore対象）
├── start.bat         # ローカル確認用サーバー起動スクリプト（Windows）
└── audit_report.txt  # parse_news.py の実行ログ（gitignore対象）
```

---

## UIレイアウト（v2 / 2026-03-19）

```
┌─────────────────────────────────────────────────────┐
│ [Ai] AI Navigator  │  最新  ピックアップ  ランキング  │  🔍検索  │
├──────────────┬──────────────────────────────────────┤
│              │  3/18 (WED) 16                        │
│ カテゴリ     │ ┌────────┐ ┌────────┐ ┌────────┐     │
│   ALL        │ │ card   │ │ card   │ │ card   │     │
│   AI/MCP     │ └────────┘ └────────┘ └────────┘     │
│   Obsidian   │                                       │
│   開発ツール  │  3/17 (TUE) 14                        │
│   ノーコード  │ ┌────────┐ ┌────────┐ ┌────────┐     │
│   業務効率化  │ │ card   │ │ card   │ │ card   │     │
│   マーケ     │ └────────┘ └────────┘ └────────┘     │
│              │                                       │
│ 日付         │                                       │
│   All        │                                       │
│   3/18       │                                       │
│   3/17 ...   │                                       │
└──────────────┴──────────────────────────────────────┘
```

- **タブ**: 最新 / ピックアップ / ランキング
- **サイドバー**: カテゴリ・日付フィルター（縦リスト型）
- **カードグリッド**: デスクトップ3列 / タブレット2列 / モバイル1列

---

## アーキテクチャ

```
my-vault リポジトリ
└── 自動ニュース配信/*.md   ← AIが毎日生成するニュース記事
        ↓
    personal-pick.yml（GitHub Actions）
        ↓ parse_news.py を実行
    articles.json を生成
        ↓ git push（手動）
    ai-news-hub リポジトリ（main → gh-pages ブランチ）
        ↓ Cloudflare Pages
    https://ai-news-eev.pages.dev
```

### 2リポジトリ構成

| リポジトリ | 役割 |
|---|---|
| `suzutomo-organization/my-vault` | ニュース記事の生成・parse_news.pyの実行を担うメインリポジトリ |
| `suzutomo1984/ai-news-hub` | フロントエンド（HTML/CSS/JS）とarticles.jsonを管理 |

---

## デプロイフロー

```bash
# 1. ローカルで編集・確認
start.bat   # http://localhost:8080 で確認

# 2. GitHubにpush（mainブランチ）
git add .
git commit -m "feat: ..."
git push origin main

# 3. Cloudflare本番に反映（gh-pagesがプロダクションブランチ）
git push origin main:gh-pages --force
```

> **注意**: CloudflareはGitHubの `gh-pages` ブランチをプロダクションとして監視。
> `main` へのpushはプレビューにしかならない。本番反映には `main:gh-pages` へのpushが必須。

---

## ブランチ構成

| ブランチ | 用途 |
|---|---|
| `main` | 開発・作業用メインブランチ |
| `gh-pages` | Cloudflare Pagesのプロダクションソース |

---

## カテゴリ

| カテゴリ | アイコン | 対象キーワード |
|---|---|---|
| AI/MCP | 🤖 | AIエージェント、LLM、Claude |
| Obsidian | 📝 | Obsidian、PKM、知識管理 |
| 開発ツール | 🛠️ | AI駆動開発、プログラミング、AIコーディング |
| ノーコード | 🔌 | Vibe Coding、個人開発 |
| 業務効率化 | ⚡ | DX、ビジネス |
| マーケ/収益化 | 💰 | Webマーケティング、個人開発マネタイズ |

---

## ローカル確認

```bash
# start.bat を実行（parse_news.py → http.server 起動）
start.bat

# または手動で
python parse_news.py
python -m http.server 8080
# → http://localhost:8080
```

---

## 開発経緯

- **Phase 0（2026-03-18完了）**: ローカルMVP構築・動作確認
- **Phase 1（2026-03-18完了）**: GitHub Actions連携・Cloudflare Pages公開・AI Navigatorにリネーム
- **Phase 2（2026-03-19完了）**: UI v2 - 左サイドバー + 3カラムグリッドレイアウトに刷新
- **Phase 3（今後）**: 機能追加・改善
