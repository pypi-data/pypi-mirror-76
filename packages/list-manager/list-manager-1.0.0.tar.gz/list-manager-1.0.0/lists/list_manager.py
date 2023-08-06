from os.path import (
    join as os_path_join,
    exists as os_path_exists,
    expanduser as os_path_expanduser,
)
from json import load as json_load, dump as json_dump


class ListManager:
    def __init__(self):
        self.file_name = os_path_join(os_path_expanduser("~"), ".list_manager")
        if not os_path_exists(self.file_name):
            self.lists = {}
        else:
            with open(self.file_name, "r") as json_input_file:
                json_output = json_load(json_input_file)
                self.lists = json_output.get("lists")

    def get_lists(self):
        return [list_name for list_name in self.lists]

    def get_list(self, list_name):
        if list_name in self.lists:
            return self.lists.get(list_name)
        else:
            return None

    def create_list(self, list_name, item=None):
        if list_name in self.lists:
            return False
        else:
            if item is not None:
                self.lists[list_name] = [item]
            else:
                self.lists[list_name] = []
        self.export_list_to_file()
        return True

    def delete_list(self, list_name):
        if list_name in self.lists:
            self.lists.pop(list_name)
        else:
            return False
        self.export_list_to_file()
        return True

    def add_to_list(self, list_name, item):
        if list_name in self.lists:
            if item not in self.lists.get(list_name):
                self.lists[list_name].append(item)
        else:
            return False
        self.export_list_to_file()
        return True

    def delete_from_list(self, list_name, item):
        if list_name in self.lists:
            if item in self.lists.get(list_name):
                self.lists.get(list_name).remove(item)
            else:
                return False
        else:
            return False
        self.export_list_to_file()
        return True

    def export_list_to_file(self):
        json_output = {"lists": self.lists}
        with open(self.file_name, "w") as json_output_file:
            json_dump(json_output, json_output_file)
