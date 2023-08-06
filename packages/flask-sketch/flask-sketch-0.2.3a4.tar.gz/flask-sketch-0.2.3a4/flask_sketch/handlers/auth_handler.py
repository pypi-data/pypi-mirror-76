from flask_sketch.templates import ext  # noqa
from flask_sketch.utils import (
    Answers,
    GenericHandler,
    write_tpl,
    pjoin,
    add_requirements,
)
from flask_sketch import templates


def login_handler(answers: Answers):
    if answers.auth_framework == "login_web":

        return True


def security_web_handler(answers: Answers):
    if answers.auth_framework == "security_web":
        write_tpl(
            answers.args.project_name,
            "security_web_only_tpl",
            templates.commands,
            pjoin(
                answers.application_project_folder, "commands", "__init__.py",
            ),
        )

        write_tpl(
            answers.args.project_name,
            "ext_security_web_only_tpl",
            templates.ext,
            pjoin(answers.application_project_folder, "ext", "auth.py"),
        )

        write_tpl(
            answers.args.project_name,
            "models_security_web_only_tpl",
            templates.models,
            pjoin(answers.application_project_folder, "models", "user.py"),
        )

        add_requirements(
            answers.project_folder, "flask-security-too", "bcrypt"
        )

        return True


def basicauth_web_handler(answers: Answers):
    if answers.auth_framework == "basicauth_web":
        add_requirements(answers.project_folder, "flask-basicAuth")
        return True


def praetorian_handler(answers: Answers):
    if answers.auth_framework == "praetorian":
        add_requirements(answers.project_folder, "flask-praetorian")
        return True


def jwt_extended_handler(answers: Answers):
    if answers.auth_framework == "jwt_extended":
        add_requirements(answers.project_folder, "flask-jwt-extended")
        return True


def basicauth_api_handler(answers: Answers):
    if answers.auth_framework == "basicauth_api":
        add_requirements(answers.project_folder, "flask-basicauth")
        return True


def security_web_api_handler(answers: Answers):
    if answers.auth_framework == "security_web_api":
        add_requirements(
            answers.project_folder, "flask-security-too", "flask-jwt-extended"
        )
        return True


def login_jwt_extended_handler(answers: Answers):
    if answers.auth_framework == "login_jwt_extended":
        add_requirements(
            answers.project_folder, "flask-login", "flask-jwt-extended"
        )
        return True


def basicauth_web_api_handler(answers: Answers):
    if answers.auth_framework == "basicauth_web_api":
        add_requirements(answers.project_folder, "flask-BasicAuth")
        return True


def none_handler(answers: Answers):
    if answers.auth_framework == "none":
        if not answers.database == "none":
            write_tpl(
                answers.args.project_name,
                "no_auth_tpl",
                templates.commands,
                pjoin(
                    answers.application_project_folder,
                    "commands",
                    "__init__.py",
                ),
            )

        return True


class AuthHandler(GenericHandler):
    ...


auth_handler = AuthHandler(
    login_handler,
    security_web_handler,
    basicauth_web_handler,
    praetorian_handler,
    jwt_extended_handler,
    basicauth_api_handler,
    security_web_api_handler,
    login_jwt_extended_handler,
    basicauth_web_api_handler,
    none_handler,
)
