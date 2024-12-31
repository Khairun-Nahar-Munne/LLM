LLM/                # Main Django project
        manage.py                  # Django entry point
        django_project/            # Django project settings
            __init__.py
            settings.py
            urls.py
            wsgi.py
            asgi.py
        properties/                # Django app for property-related logic
            __init__.py
            admin.py
            apps.py
            cli.py                 # Custom CLI commands for processing properties
            migrations/
                __init__.py
            models.py              # ORM models
            views.py
            tests.py
        requirements.txt           # Python dependencies
    docker-compose.yml             # Docker configuration
    Dockerfile                     # Django service Dockerfile
    ollama/                        # Ollama configuration directory
    .env                           # Environment variables
