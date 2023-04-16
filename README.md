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
    "name": "�������� ����",
    "last_name": "��������",
    "first_name": "����",
    "gender": "�������",
    "age": "53",
    "birth_year": "1970",
    "phone": "+7 (999) 8883344",
    "mail": "vasilev1970@mymail.com",
    "sity": "�����������"
  },
  "position_and_salary": {
    "title": "����������� �����������",
    "salary": "100500",
    "employments": "������ ���������",
    "schedules": "������ ����"
  },
  "education": {
    "������": {
      "2022": {
        "institution": "��������� ������������ ���� ��� �������������",
        "description": "���������������� �� ���� ������ ����"
      },
      "2014": {
        "institution": "������� ��� �������������",
        "description": "����� ����������������"
      }
    }
  },
  "additional_education": {
    "2020": {
      "institution": "���� ��������� ������������ javascript ������������",
      "description": "��� ��������� ����������"
    }
  },
  "skill_set": {
    "language": "������� � ������\n����������  � A1 � ���������\n",
    "skills": "�������� � ���������"
  },
  "driver_experience": {
    "driver_license_types": [
      "B"
    ],
    "has_vehicle": True
  },
  "additional_info": {
    "about": "�� ����� ���� ���� ����, ���� � �����"
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
gender      | string |           Gender            | `�������`, `�������`    |
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