Note Nginx
===============

## Proxy

- `jinja2`によるtemplatingの際は`nginx`の設定だけではうまくいかない場合がある(ssl化の時など)
    - `uvicorn`など、アプリ側の設定項目も確認する必要がある
    - `uvicorn + nginx`でssl化する場合(リバースプロキシ)、nginxで`proxy`関連の設定を行った上で`uvicorn`は`--forwarded-allow-ips`、`--proxy-headers`を適切に設定する必要

------------

## Useful Links

- https://qiita.com/ukitazume/items/1861b4955c8706a87074
- https://qiita.com/hyakt/items/c0aa8005d9a9700fbe45
- https://qiita.com/ywatai@github/items/a179186a458a42b3c7f0
- https://qiita.com/imoimo2009/items/515ceaeea5aeb1bade3a
