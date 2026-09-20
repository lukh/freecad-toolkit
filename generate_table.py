from collections import defaultdict
import FreeCAD as App
import FreeCADGui as Gui

from itertools import groupby
from collections import defaultdict

from .utils import *



def make_table(grouped_objects, attributes, funcs={}):
    """

    return a data list in a form of [row1, row2] with rows = (c0, c1, ...)
    
    It checks if attributes exists for the link, then for the obj
    It will join the set of data by default, so in a group, IDs will give "1,2,3" if differents, or "2" if same (not "2,2,2)

    the #attribute will apply a function from func.
    the .attribute is the default, trying to getattr to the link and the obj
    
    the + in front of an item will sum instead of joining

    grouped_objects = [(key, [(obj, lnk), (obj, lnk), ...]), ...]
    attributes  = [
        "#parent",
        ".PID",
        "#family",
        ".SizeName",
        ".Length",
        ".CuttingAngleA",
        ".CuttingAngleB",
        ".Cutout",
        "#count",
        ".Material",
        "+.ApproxWeight",
        ".Label"
    ]
    """

    # t = obj, lnks, attr = "Attribute"
    # make_get_std_attr = lambda a : lambda o, l : getattr(l, a, getattr(o, a, "?"))
    def format_value(value, fmt=None):
        if fmt is None:
            return str(value)

        if isinstance(value, App.Units.Quantity):
            return value.UserString

        return format(value, fmt)

    def make_get_std_attr(spec):
        if ":" in spec:
            attr, fmt = spec.split(":", 1)
        else:
            attr = spec
            fmt = None

        def get_attr(o, l):
            value = getattr(l, attr, getattr(o, attr, "N/A"))

            if value == "N/A":
                return value

            return format_value(value, fmt)

        return get_attr

    # build the list of functions that will work on each group of item
    header_functions = []
    for attr in attributes:
        make_group_func = lambda f : lambda l : ", ".join(list(set([str(f(*i)) for i in l])))
        if attr.startswith('+'):
            attr = attr[1:]
            make_group_func = lambda f : lambda l : sum([f(*i) for i in l])

        if attr.startswith('#'):
            f = funcs[attr[1:]]
        elif attr.startswith('.'):
            f = make_get_std_attr(attr[1:])
        else:
            raise ValueError(f'Unknow prefix, must be . or # : {attr}')
        
        header_functions.append(make_group_func(f))


    data = []
    for key, objects in grouped_objects:
        row = [hf(objects) for hf in header_functions]
        data.append(row)

    for row in data:
        print(data)

    return data