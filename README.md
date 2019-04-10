# rss_proxy

プロキシ＋パスワード認証が必要なRSS

## このスクリプトがしてくれること
1. サーバーにプロキシを通してRSSを取得
2. スクリプト実行時の前日に公開された記事のタイトル・リンク・本文をSlackに投稿 (Incoming WebHooksを利用)

## つかいかた
0. `git clone`する。
1. `config_sample.yml`を複製して`config.yml`とする。
2. `config.yml`にプロキシサーバーの認証情報、RSS取得先、Incoming WebHooksのURLを入力
3. 関数`feed_of_the_day`の`if`文内の処理を、実際のRSSの中身にあわせて変更 (このスクリプトでは、取得先にpublishedがなく、タイトル末尾に日付が`yyyy-mm-dd`の形で入っていたのでこのようにしてある)
4. `cd rss_proxy`
5. `python feed_extraction.py`

※プロキシサーバーでパスワード認証がない場合や、プロキシを通す必要がそもそもない場合は関数`proxy_auth`をいじったり、関数`feed_of_the_day`で`feed = feedparser.parse(target_url)`としたりすればよいはず。
