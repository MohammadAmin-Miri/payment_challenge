# Development Environment Setup Documentation

This django project consist of two application user and pay which the user part was already developed so I used it instead
of developing it again and the pay application which was designed for this challenge. </BR>

You can use both Swagger with `http://localhost:8000/swagger/` address or Postman collection for using the APIs,
however, using the postman collection is recommended.

_create __.env___ with the bellow content

```
SECRET_KEY='django-insecure-%*@_(96wh!z7zfmq98yk^i7q&z*a4+ymxn^@rmzy%+q6$8jcgi'
ALLOWED_HOSTS='["*"]'
DEVELOPMENT=True

REDIS_HOST='redis'
REDIS_PORT=6379
```

_Run the following command :_

```bash
$ docker compose up -d
```

after running this command project will be configured and ready for running however you need a user for working with
so follow below instructions for creating a user

__vscode configuration :__

_You need to download and install $2$ extensions so open extension tab (`ctrl+shift+x`):_

* `docker`
* `dev containers`

_After the installation, click on the `Remote window` icon (lower left of the vscode window under the settings)_

* _select: `Attach to a running container`_
* _select container name_
  * _Be patient as it need to install some softwares (only first time)_


* _Install any extension you need inside the container as an example `python`: (first time only)_

_open vscode terminal (it should be inside container) :_
**First time only**

```bash
$ python manage.py createsuperuser # <provide credentials>
```
