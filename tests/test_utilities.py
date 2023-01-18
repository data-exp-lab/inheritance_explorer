from inheritance_explorer import _testing as iet


def test_test_class():
    for clss in [
        iet.ClassForTesting,
        iet.ClassForTesting3,
        iet.ClassForTesting4,
        iet.ClassForTesting2,
    ]:
        class_inst = clss()
        _ = class_inst.use_this_func(1)
