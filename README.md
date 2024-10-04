# Тестовое задание
т/з: https://docs.google.com/document/d/1HrkKll-lkoww0CPw1VY3r95r1F-QAl9biL0RFL45I5E/edit

# Установка через Docker
1. **docker-compose up -d**
2. **docker-compose run kitten_expo python3 workmate/manage.py migrate**

# Установка минимального набора данных
**docker-compose run kitten_expo python3 workmate/manage.py  loaddata fixtures_storage/test.json**

# Запуск тестов
**docker-compose run kitten_expo pytest workmate/**

# Примечания

- **swagger** доступен по http://localhost:8000/api/v1/docs/
- регистрация пользователя по http://localhost:8000/api/v1/auth/users/
- получение JWT токена для зарегистрированного пользователя по http://localhost:8000/api/v1/auth/jwt/create/
- access-токен нужно подавать в запросе в виде Header'а  -H 'Authorization: Bearer token'