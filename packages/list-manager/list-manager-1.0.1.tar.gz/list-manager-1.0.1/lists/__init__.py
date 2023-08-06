__VERSION__ = "1.0.1"

from lists.list_manager import ListManager
import argparse


def parse_args():  # pragma: no cover
    parser = argparse.ArgumentParser(description="")
    subparsers = parser.add_subparsers(dest="action")

    get_lists = subparsers.add_parser(
        "get_lists", help="Returns All List Names"
    )

    add_item = subparsers.add_parser("add_item", help="Add Item To A List")
    add_item.add_argument(
        "-l",
        "--list",
        help="The List That The Item Is Being Added To",
        action="store",
        type=str,
        required=True,
    )
    add_item.add_argument(
        "-i",
        "--item",
        help="The Item Being Added To The List",
        action="store",
        type=str,
        required=True,
    )

    get_list = subparsers.add_parser(
        "get_list", help="Returns A List And All Included Items",
    )
    get_list.add_argument(
        "-l",
        "--list",
        help="The Name Of The List Being Requested",
        action="store",
        type=str,
        required=True,
    )

    create_list = subparsers.add_parser("create_list", help="Create New List",)
    create_list.add_argument(
        "-l",
        "--list",
        help="The Name Of The List Being Created",
        action="store",
        type=str,
        required=True,
    )
    create_list.add_argument(
        "-i",
        "--item",
        help="An Item To Instantiate The List",
        action="store",
        type=str,
    )

    delete_item_from_list = subparsers.add_parser(
        "delete_item", help="Delete Item From List",
    )
    delete_item_from_list.add_argument(
        "-l",
        "--list",
        help="The Name Of The List Where The Item Is Being Deleted",
        action="store",
        type=str,
        required=True,
    )
    delete_item_from_list.add_argument(
        "-i",
        "--item",
        help="The Name Of The Item Being Deleted",
        action="store",
        type=str,
        required=True,
    )

    delete_list = subparsers.add_parser("delete_list", help="Delete List",)
    delete_list.add_argument(
        "-l",
        "--list",
        help="The Name Of The List Being Deleted",
        action="store",
        type=str,
        required=True,
    )

    return parser.parse_args()


def get_lists(args):  # pragma: no cover
    lists_manager = ListManager()
    lists = lists_manager.get_lists()
    print("Lists:")
    for list_name in lists:
        print(list_name)
    print("\n")


def get_list(args):  # pragma: no cover
    lists_manager = ListManager()
    list_name = lists_manager.get_list(args.list)
    if list_name is not None:
        print(args.list)
        for item in list_name:
            print(item)
    else:
        print(f"{args.list} Does Not Exist")
    print("\n")


def create_list(args):  # pragma: no cover
    lists_manager = ListManager()
    create_list_response = lists_manager.create_list(
        list_name=args.list, item=args.item
    )
    if create_list_response is True:
        print(f"{args.list} Was Successfully Created")
    else:
        print(f"{args.list} Already Exists")
    print("\n")


def add_item(args):  # pragma: no cover
    lists_manager = ListManager()
    add_item_response = lists_manager.add_to_list(
        list_name=args.list, item=args.item
    )
    if add_item_response is True:
        print(f"{args.item} Was Successfully Added To {args.list}")
    else:
        print(f"{args.list} Does Not Exist")
    print("\n")


def delete_item(args):  # pragma: no cover
    lists_manager = ListManager()
    delete_item_response = lists_manager.delete_from_list(
        list_name=args.list, item=args.item
    )
    if delete_item_response is True:
        print(f"{args.item} Was Successfully Deleted From {args.list}")
    else:
        print(
            f"{args.item} Could Not Be Deleted. Please Check That {args.list} "
            f"and {args.item} Exists In It"
        )


def delete_list(args):  # pragma: no cover
    lists_manager = ListManager()
    delete_list_response = lists_manager.delete_list(list_name=args.list)
    if delete_list_response is True:
        print(f"{args.list} Was Successfully Deleted")
    else:
        print(f"{args.list} Does Not Exists")


function_to_function = {
    "get_lists": get_lists,
    "get_list": get_list,
    "create_list": create_list,
    "add_item": add_item,
    "delete_item": delete_item,
    "delete_list": delete_list,
}


def main():  # pragma: no cover
    args = parse_args()
    function_to_function[args.action](args)
