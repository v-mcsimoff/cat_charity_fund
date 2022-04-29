Создайте .env файл с переменными для создания первого суперюзера:

```
FIRST_SUPERUSER_EMAIL=
FIRST_SUPERUSER_PASSWORD=
```


Установите всё из requirements.txt, дальше в терминале запустите

```bash
uvicorn app.main:app --reload
```

Swagger развернут по адресу http://127.0.0.1:8000/docs
