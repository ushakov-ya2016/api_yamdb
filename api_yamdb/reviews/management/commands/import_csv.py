from csv import DictReader

from django.core.management import BaseCommand
from reviews.models import Category, Comments, Genre, GenreTitle, Review, Title
from users.models import User

FILE_PATH = 'static/data/'

MODELS = {
    Category: 'category.csv',
    Genre: 'genre.csv',
    Title: 'titles.csv',
    GenreTitle: 'genre_title.csv',
    User: 'users.csv',
    Review: 'review.csv',
    Comments: 'comments.csv',
}

DONE_MESSAGE = """
 - Загрузка тестовых данных завершена.
"""
ERROR_MESSAGE = """
 - Cначала нужно удалить файл "db.sqlite3" (уничтожить текущую БД)
 - Выполнить команду "python3 manage.py migrate" (создание новых таблиц)
 - Выполнить команду "python3 manage.py importdata" (загрузка тестовых данных)
 """


class Command(BaseCommand):
    help = "Загрузка тестовых данных из CSV фалов /api_yamdb/static/data/"

    def handle(self, *args, **options):
        """
        Импортирует тестовые данные из таблиц CSV в БД.
        """
        for model, csv in MODELS.items():
            if model.objects.exists():
                return self.stdout.write(self.style.WARNING(ERROR_MESSAGE))

        for row in DictReader(open(FILE_PATH + MODELS[Category])):
            td = Category(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            td.save()

        for row in DictReader(open(FILE_PATH + MODELS[Genre])):
            genre = Genre(
                id=row['id'],
                name=row['name'],
                slug=row['slug'],
            )
            genre.save()

        for row in DictReader(open(FILE_PATH + MODELS[Title])):
            titles = Title(
                id=row['id'],
                name=row['name'],
                year=row['year'],
                category_id=row['category'],
            )
            titles.save()

        for row in DictReader(open(FILE_PATH + MODELS[GenreTitle])):
            genre_title = GenreTitle(
                id=row['id'],
                title_id=row['title_id'],
                genre_id=row['genre_id'],
            )
            genre_title.save()

        for row in DictReader(open(FILE_PATH + MODELS[User])):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name'],
            )
            user.save()

        for row in DictReader(open(FILE_PATH + MODELS[Review])):
            review = Review(
                id=row['id'],
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()

        for row in DictReader(open(FILE_PATH + MODELS[Comments])):
            comment = Comments(
                id=row['id'],
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comment.save()

        return self.stdout.write(self.style.SUCCESS(DONE_MESSAGE))
