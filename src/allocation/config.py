import os


def get_postgres_uri():
    host = os.environ.get("DB_HOST", "localhsot")
    port = 5432
    password = os.environ.get("DB_PASSWORD", "")
    user, db_name = "allocation", "allocation"
    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_api_url():
    host = os.environ.get("API_HOST", "localhost")
    port = 5005
    return f"http://{host}:{port}"


def get_redis_hsot_and_port():
    host = os.environ.get("REDIS_HOST", "localhsot")
    port = 6379
    return dict(host=host, port=port)


def get_email_host_and_port():
    host = os.environ.get("EMAIL_HOST", "localhsot")
    port = 1025
    http_port = 8025
    return dict(host=host, port=port, http_port=http_port)
