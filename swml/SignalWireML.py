import yaml
from typing import Dict, Union
from .Sections import Section
import json

SUPPORTED_FORMATS = ['json', 'yaml']


class CustomDumper(yaml.Dumper):
    pass


def represent_str(dumper, data):
    # Check if the string contains newlines
    if '\n' in data:
        # Use block literal style for multiline strings
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')

    else:
        # Use plain style for other strings
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style=None)


CustomDumper.add_representer(str, represent_str)


class SignalWireML:
    def __init__(self):
        # a dictionary of sections containing a list of _actions (instructions) for each section
        self._sections: Dict[str, Section] = {}

    def __repr__(self):
        # This is the string representation of the object
        return self.generate_swml(data_format='yaml')

    def add_section(self, new_section: Union[str, Section]):

        # if section being added is an instance of Section, add it to the dictionary

        if isinstance(new_section, Section):
            if new_section.name in self._sections:
                raise ValueError(f"Section with name '{new_section.name}' already exists.")
            self._sections[new_section.name] = new_section
            return new_section

        # if a section name str is passed, create a new section and add it to the dictionary
        elif isinstance(new_section, str):
            if new_section in self._sections:
                raise ValueError(f"Section with name '{new_section}' already exists.")
            section = Section(name=new_section)
            self._sections[section.name] = section
            return section
        else:
            raise ValueError(f"Invalid section type '{type(new_section)}'. Valid types are 'str' and 'Section'.")

    def serialize_sections(self):
        # Iterate through the sections and get their actions
        return {section.name: section._actions for section in self._sections.values()}

    def generate_swml(self, data_format: str = 'json'):
        if not self._sections:
            raise ValueError("No sections found. Please add at least one section to the SignalWireML object.")

        if data_format not in SUPPORTED_FORMATS:
            raise ValueError(f"Invalid data format '{data_format}'. Valid formats are 'json' and 'yaml'.")

        # Use the serialize_sections method to get serialized sections
        serialized_sections = self.serialize_sections()

        if data_format == 'json':
            return json.dumps({'sections': serialized_sections})
        elif data_format == 'yaml':
            return yaml.dump({'sections': serialized_sections}, Dumper=CustomDumper, sort_keys=False, indent=2)
