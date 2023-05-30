# dian-news-bot

I have no idea.

```
podman run -it -d --name=dian-news-bot -v $(pwd)/config:/app/config:z -v $(pwd)/db_file.db:/app/db_file.db:z abluestudent/dian-news-bot
podman generate systemd --new --files --name dian-news-bot
systemctl --user enable container-dian-news-bot.service
```
