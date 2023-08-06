from lists.list_manager import ListManager
from os.path import (
    join as os_path_join,
    exists as os_path_exists,
    expanduser as os_path_expanduser,
)
from os import remove as os_remove
from json import load as json_load, dump as json_dump


class TestListManager:
    def setup_class(self):
        self.file_name = os_path_join(os_path_expanduser("~"), ".list_manager")
        if os_path_exists(self.file_name):
            self.requires_cleanup = True
            with open(self.file_name, "r") as json_input_file:
                self.stored_lists = json_load(json_input_file)
        else:
            self.requires_cleanup = False

    def teardown_class(self):
        if self.requires_cleanup is True:
            with open(self.file_name, "w") as json_output_file:
                json_dump(self.stored_lists, json_output_file)

    def setup_method(self):
        if os_path_exists(self.file_name):
            os_remove(self.file_name)
        self.list_manager = ListManager()
        self.initial_lists = {"list_a": ["item_a", "item_b"], "list_b": "item_c"}
        self.list_manager.lists = self.initial_lists
        self.list_manager.export_list_to_file()

    def test_init_list_manager_without_file(self):
        assert self.list_manager.lists == self.initial_lists

    def test_init_list_manager_with_file(self):
        new_list_manager = ListManager()
        assert new_list_manager.lists == self.list_manager.lists

    def test_get_lists(self):
        assert self.list_manager.get_lists() == ["list_a", "list_b"]

    def test_get_list_where_list_exists(self):
        assert self.list_manager.get_list("list_a") == self.initial_lists.get("list_a")

    def test_get_list_where_list_does_not_exist(self):
        assert self.list_manager.get_list("list_c") is None

    def test_create_list_where_list_does_not_exist(self):
        assert self.list_manager.create_list(list_name="list_c") is True
        assert "list_c" in self.list_manager.lists

    def test_create_list_where_list_does_not_exist_with_initial_item(self):
        assert self.list_manager.create_list(list_name="list_c", item="item_d") is True
        assert "list_c" in self.list_manager.lists
        assert "item_d" in self.list_manager.lists.get("list_c")

    def test_create_list_where_list_exists(self):
        assert self.list_manager.create_list(list_name="list_a") is False

    def test_delete_list_where_list_exists(self):
        assert self.list_manager.delete_list(list_name="list_a") is True
        assert "list_a" not in self.list_manager.lists

    def test_delete_list_where_list_does_not_exist(self):
        assert self.list_manager.delete_list(list_name="list_c") is False
        assert self.list_manager.lists == self.initial_lists

    def test_add_item_where_list_exists(self):
        assert self.list_manager.add_to_list(list_name="list_a", item="item_d") is True
        assert "item_d" in self.list_manager.lists.get("list_a")

    def test_add_item_where_list_does_not_exist(self):
        assert self.list_manager.add_to_list(list_name="list_c", item="item_d") is False
        assert "list_c" not in self.list_manager.lists

    def test_delete_item_where_list_exists(self):
        assert self.list_manager.delete_from_list(list_name="list_a", item="item_a") is True
        assert "item_a" not in self.list_manager.lists.get("list_a")

    def test_delete_item_where_list_does_not_exist(self):
        assert self.list_manager.delete_from_list(list_name="list_c", item="item_a") is False
        assert self.list_manager.lists == self.initial_lists

    def test_delete_item_where_list_exists_but_item_does_not(self):
        assert self.list_manager.delete_from_list(list_name="list_a", item="item_d") is False
        assert self.list_manager.lists == self.initial_lists
