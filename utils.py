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
    return obj.TypeId.startswith(("Part::", "PartDesign::"))


