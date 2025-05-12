#!/bin/bash
COMMAND="${1:-payment_service}"

case $COMMAND in
    crud_api)
        echo "Запускается сервис crud_api..."
        cd crud_api
        alembic upgrade head
        python cli.py filldb
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    admin)
        cd admin
        streamlit run main.py --client.showErrorDetails=false
       ;;
    solve_api)
        echo "Запускается сервис solve_api..."
        cd solve_api
        uvicorn main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    *)
        echo "Ошибка: Неверный параметр '$COMMAND'. Используйте 'crud_api' или 'solve_api' или 'admin'"
        exit 1
        ;;
esac
