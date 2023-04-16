import os
import re
from pathlib import Path
from pprint import pprint
from typing import List, Dict, Tuple, Text

from tools import Constants
from tools import ExternalTools as Et

BASE_DIR = Path(__file__).resolve().parent

REGEX_FOR_AGE = r'[0-9]+ лет'


def get_list_year_education(text) -> Tuple[List, List]:
    list_year = re.findall(Constants.REGEX_FOR_YEAR_EDUCATION, text)
    list_year = list(filter(None, list_year))
    list_year_index = [text.index(year) for year in list_year]
    count_years = len(list_year_index)

    list_year_description = []
    for i in range(count_years):
        start_index = list_year_index[i]
        if i == count_years - 1:
            list_year_description.append(text[start_index:])
        else:
            end_index = list_year_index[i + 1]
            list_year_description.append(text[start_index:end_index])

    list_year_description = list(filter(None, list_year_description))
    return list_year, list_year_description


class ResumeParser:
    def __init__(self, path: str, save_path: str = None):
        """
        Initial object ResumeParser.
        :param path: Path to folder or file.
        :param save_path:Path for save file.
        """
        self.path = path
        self.save_path = save_path

    def run(self) -> Dict | List[Tuple[Text, Dict]]:
        if os.path.isdir(self.path):
            filename_list = Et.get_list_files(path=self.path)
            json_list = []
            for file in filename_list:
                file_path = os.path.join(self.path, file)
                text = Et.get_text_from_file(file_path=file_path)
                current_json = self._get_parsed_data(text=text)
                json_list.append((file, current_json))

            if self.save_path:
                for file_name, json_data in json_list:
                    file_name = re.sub('\.[A-z0-9]+', '', file_name) + '.json'
                    path = os.path.join(self.save_path, file_name)
                    Et.save_json(path=path, json_data=json_data)
            return json_list

        elif os.path.isfile(self.path):
            text = Et.get_text_from_file(file_path=self.path)
            json_data = self._get_parsed_data(text=text)

            if self.save_path:
                file_name = re.sub('\.[A-z0-9]+', '', self.path.split('/')[-1]) + '.json'
                path = os.path.join(self.save_path, file_name)
                Et.save_json(path=path, json_data=json_data)

            return json_data

        else:
            raise Exception("It's not a file or folder path")

    @staticmethod
    def _get_blocks(text: str) -> Dict:
        list_block_index: List = []
        for i in Constants.STOP_WORDS:
            if i in text:
                list_block_index.append((i, text.index(i)))

        count_blocks = len(list_block_index)

        dict_with_text = {"personal_info": text[: list_block_index[0][1]]}

        for i in range(count_blocks):
            stop_word, index = list_block_index[i]
            key = Constants.STOP_WORDS_MAPING.get(stop_word)
            start_index = index + len(stop_word)
            if i == count_blocks - 1:
                dict_with_text[key] = text[start_index:]
            else:
                end_index = list_block_index[i + 1][1]
                dict_with_text[key] = text[start_index:end_index]

        return dict_with_text

    @staticmethod
    def _get_personal_info(text) -> Dict:
        personal_info_dict = {}

        text_rows = [row for row in text.split('\n') if len(row) > 0]

        name = text_rows[0]
        personal_info_dict['name'] = name

        list_tag_name = ['last_name', 'first_name', 'middle_name']
        list_keys = ['gender', 'age', 'birth_year', 'phone', 'mail', 'sity']

        for index, word in enumerate(name.split(' ')):
            personal_info_dict[list_tag_name[index]] = word

        for index, key in enumerate(list_keys):
            try:
                personal_info_dict[key] = re.findall(Constants.LIST_PERSONAL_INFO_REGEX[index], text)[0]
            except:
                pass

        return personal_info_dict

    @staticmethod
    def _get_position_and_salary(text) -> Dict:

        position_and_salary_dict = {}

        list_keys = ['title', 'salary', 'employments', 'schedules']

        for index, key in enumerate(list_keys):
            try:
                position_and_salary_dict[key] = re.findall(Constants.LIST_POSITION_AND_SALARY_REGEX[index], text)[0]
            except:
                pass
        return position_and_salary_dict

    @staticmethod
    def _get_work_experience(text) -> Dict:
        work_experience_dict = {}
        text
        list_keys = ['total_experience']
        for index, key in enumerate(list_keys):
            try:
                work_experience_dict[key] = re.findall(Constants.LIST_WORK_EXPERIENCE_REGEX[index], text)[0]
            except:
                pass
        text = re.sub(r'[——](.+)\n', '', text).strip()

        job_period_list = re.findall(Constants.REGEX_FOR_JOB_EXPERIENCE, text)
        job_experience_list = re.split(Constants.REGEX_FOR_JOB_EXPERIENCE, text)
        job_experience_list = list(filter(None, job_experience_list))
        job_experience = {}

        for index, job in enumerate(job_experience_list):
            time_period = re.findall(Constants.REGEX_FOR_JOB_PERIOD, job)[0]

            start_index_job_about = text.index(time_period) + len(time_period)
            job_about = text[start_index_job_about:].split('\n')
            job_about = list(filter(None, job_about))

            firm_name = job_about[0]
            position = job_about[1]
            description = ' '.join(job_about[2:])

            job_experience[firm_name] = {
                'period': job_period_list[index].replace('\n', ''),
                'time': time_period,
                'position': position,
                'description': description
            }
        work_experience_dict['job_experience'] = job_experience
        return work_experience_dict

    @staticmethod
    def _get_education(text) -> Dict:
        education_dict = {}

        list_level_education = re.findall(Constants.REGEX_FOR_LEVEL_EDUCATION, text)
        list_education = re.split(Constants.REGEX_FOR_LEVEL_EDUCATION, text)
        list_education = list(filter(None, list_education))

        for index, description in enumerate(list_education):
            description = description.strip()

            list_year, list_year_description = get_list_year_education(text=description)

            education_dict[list_level_education[index]] = {}
            for index_year, description_year in enumerate(list_year_description):
                education_dict[list_level_education[index]].update({list_year[index_year]: {
                    'institution': re.match(Constants.REGEX_FOR_DESCRIPTION_EDUCATION, description_year).group(1),
                    'description': re.match(Constants.REGEX_FOR_DESCRIPTION_EDUCATION, description_year).group(3)
                }})

        return education_dict

    @staticmethod
    def _get_additional_education(text) -> Dict:
        additional_education_dict = {}

        text = text.strip()

        list_year, list_year_description = get_list_year_education(text=text)

        for index_year, description_year in enumerate(list_year_description):
            additional_education_dict[list_year[index_year]] = {
                'institution': re.match(Constants.REGEX_FOR_DESCRIPTION_EDUCATION, description_year).group(1),
                'description': re.match(Constants.REGEX_FOR_DESCRIPTION_EDUCATION, description_year).group(3)
            }

        return additional_education_dict

    @staticmethod
    def _get_skill_set(text) -> Dict:
        skill_set_dict = {}

        list_keys = ['language', 'skills']

        for index, key in enumerate(list_keys):
            try:
                skill_set_dict[key] = re.findall(Constants.LIST_SKILL_SET_REGEX[index], text)[0]
            except:
                pass

        return skill_set_dict

    @staticmethod
    def _get_driver_experience(text) -> Dict:
        driver_experience_dict = {}

        driver_license_types = re.findall(Constants.REGEX_FOR_DRIVE_LICENSE_TYPES, text)[0]
        driver_experience_dict['driver_license_types'] = driver_license_types.strip().split(',')

        driver_experience_dict['has_vehicle'] = bool(re.match(Constants.REGEX_FOR_DRIVE_VEHICLE, text))

        return driver_experience_dict

    @staticmethod
    def _get_additional_info(text) -> Dict:
        additional_info_dict = {
            'about': re.match(Constants.REGEX_FOR_ADDITIONAL_INFO, text).group(1).strip()
        }

        return additional_info_dict

    def _run_parse_text(self, field, text) -> Dict:
        text = text.strip()
        match field:
            case 'personal_info':
                return self._get_personal_info(text=text)
            case 'position_and_salary':
                return self._get_position_and_salary(text=text)
            case 'work_experience':
                return self._get_work_experience(text=text)
            case 'education':
                return self._get_education(text=text)
            case 'additional_education':
                return self._get_additional_education(text=text)
            case 'skill_set':
                return self._get_skill_set(text=text)
            case 'driver_experience':
                return self._get_driver_experience(text=text)
            case 'additional_info':
                return self._get_additional_info(text=text)

    def _get_parsed_data(self, text: str) -> Dict:
        block_text = self._get_blocks(text=text)

        json_data = {}
        for key, value in block_text.items():
            json_data[key] = self._run_parse_text(field=key, text=value)

        return json_data


parser = ResumeParser(path="fastfile", save_path="results")
parsed_json = parser.run()
# pprint(parsed_json)
