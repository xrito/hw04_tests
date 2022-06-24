## hw04_tests - добавление функционала и покрытие тестами проекта hw03_forms
 Файл posts/tests.py

#### Тестами проверяется:
1. Создание персональной страницы после регистрации пользователя 
2. Авторизованный пользователь может опубликовать пост (new)
3. Неавторизованный посетитель не может опубликовать пост (его редиректит на страницу входа)
4. После публикации поста новая запись появляется на главной странице сайта (index), на персональной странице пользователя (profile), и на отдельной странице поста (post)
5. Авторизованный пользователь может отредактировать свой пост и его содержимое изменится на всех связанных страницах
7. Добавлены тесты проверяющие, что если при создании поста указать группу, то этот пост появляется:
  - на главной странице сайта,
  - на странице выбранной группы,
  - в профайле пользователя.
8. Добавлены тесты проверяющие, что при создании поста, этот пост не попал в группу, для которой не был предназначен.
9. Добавлены тесты проверяющие, что при отправке валидной формы со страницы создания поста reverse(posts:create_post) создаётся новая запись в базе данных.
10. Добавлены тесты проверяющие, что при отправке валидной формы со страницы редактирования поста reverse(posts:create_post args='post_id') происходит изменение поста с post_id в базе данных.
## Стек
При написании тестов использовалась библиотека Unittest, и методы setUp и setUpClass

### Автор

[![Telegram](https://img.shields.io/badge/-Telegram-464646?style=flat-square&logo=Telegram)](https://t.me/harkort)
[<img src='https://cdn.jsdelivr.net/npm/simple-icons@3.0.1/icons/github.svg' alt='github' height='40'>](https://github.com/xrito)  

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![pytest](https://img.shields.io/badge/-pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![SQLite3](https://img.shields.io/badge/-SQLite3-464646?style=flat-square&logo=SQLite)](https://www.sqlite.org/)
