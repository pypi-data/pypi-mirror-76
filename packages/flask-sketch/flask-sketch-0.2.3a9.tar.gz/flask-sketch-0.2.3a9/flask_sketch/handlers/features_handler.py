from flask_sketch.utils import Answers, write_tpl, pjoin
from flask_sketch import templates


def handle_caching(answers: Answers):
    answers.settings["development"]["CACHE_TYPE"] = "simple"
    answers.settings["testing"]["CACHE_TYPE"] = "simple"
    answers.settings["production"]["CACHE_TYPE"] = "simple"
    answers.settings["default"]["EXTENSIONS"].extend(
        [f"{answers.args.project_name}.ext.caching:init_app"]
    )


def handle_limiter(answers: Answers):
    answers.settings["default"][
        "RATELIMIT_DEFAULT"
    ] = "200 per day;50 per hour"
    answers.settings["default"]["RATELIMIT_ENABLED"] = True
    answers.settings["development"]["RATELIMIT_ENABLED"] = False
    answers.settings["default"]["EXTENSIONS"].extend(
        [f"{answers.args.project_name}.ext.limiter:init_app"]
    )


def handle_migrate(answers: Answers):
    answers.settings["default"]["EXTENSIONS"].extend(
        [f"{answers.args.project_name}.ext.migrate:init_app"]
    )


def handle_features(answers: Answers):
    features: list = answers.features
    if "debugtoolbar" in features:
        if answers.config_framework == "dynaconf":
            features.remove("debugtoolbar")
        else:
            ...

    for feature in answers.features:
        write_tpl(
            answers.args.project_name,
            f"ext_{feature}_tpl",
            templates.ext,
            pjoin(answers.application_project_folder, "ext", f"{feature}.py"),
        )

        globals()[f"handle_{feature}"](answers)
