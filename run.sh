#!/bin/bash
COMMAND="${1:-payment_service}"

case $COMMAND in
    crud_api)
        echo "Запускается сервис crud_api..."
        cd crud_api
        uv run alembic upgrade head
        python cli.py filldb
        uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    admin)
        cd admin
        uv run streamlit run main.py --client.showErrorDetails=false
       ;;
    *)
        echo "Ошибка: Неверный параметр '$COMMAND'. Используйте 'crud_api' или 'solve_api' или 'admin'"
        exit 1
        ;;
esac
