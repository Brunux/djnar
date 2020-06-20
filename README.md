django-webinar or djinar experiments
==============================
[![Maintainability](https://api.codeclimate.com/v1/badges/ee82ab1e02631b1948f4/maintainability)](https://codeclimate.com/github/Brunux/djnar/maintainability)
![](https://github.com/Brunux/djinar/.github/workflows/django.yml/badge.svg)

Development
==============================
Get the repo
```sh
$ git clone git@github.com:Brunux/djnar.git --branch experiments && cd djnar
```

Create a virtual environment with [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html) or use your favorite tool.
```sh
$ pip install virtualenv
$ virtualenv venv
$ source venv/bin/active
```


Install dependencies
```sh
$ pip install -r requirements/local.txt
```

Create a exclusive Postgres DB docker instance
```sh
$ docker run -d \
    --name djinar \
    -e POSTGRES_USER=django \
    -e POSTGRES_PASSWORD=4dm1n4dm1n \
    -e POSTGRES_DB=djinar
    -p 25432:5432
    postgres
```

Or update Django settings
```python
# djinar/config/settings/local.py
...

DATABASES = {
    # Raises ImproperlyConfigured Exception
    # if DATABASE_URL Not in os.environ and
    # the "default" argument is not defined.
    # The DATABASE_URL environment variables
    # expect a value in the following format:
    # DATABASE_URL=postgres://user:password@hostname_or_ip:port/database_name
    "default": env.db(
        "DATABASE_URL", default="postgres://django:4dm1n4dm1n@localhost:25432/djinar"
    )
}
```

Apply migrations
```sh
$ python manage.py migrate
```

Run development server
```
$ uvicorn project.asgi:application --reload
```

Open experiments
```
http://localhost:8000/experiments/
```
