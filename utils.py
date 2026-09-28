def is_assembly(obj):
    return obj.TypeId == 'Assembly::AssemblyObject'

def is_fusion(obj):
    if obj.TypeId == "Part::MultiFuse":
        shape = obj.Shape
        if shape is not None and (shape.ShapeType == "Compound" or shape.isValid() and len(shape.Faces) > 0):
            return True
    return False


def is_part(obj):
    return obj.TypeId == "App::Part"


def is_group(obj):
    return obj.TypeId == "App::DocumentObjectGroup"


def is_frameforge_container(obj):
    if obj.TypeId == "Part::FeaturePython":
        if hasattr(obj, "Sketchs") and hasattr(obj, "Elements") and hasattr(obj, "Infos"):
            return True
    return False


def is_variant(obj):
    if obj.TypeId == "Part::FeaturePython":
        if hasattr(obj, "Source") and hasattr(obj, "Enable"):
            return True
    return False


def is_part_or_part_design(obj):
    return obj.TypeId.startswith(("Part::", "PartDesign::")) and obj.TypeId != "Part::FeaturePython"

def is_plume_item(obj):
    return hasattr(obj, "PlumeIPN") or hasattr(get_link(obj), "PlumeIPN")

    
def is_fastener(obj):
    return obj.TypeId == "Part::FeaturePython" and hasattr(obj, "Invert") and hasattr(obj, "Type") and obj.Type != ""



def get_plm_obj_attr(obj, src, attr, default=None):
    if default is None:
        return getattr(obj, attr, getattr(src, attr))
    else:
        return getattr(obj, attr, getattr(src, attr, default))


def get_fastener_name(obj):
    if not is_fastener(obj):
        return "Unknown"

    fastener_type = obj.Type
    dia = getattr(obj, "Diameter", "")
    material = get_material_name(obj)
    length = getattr(obj, 'Length', '') if getattr(obj, 'Length', '') != "Custom" else str(getattr(obj, 'LengthCustom', '')).replace(" mm", "")
    name = ''.join([char for char in obj.Name if not char.isdigit()])

    output = f"{name}_{fastener_type}_{dia}"
    if length != "":
        output += f"_{length}"
    if material != "":
            output += f"_{material}"

    return output

def get_link(obj, recursive=False):
    if obj.TypeId == "App::Link":
        return get_link(obj.LinkedObject) if recursive else obj.LinkedObject
    return obj


def get_material_name(obj):
    """
    return obj.ShapeMaterial.Name
    """
    return obj.ShapeMaterial.Name

