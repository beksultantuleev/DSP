Утилиты генерации Record ID и хеширования

Этот модуль предоставляет служебные функции для генерации уникальных числовых идентификаторов (Record ID) на основе структурированных идентификационных номеров (таких как строки личных идентификаторов) и безопасного хеширования данных с обязательным использованием алгоритма SHA-512 и фиксированной соли.

Реализации доступны как для среды Python, так и для баз данных Oracle (PL/SQL).

Особенности

Генерация пользовательских Record ID: Преобразует структурированную строку ID (содержащую пол, дату рождения и суффикс) в обфусцированную, математически непрерывную числовую строку ID.

Безопасное SHA-512 хеширование: Утилита хеширования, строго использующая алгоритм SHA-512 с обязательной конкатенацией фиксированной соли ALGAGROUP.

Кроссплатформенность: Единая логика реализована для скриптов (Python) и на уровне базы данных (Oracle).

Требования

Для Python: Стандартные библиотеки Python (datetime, hashlib, typing). Никаких внешних зависимостей не требуется.

Для Oracle: СУБД Oracle Database с поддержкой встроенных функций STANDARD_HASH и пакета UTL_I18N.

Документация по функциям (Python)

1. func_generate_record_id

Генерирует уникальный идентификатор записи на основе входной строки ID, вычисляя количество дней, прошедших с базовой даты (1940-01-01).

def func_generate_record_id(inn: str, shift: int = 0, verbose: bool = False) -> Optional[str]:


Ожидаемый формат inn (действительно для всех реализаций)

Входная строка inn должна быть строго отформатирована следующим образом:

Индекс 0 (1 цифра): Индикатор пола. 1 для женщин, 2 для мужчин.

Индексы 1-8 (8 цифр): Дата рождения в формате DDMMYYYY (ДДММГГГГ).

Индекс 9+ (1 и более цифр): Числовой суффикс/последовательность.

Параметры:

inn (str): Структурированная идентификационная строка.

shift (int, опционально): Дополнительное целое число для прибавления к компоненту суффикса ID. По умолчанию 0.

verbose (bool, опционально): Если True, логические ошибки будут выводиться в консоль. По умолчанию False.

Возвращает:

str: Сгенерированный Record ID в виде строки.

None: Если формат ввода неверен, дата предшествует 1940-01-01 или цифра пола не равна 1 или 2.

2. func_generate_sha_hash

Генерирует безопасный хеш входной строки, строго используя алгоритм SHA-512. К входным данным перед хешированием всегда добавляется фиксированная соль ALGAGROUP (соль + входные_данные).

def func_generate_sha_hash(input_data: str, bit_length: int = 512, salt: str = "ALGAGROUP") -> Optional[str]:


Параметры:

input_data (str): Строка, которую нужно хешировать.

bit_length (int, опционально): Строго 512.

salt (str, опционально): Строго "ALGAGROUP".

Возвращает:

str: Шестнадцатеричный дайджест хеша (SHA-512).

None: Если input_data равно None.

Документация по функциям (Oracle PL/SQL)

1. func_dsp_dsml_generate_record_id

PL/SQL аналог функции генерации Record ID. Логика, вместимость (100 000 ID на пол в день) и базовые сдвиги (v_ag_shift = 1265) полностью идентичны версии на Python.

FUNCTION func_dsp_dsml_generate_record_id(
    p_inn IN VARCHAR2,
    p_shift in number default 0
) RETURN VARCHAR2;


Параметры:

p_inn (VARCHAR2): Структурированная идентификационная строка (формат описан выше).

p_shift (NUMBER, опционально): Дополнительное смещение суффикса. По умолчанию 0.

Возвращает:

VARCHAR2: Сгенерированный Record ID.

NULL: В случае логической ошибки (неверный пол, дата до 1940 года) или ошибки парсинга типов.

2. func_dsml_dsp_sha_algorithm

PL/SQL реализация хеширования. Использует встроенный механизм STANDARD_HASH базы данных Oracle и конвертирует результат в строку шестнадцатеричных символов в нижнем регистре.

FUNCTION func_dsml_dsp_sha_algorithm(
    p_data IN VARCHAR2,
    p_salt IN VARCHAR2 DEFAULT '',
    p_algorithm IN VARCHAR2 DEFAULT 'SHA512'
) RETURN VARCHAR2;


Параметры:

p_data (VARCHAR2): Данные для хеширования (например, Record ID).

p_salt (VARCHAR2, опционально): Соль для конкатенации перед данными. По умолчанию ''.

p_algorithm (VARCHAR2, опционально): Алгоритм хеширования. По умолчанию 'SHA512'.

Возвращает:

VARCHAR2: Хеш в формате hex.

NULL: Если p_data является NULL.

Примеры использования

Пример на Python

from your_module import func_generate_record_id, func_generate_sha_hash

# 1. Определяем входную строку (2 - Мужчина | 21101995 - Дата | 00001 - Суффикс)
inn = "22110199500001" 

# 2. Генерируем Record ID
record_id = func_generate_record_id(inn, verbose=True)
print(f"Generated Record ID: {record_id}")
# Вывод: 4076401266

# 3. Хешируем Record ID (строго SHA-512 и соль 'ALGAGROUP')
hashed_rec_id = func_generate_sha_hash(record_id, bit_length=512, salt='ALGAGROUP')
print(f"SHA-512 Hash: {hashed_rec_id}")
# Вывод: fc82bcf49c1630209a816c668240b4b363ace3bcc1f1f7675bcbe39ef07d1d87e6faf789c5155b424455863d1be9877c867db2a25465dadba3688420e7ab6bd3


Пример на Oracle PL/SQL

Анонимный блок для тестирования вызова обеих функций:

DECLARE
  v_rec_id VARCHAR2(100);
  v_hashed_rec_id VARCHAR2(4000);
BEGIN
  -- 1. Генерируем Record ID
  v_rec_id := func_dsp_dsml_generate_record_id(
      p_inn => '22110199500001'
  );
  
  -- 2. Хешируем полученный ID с солью
  v_hashed_rec_id := func_dsml_dsp_sha_algorithm(
      p_data => v_rec_id,
      p_salt => 'ALGAGROUP'
  );
  
  -- Вывод результатов (требуется SET SERVEROUTPUT ON)
  DBMS_OUTPUT.PUT_LINE('Record ID: ' || v_rec_id);
  DBMS_OUTPUT.PUT_LINE('Hashed ID: ' || v_hashed_rec_id);
END;
/
