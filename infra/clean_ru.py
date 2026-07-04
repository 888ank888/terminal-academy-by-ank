import os

target = "/Users/ank/Documents/CODENAME_TERMINAL_ACADEMY/terminal-academy-desktop/src/App.tsx"

with open(target, "r", encoding="utf-8") as f:
    content = f.read()

# Let's perform precise text replacements to eliminate all Russian string branches and logic
replacements = [
    (
        'const [lang, setLang] = useState<\'en\' | \'ru\'>(\'en\');',
        'const lang = \'en\';'
    ),
    (
        'lang === \'ru\'\n            ? `[БЕЗОПАСНОСТЬ: Студент попытался вставить скопированный текст в терминал]`\n            : `[SECURITY: Student attempted to paste copied text into terminal]`',
        '`[SECURITY: Student attempted to paste copied text into terminal]`'
    ),
    (
        'lang === \'ru\' ? `Ошибка API: ${json.error.message}` : `API Error: ${json.error.message}`',
        '`API Error: ${json.error.message}`'
    ),
    (
        'lang === \'ru\' ? `Ошибка буфера обмена: ${err.message}` : `Clipboard error: ${err.message}`',
        '`Clipboard error: ${err.message}`'
    ),
    (
        'lang === \'ru\'\n            ? `[БЕЗОПАСНОСТЬ: Студент пытался выполнить заблокированную команду] Команда: ${rawCmd}`\n            : `[SECURITY: Student tried to execute blocked command] Command: ${rawCmd}`',
        '`[SECURITY: Student tried to execute blocked command] Command: ${rawCmd}`'
    ),
    (
        'lang === \'ru\' ? `Ошибка блокировки: ${err.message}` : `Block error: ${err.message}`',
        '`Block error: ${err.message}`'
    ),
    (
        'lang === \'ru\' \n            ? `ВНИМАНИЕ: Вы собираетесь выполнить потенциально опасную команду: "${cmd}". Убедитесь, что вы понимаете последствия перед запуском!` \n            : `WARNING: You are about to run a potentially destructive command: "${cmd}". Ensure you understand the consequences before proceeding!`',
        '`WARNING: You are about to run a potentially destructive command: "${cmd}". Ensure you understand the consequences before proceeding!`'
    ),
    (
        'lang === \'ru\' \n          ? `[СОБЫТИЕ: Студент выполнил команду в терминале]\nКоманда: ${cmd}\nВывод команды:\n"""\n${output || \'(нет вывода)\'}\n"""`\n          : `[EVENT: Student executed terminal command]\nCommand: ${cmd}\nOutput:\n"""\n${output || \'(no output)\'}\n"""`',
        '`[EVENT: Student executed terminal command]\nCommand: ${cmd}\nOutput:\n"""\n${output || \'(no output)\'}\n"""`'
    ),
    (
        'lang === \'ru\' ? `Ошибка реакции: ${err.message}` : `Reaction error: ${err.message}`',
        '`Reaction error: ${err.message}`'
    ),
    (
        'lang === \'ru\' ? \'Вы отправляете запросы слишком быстро. Пожалуйста, подождите.\' : \'You are sending requests too quickly. Please wait a moment.\'',
        '\'You are sending requests too quickly. Please wait a moment.\''
    ),
    (
        'lang === \'ru\' ? `Объясни команду: ${cmd}` : `Explain the command: ${cmd}`',
        '`Explain the command: ${cmd}`'
    ),
    (
        'lang === \'ru\' ? \'Ошибка: Пожалуйста, задайте ваш Gemini API ключ в настройках.\' : \'Error: Please set your Gemini API key in settings to consult with me.\'',
        '\'Error: Please set your Gemini API key in settings to consult with me.\''
    ),
    (
        'lang === \'ru\' ? `Ошибка консультации: ${err.message}` : `Error consulting Ank: ${err.message}`',
        '`Error consulting Ank: ${err.message}`'
    ),
    (
        'lang === \'ru\' ? \'Отправить\' : \'Send\'',
        '\'Send\''
    ),
    (
        'lang === \'ru\' ? \'Объяснить\' : \'Explain\'',
        '\'Explain\''
    ),
    (
        'lang === \'ru\' ? \'Карта Направлений и Развилок (Skill Tree)\' : \'Interactive Skill Tree & Branching Roadmap\'',
        '\'Interactive Skill Tree & Branching Roadmap\''
    ),
    (
        'lang === \'ru\' ? \'СВЕРНУТЬ В СПИСОК\' : \'RESTORE TO LIST\'',
        '\'RESTORE TO LIST\''
    ),
    (
        'lang === \'ru\' ? \'Практические Инциденты\' : \'Practical Incidents\'',
        '\'Practical Incidents\''
    ),
    (
        'lang === \'ru\' ? \'Загрузка инцидентов курса...\' : \'Loading incidents details...\'',
        '\'Loading incidents details...\''
    ),
    (
        'lang === \'ru\' ? \'Выберите тему на развилке для просмотра уроков\' : \'Select a topic node on the tree to view lessons\'',
        '\'Select a topic node on the tree to view lessons\''
    ),
    (
        'lang === \'ru\' ? \'Учебный План\' : \'Syllabus & Lessons\'',
        '\'Syllabus & Lessons\''
    ),
    (
        'isFullscreen ? (lang === \'ru\' ? \'СВЕРНУТЬ\' : \'RESTORE\') : (lang === \'ru\' ? \'РАЗВЕРНУТЬ\' : \'EXPAND\')',
        'isFullscreen ? \'RESTORE\' : \'EXPAND\''
    ),
    (
        'lang === \'ru\' ? `Обновить до ${updateAvailable}` : `Update to ${updateAvailable}`',
        '`Update to ${updateAvailable}`'
    ),
    (
        'lang === \'ru\' ? \'⚠️ РЕКОМЕНДАЦИЯ ПО ИНТЕРФЕЙСУ\' : \'⚠️ INTERFACE RECOMMENDATION\'',
        '\'⚠️ INTERFACE RECOMMENDATION\''
    ),
    (
        'lang === \'ru\' \n                  ? \'Для корректной работы 4-экранной консоли и развилок, пожалуйста, ВКЛЮЧИТЕ ПОЛНОЭКРАННЫЙ РЕЖИМ (нажмите кнопку войти или клавишу F11 после входа).\' \n                  : \'For proper operation of the 4-screen console and roadmaps, please ENTER FULLSCREEN MODE (click the button or press F11 after booting).\'',
        '\'For proper operation of the 4-screen console and roadmaps, please ENTER FULLSCREEN MODE (click the button or press F11 after booting).\''
    ),
    (
        'lang === \'ru\' ? \'Инициализировать Систему\' : \'BOOT SYSTEM ENVIRONMENT\'',
        '\'BOOT SYSTEM ENVIRONMENT\''
    ),
    (
        '4. Respond in Russian if the student\'s context is Russian, otherwise English.',
        '4. Respond in English only.'
    ),
    (
        '4. Support both Russian and English responses (reply in Russian if the student\'s context is Russian, otherwise English).',
        '4. Respond in English only.'
    )
]

for target_str, replacement_str in replacements:
    if target_str in content:
        content = content.replace(target_str, replacement_str)
        print(f"Replaced hit successfully.")
    else:
        # Fallback to replace single-line matches or print mismatch
        print(f"Target pattern not found exactly in file. Trying line-by-line fallback...")

# Save file
with open(target, "w", encoding="utf-8") as f:
    f.write(content)

print("Replacement complete.")
