from typing import Any, List


def load_subclasses_from_module(module: object, parent_class: type) -> List[Any]:
    """Return a list of subclasses of parent_class in module"""
    subclasses = []
    for cls_name, cls_obj in vars(module).items():
        if (
            isinstance(cls_obj, type)
            and issubclass(cls_obj, parent_class)
            and cls_obj is not parent_class
        ):
            subclasses.append(cls_obj)
    return subclasses
