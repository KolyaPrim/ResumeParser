# ResumeParser

---

### How use it ?

You can run it from console and throw an argument `path` and `save_path`

```
>python ResumeParser.py -h
options:
  -h, --help                            show this help message and exit
  -p PATH, --path PATH                  Path to file or folder. It is required
  -sp SAVE_PATH, --save_path SAVE_PATH  Path where files wiil be saved. It is not required
```

For example in Windows:

```
(resume_parser) D:\ResumeParser> dir -n results
(resume_parser) D:\ResumeParser> python ResumeParser.py -p '.\files\NameFile.rtf' -sp 'results'
(resume_parser) D:\ResumeParser> dir -n results
NameFile.json
(resume_parser) D:\ResumeParser>

```

Or you can use it as module.

```
>>> from ResumeParser import ResumeParser
>>> parser = ResumeParser(path='files\NameFile.pdf')
>>> json_data = parser.run()
>>> print(json_data)
```

---

### What will be returned ?

This module return a json object or list of json object that look like this:

```json
{
  "personal_info": {
    "name": "Васильев Вася",
    "last_name": "Васильев",
    "first_name": "Вася",
    "gender": "Мужчина",
    "age": "53",
    "birth_year": "1970",
    "phone": "+7 (999) 8883344",
    "mail": "vasilev1970@mymail.com",
    "sity": "Владивосток"
  },
  "position_and_salary": {
    "title": "Программист разработчик",
    "salary": "100500",
    "employments": "полная занятость",
    "schedules": "полный день"
  },
  "education": {
    "Высшее": {
      "2022": {
        "institution": "Наилучший универсистет мира для программистов",
        "description": "Программирование на всех языках мира"
      },
      "2014": {
        "institution": "Колледж для программистов",
        "description": "Языки программирования"
      }
    }
  },
  "additional_education": {
    "2020": {
      "institution": "Курс повышения квалификации javascript разработчика",
      "description": "Как создавать переменные"
    }
  },
  "skill_set": {
    "language": "Русский — Родной\nАнглийский  — A1 — Начальный\n",
    "skills": "Упорство и слабоумие"
  },
  "driver_experience": {
    "driver_license_types": [
      "B"
    ],
    "has_vehicle": True
  },
  "additional_info": {
    "about": "Всё время хочу пить кофе, есть и спать"
  }
}
```

---
Block *`personal_info`*

Field       |  Type  |       What is it mean       | Possible values         |
:---        |:------:|:---------------------------:|-------------------------|
name        | string |          Full name          ||
last_name   | string |          Last name          ||
first_name  | string |         First name          ||
gender      | string |           Gender            | `Мужчина`, `Женщина`    |
age         | string |             Age             |                         |
birth_year  | string |     Just year of birth      ||
phone       | string | Phone number for contact    | `"+7 (999) 8883344"`    |
mail        | string |      Mail for contact       | `podcolz1995@yandex.ru` |
sity        | string |          Full name          |                         |

Block *`position_and_salary`*

Field       |  Type  |   What is it mean   |
:---        |:------:|:-------------------:|
title       | string |  Preferer position  |
salary      | string |   Desired salary    |
employments | string | Possible employment |
schedules   | string |    work schedule    |

Block *`education`* and *`additional_education`*
All keys is level education.
Then level split by year and for each level get `institution` and `description`

Field       |  Type  |                    What is it mean                    |
:---        |:------:|:-----------------------------------------------------:|
institution | string |          Institute or place of education              |
salary      | string | Description of the received education, specialization |

Block *`skill_set`*

Field       |  Type  |    What is it mean    |
:---        |:------:|:---------------------:|
language    | string | Language proficiency  |
salary      | string |    Personal skills    |

Block *`driver_experience`*

Field                   | Type |        What is it mean         |
:---                    |:----:|:------------------------------:|
driver_license_types    | list | List of driver license types   |
has_vehicle             | bool |     Availability of a car      |

Block *`additional_info`*

Field    |  Type  |             What is it mean             |
:---     |:------:|:---------------------------------------:|
about    | string | Description of yourself in any form     |