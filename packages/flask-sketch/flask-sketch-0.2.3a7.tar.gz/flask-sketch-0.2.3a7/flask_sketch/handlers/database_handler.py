import importlib.resources as pkg_resources  # noqa
from flask_sketch import templates  # noqa
from flask_sketch.utils import (
    Answers,
    GenericHandler,
    write_tpl,
    add_requirements,
    pjoin,
)


def handle_sql_db(answers: Answers):
    write_tpl(
        answers.args.project_name,
        "ext_sqlalchemy_tpl",
        templates.ext,
        pjoin(answers.application_project_folder, "ext", "database.py"),
    )
    write_tpl(
        answers.args.project_name,
        "ext_migrate_tpl",
        templates.ext,
        pjoin(answers.application_project_folder, "ext", "migrate.py"),
    )
    add_requirements(
        answers.project_folder, "flask-sqlalchemy", "flask-migrate"
    )

    answers.settings["default"]["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    answers.settings["development"]["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
    answers.settings["default"][
        "SQLALCHEMY_DATABASE_URI"
    ] = "sqlite:///db.sqlite3"
    answers.settings["default"]["EXTENSIONS"].extend(
        [
            f"{answers.args.project_name}.ext.database:init_app",
            f"{answers.args.project_name}.ext.migrate:init_app",
        ]
    )


def sqlite_handler(answers: Answers):
    if answers.database == "sqlite":
        handle_sql_db(answers)
        return True


def mysql_handler(answers: Answers):
    if answers.database == "mysql":
        handle_sql_db(answers)
        add_requirements(answers.project_folder, "mysqlclient")
        return True


def postgres_handler(answers: Answers):
    if answers.database == "postgres":
        handle_sql_db(answers)
        add_requirements(answers.project_folder, "psycopg2")
        return True


def mongodb_handler(answers: Answers):
    if answers.database == "mongodb":
        return True


def none_handler(answers: Answers):
    if answers.database == "none":
        return True


class DatabaseHandler(GenericHandler):
    ...


database_handler = DatabaseHandler(
    sqlite_handler,
    mysql_handler,
    postgres_handler,
    mongodb_handler,
    none_handler,
)
