# ⚙️ SERVICE.COMMAND-HANDLE

![main_img](https://github.com/STALCRAFT-FUNCKA/toaster.command-handling-service/assets/76991612/bbb5fee4-803e-4613-8f19-9acb5daf4e1e)

## 📄 Информация

**SERVICE.COMMAND-HANDLER** - сервис обработки событий, классифицированных как "command". Событие приходит от сервиса фетчинга через шину Redis, после чего обрабатывается, параллельно логируя свои дейстивия как внутри контейнера (внутренние логи), так и внутри лог-чатов (внешние логи).

### Входные данные

Пример обьекта события, которое приходит на service.command-handler:

```python
class Event:
    event_id: str
    event_type: str

    peer: Peer
    user: User
    message: Message
```

```python
class Message(NamedTuple):
    cmid: int
    text: str
    reply: Optional[Reply]
    forward: List[Reply]
    attachments: List[str]
```

```python
class Peer(NamedTuple):
    bpid: int
    cid: int
    name: str
```

```python
class User(NamedTuple):
    uuid: int
    name: str
    firstname: str
    lastname: str
    nick: str
```

Далее, сервис определяет командлет внутри текста сообщения и исполняет вызываемую команду.

### Выходные данные

Иногда бывает так, что сервису необходимо тоже что-то отправить в шину Redis.
Случается это при использовании таких команд как "warn", "delete", "kick", "unwarn".
Каждая из этих команд подразумевает применение каких-то санкций в сторону пользователя.
Отсюда появляется новый тип события "Punishment". Оно значительно проще события "Event", но играет не меньшую роль в работе сервисов.

```python
class Punishment:
    punishment_type: str
    comment: str
    cmids: Union[int, List[int]]
    bpid: int
    uuid: int
    points: Optional[int]
    mode: Optional[str]
```

### Дополнительно

Docker setup:

```text
    docker network
        name: TOASTER
        ip_gateway: 172.18.0.1
        subnet: 172.18.0.0/16
        driver: bridge
    

    docker image
        name: service.command-handler
        args:
            TOKEN: "..."
            GROUPID: "..."
            SQL_HOST: "..."
            SQL_PORT: "..."
            SQL_USER: "..."
            SQL_PSWD: "..."
    

    docker container
        name: service.command-handler
        network_ip: 172.1.08.6
```

Jenkins shell command:

```shell
imageName="service.command-handler"
containerName="service.command-handler"
localIP="172.18.0.6"
networkName="TOASTER"

#stop and remove old container
docker stop $containerName || true && docker rm -f $containerName || true

#remove old image
docker image rm $imageName || true

#build new image
docker build . -t $imageName \
--build-arg TOKEN=$TOKEN \
--build-arg GROUPID=$GROUPID \
--build-arg SQL_HOST=$SQL_HOST \
--build-arg SQL_PORT=$SQL_PORT \
--build-arg SQL_USER=$SQL_USER \
--build-arg SQL_PSWD=$SQL_PSWD

#run container
docker run -d \
--name $containerName \
--restart always \
$imageName

#network setup
docker network connect --ip $localIP $networkName $containerName

#clear chaches
docker system prune -f
```
