import os
import re
from pathlib import Path
from pprint import pprint
from typing import List, Dict, Tuple, Text

from tools import Constants
from tools import ExternalTools as Et

BASE_DIR = Path(__file__).resolve().parent

REGEX_FOR_AGE = r'[0-9]+ лет'


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
                    path = os.path.join(self.save_path, file_name)
                    Et.save_json(path=path, json_data=str(json_data))
            return json_list

        elif os.path.isfile(self.path):
            text = Et.get_text_from_file(file_path=self.path)
            json_data = self._get_parsed_data(text=text)

            if self.save_path:
                path = os.path.join(self.save_path, self.path.split('/')[-1])
                Et.save_json(path=path, json_data=str(json_data))

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
                work_experience_dict[key] = re.findall(Constants.LIST_POSITION_AND_SALARY_REGEX[index], text)[0]
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
                'description': description,
            }
        work_experience_dict['job_experience'] = job_experience
        return work_experience_dict

    @staticmethod
    def _get_education(text) -> Dict:
        education_dict = {}
        return education_dict

    @staticmethod
    def _get_additional_education(text) -> Dict:
        additional_education_dict = {}
        return additional_education_dict

    @staticmethod
    def _get_skill_set(text) -> Dict:
        skill_set_dict = {}
        return skill_set_dict

    @staticmethod
    def _get_driver_experience(text) -> Dict:
        driver_experience_dict = {}
        return driver_experience_dict

    @staticmethod
    def _get_additional_info(text) -> Dict:
        additional_info_dict = {}
        return additional_info_dict

    def _run_parse_text(self, field, text) -> Dict:
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
