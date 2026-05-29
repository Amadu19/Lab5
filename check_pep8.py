import subprocess
import sys
import glob

PY_FILES = [
    f for f in glob.glob("**/*.py", recursive=True)
    if not any(skip in f for skip in ["venv/", ".venv/", "env/", "check_pep8.py"])
]

if not PY_FILES:
    print("Файлов .py не было обнаружено")
    sys.exit(0)

print(f"Проверяется {len(PY_FILES)} файл(ов): {', '.join(PY_FILES)}")
print("-" * 50)

result = subprocess.run(
    ["pycodestyle"] + PY_FILES,
    capture_output=True,
    text=True
)

if result.stdout:
    print(result.stdout)

if result.returncode != 0:
    print("-" * 50)
    print(f"Проверка PEP-8 не пройдена : Обнаружены ошибки в коде")
    sys.exit(1)
else:
    print("Проверка PEP-8 пройдена: Ошибок не обнаружена")
    sys.exit(0)
