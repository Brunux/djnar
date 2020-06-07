django-webinar or djinar
==============================
[![Maintainability](https://api.codeclimate.com/v1/badges/ee82ab1e02631b1948f4/maintainability)](https://codeclimate.com/github/Brunux/djnar/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/ee82ab1e02631b1948f4/test_coverage)](https://codeclimate.com/github/Brunux/djnar/test_coverage)

WebRTC online meeting app

Development
==============================
Get the repo
```sh
$ git clone git@github.com:Brunux/djnar.git
```

Crete a virtual environment use you preferred tool or just
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

Or update Django settings at and add your custom DB configuration
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

Run the tests with nice report
```sh
$ coverage run -m pytest
```

Run development server
```
$ python manage.py runserver 0:8000
```

Open the webinar interface
```
http://localhost:8000/
```

For more information, see TODO.
