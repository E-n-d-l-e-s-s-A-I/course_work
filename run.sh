#!/bin/bash
COMMAND="${1:-payment_service}"

case $COMMAND in
    crud_api)
        echo "Запускается сервис crud_api..."
        uv run uvicorn crud_api.main:app --host 0.0.0.0 --port 8000 --reload
        ;;
    *)

        echo "Ошибка: Неверный параметр '$COMMAND'. Используйте 'crud_api' или 'crud_api'"
        exit 1
        ;;
esac
