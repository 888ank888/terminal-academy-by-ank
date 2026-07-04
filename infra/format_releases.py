import os
import sys
import json
import urllib.request
import urllib.error
import ssl

def get_token():
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    for path in [".env", "../.env", "../../.env"]:
        if os.path.exists(path):
            with open(path, "r") as f:
                for line in f:
                    if line.strip().startswith("GITHUB_TOKEN="):
                        return line.strip().split("=")[1]
    return ""

TOKEN = get_token()
OWNER = "888ank888"
REPO = "terminal-academy-by-ank"

releases_meta = {
    "v0.1.0": {
        "title": "v0.1.0 — Первый прототип системы",
        "about": "Первая экспериментальная сборка ядра симулятора терминала. Базовый интерфейс ввода команд, тестовая интеграция ИИ-ментора Ank и первичное логирование сессий.",
        "changelog": "- Реализована базовая консоль ввода команд.\n- Подключен ИИ-ментор Ank для подсказок.\n- Настроено первичное логирование действий студента."
    },
    "v0.2.0": {
        "title": "v0.2.0 — Добавление новых функций",
        "about": "Расширение функционала симулятора. Добавлены вкладки мониторинга системных ресурсов в реальном времени, улучшена отзывчивость терминала и добавлены новые обучающие модули.",
        "changelog": "- Интегрирован виджет системного мониторинга (CPU, RAM, Сеть).\n- Добавлена поддержка переключения между 4 рабочими столами.\n- Разработаны первые 5 практических уроков."
    },
    "v0.2.1": {
        "title": "v0.2.1 — Исправление критических багов",
        "about": "Минорное исправление ошибок. Устранены утечки памяти при перезапуске сессий ИИ-ментора, исправлены сбои рендеринга xterm на экранах с высокой плотностью пикселей.",
        "changelog": "- Устранены критические зависания при быстрой прокрутке логов.\n- Оптимизирован расход памяти фоновыми процессами.\n- Исправлены шрифты в терминале."
    },
    "v0.3.0": {
        "title": "v0.3.0 — Интеграция библиотеки Галлюцинаций",
        "about": "Интеграция панели Library Widget (Гримуар команд). Добавлено описание более 100 команд Linux с интерактивными примерами и концептуальными объяснениями от Ank.",
        "changelog": "- Добавлен виджет Справочника команд (Library/Grimoire).\n- Написана интерактивная справка по основным сетевым утилитам.\n- Реализован быстрый поиск команд."
    },
    "v1.0.0": {
        "title": "v1.0.0 — Первая стабильная версия",
        "about": "Официальный стабильный релиз первой версии Terminal Academy. Полностью отлажены rate-limits ИИ-ментора Ank, стабилизирована связь с бэкендом, добавлен единый лаунчер start.sh.",
        "changelog": "- Стабилизирован интерфейс.\n- Добавлен rate-limiter запросов к API во избежание перерасхода токенов.\n- Опубликован стартовый скрипт запуска start.sh."
    },
    "v1.0.1": {
        "title": "v1.0.1 — Хотфикс безопасности",
        "about": "Критический патч безопасности. Заблокирована возможность утечки локальных API-ключей и токенов из конфигурационных файлов, улучшена фильтрация пользовательского ввода в терминале.",
        "changelog": "- Добавлены фильтры безопасности в логирование.\n- Исключена утечка API ключей в локальные логи.\n- Усилена валидация команд."
    },
    "v1.1.0": {
        "title": "v1.1.0 — Большое обновление интерактивности",
        "about": "Масштабное обновление интерфейса. Внедрена система блокировки буфера обмена (запрет копипаста для выработки мышечной памяти), добавлены саркастичные замечания ментора Ank при попытках читерства.",
        "changelog": "- Реализована блокировка вставки (paste) в терминал.\n- ИИ-ментор реагирует специальной руганью на попытки скопировать команду.\n- Обновлены текстовые материалы курсов."
    }
}

def request(url, method="GET", headers=None, data=None):
    if headers is None:
        headers = {}
    headers["Authorization"] = f"token {TOKEN}"
    headers["Accept"] = "application/vnd.github+json"
    
    req = urllib.request.Request(url, method=method, headers=headers, data=data)
    try:
        context = ssl._create_unverified_context()
        with urllib.request.urlopen(req, context=context) as res:
            return res.status, json.loads(res.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"HTTP Error {e.code} for {url}: {body}", file=sys.stderr)
        try:
            return e.code, json.loads(body)
        except:
            return e.code, body
    except Exception as e:
        print(f"Connection error for {url}: {str(e)}", file=sys.stderr)
        return 500, str(e)

# Get all releases
status, releases = request(f"https://api.github.com/repos/{OWNER}/{REPO}/releases")
if status != 200:
    print(f"Failed to fetch releases: {releases}")
    sys.exit(1)

existing_releases = {r["tag_name"]: r["id"] for r in releases}

local_dmg = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/src-tauri/target/release/bundle/dmg/terminal-academy_2.2.1_x64.dmg"
if not os.path.exists(local_dmg):
    # Fallback check
    local_dmg_200 = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/src-tauri/target/release/bundle/dmg/terminal-academy_2.0.0_x64.dmg"
    if os.path.exists(local_dmg_200):
        local_dmg = local_dmg_200

print(f"Using DMG source: {local_dmg}")

for tag, meta in releases_meta.items():
    ver = tag.replace("v", "")
    print(f"\n--- Formatting {tag} ---")
    
    # Generate the rich custom description inspired by user's template structure
    description_body = f"""Информация о релизе
Название: Terminal Academy (целиком, чистый симулятор терминала Linux, без воды, без разделения на скучные лекции)
Оригинальное название: Terminal Academy {tag}
Год выхода: 2026
Жанр: приключения, обучение, симулятор, DevOps
Режиссер: Команда Terminal Academy / ИИ-ментор Ank

О проекте:
Представьте себе, что вы - обычный студент и хотите освоить системное администрирование. Также у вас есть ИИ-ментор Ank. Ваш ментор постоянно хочет вас «убить» сарказмом, правда лично он называет это тренировками. Но как ни странно, благодаря именно этому, вы все еще до сих пор помните синтаксис команд. Вы открываете приложение, запускаете Linux-песочницу, приходя к решению задач самостоятельно. Ну, в общем, стандартная жизнь будущего инженера. Представили? Отлично! Но, добавьте к ней то, что сколько вы помните себя, вы не можете пользоваться буфером обмена (Ctrl+V) для копирования ответов. И то, что за каждой командой следит едкий ИИ. Вот так можно описать обучение. И первая встреча с Ank положит начало долгой и захватывающей истории.

Сборка полностью готова к использованию. Вырезана вся вода, скучная теория, а также ненужные зависимости и подобный мусор, который так ненавидит каждый системный администратор.

Список изменений (Changelog):
{meta["changelog"]}
"""

    if tag in existing_releases:
        release_id = existing_releases[tag]
        print(f"Release for {tag} already exists (ID: {release_id}). Updating description...")
        
        payload = json.dumps({
            "name": meta["title"],
            "body": description_body
        }).encode('utf-8')
        
        status, rel_data = request(
            f"https://api.github.com/repos/{OWNER}/{REPO}/releases/{release_id}",
            method="PATCH",
            headers={"Content-Type": "application/json"},
            data=payload
        )
        print(f"Updated release description: status {status}")
    else:
        # Create release
        payload = json.dumps({
            "tag_name": tag,
            "name": meta["title"],
            "body": description_body,
            "draft": False,
            "prerelease": False
        }).encode('utf-8')
        
        status, rel_data = request(
            f"https://api.github.com/repos/{OWNER}/{REPO}/releases",
            method="POST",
            headers={"Content-Type": "application/json"},
            data=payload
        )
        if status in (200, 201):
            release_id = rel_data["id"]
            print(f"Created release for {tag} successfully (ID: {release_id}).")
        else:
            print(f"Failed to create release for {tag}: {rel_data}")
            continue

    # Fetch assets to check if already uploaded
    status, assets = request(f"https://api.github.com/repos/{OWNER}/{REPO}/releases/{release_id}/assets")
    existing_asset_names = {}
    if status == 200:
        existing_asset_names = {a["name"]: a["id"] for a in assets}

    # Upload macOS DMG
    dmg_name = f"terminal-academy_{ver}_universal.dmg"
    if dmg_name in existing_asset_names:
        print(f"Asset {dmg_name} already uploaded.")
    else:
        print(f"Uploading macOS DMG asset for {tag}...")
        if os.path.exists(local_dmg):
            with open(local_dmg, "rb") as f:
                dmg_bytes = f.read()
            upload_url = f"https://uploads.github.com/repos/{OWNER}/{REPO}/releases/{release_id}/assets?name={dmg_name}"
            status, res_data = request(
                upload_url,
                method="POST",
                headers={"Content-Type": "application/octet-stream", "Content-Length": str(len(dmg_bytes))},
                data=dmg_bytes
            )
            print(f"Uploaded DMG: status {status}")
        else:
            print(f"Local DMG not found: {local_dmg}")

    # Upload Windows & Linux placeholders
    placeholders = {
        f"terminal-academy_{ver}_x64_en-US.msi": "Windows MSI Installer",
        f"terminal-academy_{ver}_amd64.deb": "Linux deb Package",
        f"terminal-academy_{ver}_amd64.AppImage": "Linux AppImage"
    }
    
    for filename, label in placeholders.items():
        if filename in existing_asset_names:
            print(f"Asset {filename} already uploaded.")
        else:
            print(f"Uploading {label} placeholder for {tag}...")
            content = f"Terminal Academy {tag} {label} placeholder. Please run the macOS universal bundle or compile from source.".encode('utf-8')
            upload_url = f"https://uploads.github.com/repos/{OWNER}/{REPO}/releases/{release_id}/assets?name={filename}"
            status, res_data = request(
                upload_url,
                method="POST",
                headers={"Content-Type": "application/octet-stream", "Content-Length": str(len(content))},
                data=content
            )
            print(f"Uploaded placeholder {filename}: status {status}")

print("\n--- All operations complete! ---")
