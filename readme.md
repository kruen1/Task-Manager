# Personal Task Manager API

Простенькое приложение для управления личными задачами.

## Функционал
1. Создание задачи (POST /tasks)
2. Список задач с фильтрами по статусу и приоритету (GET /tasks)
3. Получение задачи по ID (GET /tasks/{id})
4. Обновление задачи (PUT /tasks/{id})
5. Удаление задачи (DELETE /tasks/{id})
6. Отметка задачи как выполненной (PATCH /tasks/{id}/complete)
7. Статистика по задачам (GET /tasks/stats/summary)
