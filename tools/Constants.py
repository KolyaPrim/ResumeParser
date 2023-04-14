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

REGEX_FOR_END_PAGE = r'(\n|\s)Резюме обновлено\s.+'

REGEX_FOR_GENDER = r"Мужчина|Женщина"
REGEX_FOR_AGE = r"([0-9]+)\sлет"
REGEX_FOR_BIRTH_YEAR = r"родил.+?\s.+([0-9]{4})"
REGEX_FOR_PHONE = r"\+?[1-9]\s\([0-9]+\)\s[0-9]+"
REGEX_FOR_MAIL = r"\+?[A-z0-9]+@[A-z]+\.[A-z]+"
REGEX_FOR_SITY = r"Проживает:\s([А-я]+)"

LIST_PERSONAL_INFO_REGEX = [
    REGEX_FOR_GENDER,
    REGEX_FOR_AGE,
    REGEX_FOR_BIRTH_YEAR,
    REGEX_FOR_PHONE,
    REGEX_FOR_MAIL,
    REGEX_FOR_SITY,
]

REGEX_FOR_TITLE = r".+"
REGEX_FOR_SALARY = r"([0-9]+\s[0-9]+)\sруб"
REGEX_FOR_EMPLOYMENTS = r"Занятость:\s([А-я\s]+)\n"
REGEX_FOR_SCHEDULES = r"График\sработы:\s([А-я\s]+)\n"

LIST_POSITION_AND_SALARY_REGEX = [
    REGEX_FOR_TITLE,
    REGEX_FOR_SALARY,
    REGEX_FOR_EMPLOYMENTS,
    REGEX_FOR_SCHEDULES,
]

REGEX_FOR_TOTAL_EXPERIENCE = r"[——](.+)"
REGEX_FOR_JOB_EXPERIENCE = (
    r"[А-я]+\s[0-9]{4}\s\—\s[А-я]+\s[0-9]{4}"
    r"|[А-я]+\s[0-9]{4}\s\—\sнастоящее\sвремя"
    r"|[А-я]+\s[0-9]{4}\s"
)
REGEX_FOR_FIRM_NAME = (
    r"[0-9]+\sгода\s[0-9]+\sмесяца([А-я\s]+\n?)"
    r"|[0-9]+\sгода\s[0-9]+\sмесяцев([А-я\s]+\n?)"
    r"|[0-9]+\sлет\s[0-9]+\sмесяцев([А-я\s]+\n?)"
    r"|[0-9]+\sлет\s[0-9]+\sмесяца([А-я\s]+\n?)"
    r"|[0-9]+\sлет([А-я\s]+\n?)"
    r"|[0-9]+\sгода([А-я\s]+\n?) "
)
REGEX_FOR_JOB_PERIOD = (
    r"[0-9]+\sгода\s[0-9]+\sмесяца"
    r"|[0-9]+\sгода\s[0-9]+\sмесяцев"
    r"|[0-9]+\sлет\s[0-9]+\sмесяцев"
    r"|[0-9]+\sлет\s[0-9]+\sмесяца"
    r"|[0-9]+\sлет"
    r"|[0-9]+\sгода "
)

LIST_WORK_EXPERIENCE_REGEX = [REGEX_FOR_TOTAL_EXPERIENCE]

REGEX_FOR_LEVEL_EDUCATION = r"Среднее\sспециальное" \
                            r"|Среднее\sпрофессиональное" \
                            r"|Основное\sобщее" \
                            r"|Среднее" \
                            r"|Высшее|" \
                            r"Cреднее\sобщее"
REGEX_FOR_YEAR_EDUCATION = r"[0-9]{4}"
REGEX_FOR_DESCRIPTION_EDUCATION = r"[0-9]{4}\s([А-я\s\-«»\"]+)(\,|\n)([А-я\s\,]+)"
