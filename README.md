# Сервис Благотворительного фонда поддержки котиков: QRKot

Фонд собирает пожертвования на любые цели, связанные с поддержкой кошачьей популяции.

В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Реализована возможность получения отчета с перечнем профинансированных проектов, отсортированных по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.

## Технологии
- Python
- FastAPI
- SQLAlchemy
- Alembic
- Uvicorn
- Google Sheets API и Google Drive API

## Использование

#### Клонируйте реппозиторий

```sh
git clone https://github.com/94R1K/cat_charity_fund.git
```

#### Перейдите в папку cat_charity_fund, установите и запустите виртуальное окружение.

```sh
cd cat_charity_fund
```

```
python -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/Scripts/activate
    ```
#### Установите зависимости:

```sh
pip install -r requirements.txt
```

#### Запустите приложение на локальном сервере

```sh
uvicorn app.main:app --reload
```


# Об авторе
Лошкарев Ярослав Эдуардович \
Python-разработчик (Backend) \
Россия, г. Москва \
E-mail: real-man228@yandex.ru 

[![VK](https://img.shields.io/badge/Вконтакте-%232E87FB.svg?&style=for-the-badge&logo=vk&logoColor=white)](https://vk.com/yalluv)
[![TG](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/yallluv)
