# Real-time-chat-with-Python-Django Oauth authentication 

Copyright (c) 2013 sharan salokye
Released under the MIT license
http://opensource.org/licenses/mit-license.php

これが使用したPython Djangoのリアルタイムチャットのサンプルコード
https://pypi.python.org/pypi/django-ajax-chat


まず、はじめにデータベースを作成します。下記のコマンドで作成されます。
ここで作成するデータベースは、twitterのOauth認証を用いた際に取得できるaccess_keyとsecret_keyとtwitter名などをひも付けして
格納されます。

>>python manage.py syncdb

TwitterのOauthを用いるためには　https://apps.twitter.com/　のページでアプリを登録してください。
ここで作成されるCONSUMER_KEY と　CONSUMER_SECRET をdjangoChat/views.py内の25,26行目に記入してください。

あとは、runserverをしてサーバを動かし、http://127.0.0.1:8000/chat/　にアクセスするとtwitterの認証が聞かれ、認証が通ると
チャットルームに移動することができます。
また、チャットで書き込んだことは、その人のツイッターにもコメントが反映されるようになっています。（ハッシュタグをつけて）

>>python manage.py runserver

