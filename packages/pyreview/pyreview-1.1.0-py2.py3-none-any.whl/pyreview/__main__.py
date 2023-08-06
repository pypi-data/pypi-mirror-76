#!/usr/bin/env python
__all__ = ("main",)


def main():
    """
    Tool to deploy a Heroku Review App in Bitbucket Pipelines.

    Environment Variables used from Bitbucket Pipelines:
        - BITBUCKET_COMMIT: commit hash to be used as the deploy version
        - BITBUCKET_BRANCH: git branch to be used as project name

    Environment Variables needed:
        - Path to the project
        - settings for the Heroku Platform API (HEROKU_API_KEY)
        - Bitbucket Pipelines variables (HEROKU_PIPELINE_NAME)
        - Heroku Project Name (HEROKU_DEV_NAME)

    Make sure you include this envs in the pipeline:
        - HEROKU_API_KEY: Heroku api key
        - HEROKU_PROJECT_NAME: Heroku

    https://devcenter.heroku.com/articles/heroku-postgres-backups#direct-database-to-database-copies
    """
    import os
    from pathlib import Path

    from dotenv import load_dotenv

    from .create_review_app import create_review_app
    from .pipeline import get_pipeline_id
    from .source_blob import create_source_blob
    from .utils import filter_env_vars

    base_dir = Path.cwd()
    env_path = base_dir / ".env"
    load_dotenv(dotenv_path=env_path)

    base_url = "https://api.heroku.com"

    api_key = os.getenv("HEROKU_API_KEY")
    branch = os.getenv("BITBUCKET_BRANCH")
    project = os.getenv("HEROKU_DEV_NAME")
    version = os.getenv("BITBUCKET_COMMIT")
    heroku_pipeline_name = os.getenv("HEROKU_PIPELINE_NAME")

    headers = {
        "Accept": "application/vnd.heroku+json; version=3",
        "Authorization": f"Bearer {api_key}",
    }

    pipeline = get_pipeline_id(base_url, headers, heroku_pipeline_name)
    source_blob_url = create_source_blob(base_url, headers, base_dir, project, version)
    envs = filter_env_vars("CI_")

    data = {
        "branch": branch,
        "pipeline": pipeline,
        "source_blob": {"url": source_blob_url, "version": version,},
        "environment": envs,
    }

    res = create_review_app(base_url, headers, data)

    return res


if __name__ == "__main__":  # pragma: no cover
    main()
