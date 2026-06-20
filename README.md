# 📚 Semka Informatics

Персональный сайт с работами по информатике.  
Каждая практическая работа доступна для просмотра онлайн с подсветкой кода и возможностью скачивания.

🌐 Демо: https://isemene4kai.ru  

---

## 🚀 Возможности

- 📄 Красивый просмотр кода с подсветкой (highlight.js)
- ⬇️ Скачивание файлов
- 🔗 Быстрая ссылка на GitHub
- 📅 Отображение даты изменения
- 🔎 Поиск и фильтрация по языку
- 📊 Статистика просмотров и RSS-лента обновлений
- ↔️ Навигация между соседними работами и ссылки на строки
- 🧠 Автоматическое преобразование названий:
  
  `1part2.py → Практическая работа 1 часть 2`

- 🐳 Docker-ready, с liveness/readiness проверками
- ☸️ Развёртывание в k3s через Argo CD и Traefik

---

## 🛠 Технологии

- Python 3.12
- Flask
- Gunicorn
- Docker
- k3s, Traefik и Argo CD
- Highlight.js

---

## 📦 Запуск локально

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m app.app
```

## Проверки

```bash
.venv/bin/pytest
.venv/bin/ruff check .
```

Production-развёртывание хранится в репозитории
[`ISemene4kaI/sites_kubernetes`](https://github.com/ISemene4kaI/sites_kubernetes):
Argo CD синхронизирует Helm values, Traefik принимает трафик, а счётчики
просмотров сохраняются на PVC в `/data`.
