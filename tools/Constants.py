STOP_WORDS = [
    "Желаемая должность и зарплата",
    "Опыт работы",
    "Образование",
    "Повышение квалификации, курсы",
    "Ключевые навыки",
    "Опыт вождения",
    "Дополнительная информация",
]

STOP_WORDS_MAPING = {
    "Желаемая должность и зарплата": "position_and_salary",
    "Опыт работы": "work_experience",
    "Образование": "education",
    "Повышение квалификации, курсы": "additional_education",
    "Ключевые навыки": "skill_set",
    "Опыт вождения": "driver_experience",
    "Дополнительная информация": "additional_info",
}

REGEX_FOR_GENDER = r'Мужчина|Женщина'
REGEX_FOR_AGE = r'([0-9]+)\sлет'
REGEX_FOR_BIRTH_YEAR = r'родил.+?\s.+([0-9]{4})'
REGEX_FOR_PHONE = r'\+?[1-9]\s\([0-9]+\)\s[0-9]+'
REGEX_FOR_MAIL = r'\+?[A-z0-9]+@[A-z]+\.[A-z]+'
REGEX_FOR_SITY = r'Проживает:\s([А-я]+)'

LIST_PERSONAL_INFO_REGEX = [REGEX_FOR_GENDER, REGEX_FOR_AGE, REGEX_FOR_BIRTH_YEAR, REGEX_FOR_PHONE, REGEX_FOR_MAIL,
                            REGEX_FOR_SITY]
