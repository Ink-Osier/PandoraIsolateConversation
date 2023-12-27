# 项目简介

为了方便大家使用 [PandoraNext](https://github.com/pandora-next/deploy) 进行合租完成了这个小轮子。

![image](https://github.com/Ink-Osier/PandoraIsolateConversation/assets/133617214/1907b4bd-70c8-41a2-b081-16e641ea5686)


# 部署方式

1. docker-compose.yml

```yaml
version: '3'

services:
  backend-to-api:
    image: wizerd/pandora-isolate-middleware:latest
    restart: always
    environment:
      - PANDORA_BACKEND_URL=http://172.17.0.1:8181 # PandoraNext地址
      - FILTER_KEYWORD=* # zPandoraNext中设置的会话隔离关键字，默认为*
    ports:
      - "50012:33333"
    
```

然后执行`docker-compose up -d`.

2. 在PandoraNext反代的nginx中添加如下配置

```nginx
location /backend-api/conversations {
    proxy_set_header Host $host;
    proxy_set_header X-Forwarded-Scheme $scheme;
    proxy_set_header X-Forwarded-Proto  $scheme;
    proxy_set_header X-Forwarded-For    $remote_addr;
    proxy_set_header X-Real-IP		$remote_addr;
    proxy_pass       http://172.17.0.1:50012;
}
```
PS. 将其中的`http://172.17.0.1:50012`替换为你的docker-compose.yml中的端口和nginx可访问到容器的url。

3. 执行`nginx -s reload`重载nginx配置即可。