import unittest

import bpy

from . import common
from . import compatibility as compat


class TestMirrorUV(common.TestBase):
    module_name = "mirror_uv"
    idname = [
        # Mirror UV
        ('OPERATOR', 'uv.muv_mirror_uv'),
    ]

    def setUpEachMethod(self):
        obj_name = "Cube"

        common.select_object_only(obj_name)
        compat.set_active_object(bpy.data.objects[obj_name])
        bpy.ops.object.mode_set(mode='EDIT')

    def test_ng_no_uv(self):
        # Warning: Object must have more than one UV map
        print("[TEST] (NG) No UV")
        bpy.ops.mesh.select_all(action='SELECT')
        result = bpy.ops.uv.muv_mirror_uv()
        self.assertSetEqual(result, {'CANCELLED'})

    def test_ok_default(self):
        print("[TEST] (OK) Default")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_mirror_uv()
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified_1(self):
        print("[TEST] (OK) User specified 1")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_mirror_uv(axis='Y', error=0.7, origin='GLOBAL')
        self.assertSetEqual(result, {'FINISHED'})

    def test_ok_user_specified_2(self):
        print("[TEST] (OK) User specified 2")
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.uv_texture_add()
        result = bpy.ops.uv.muv_mirror_uv(axis='Y', error=19.4, origin='WORLD')
        self.assertSetEqual(result, {'FINISHED'})

    @unittest.skipIf(compat.check_version(2, 80, 0) < 0,
                     "Not supported in <2.80")
    def test_ok_multiple_objects(self):
        print("[TEST] (OK) Multiple Objects")

        # Duplicate object.
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_names = ["Cube", "Cube.001"]
        common.select_object_only(obj_names[0])
        common.duplicate_object_without_uv()

        for name in obj_names:
            bpy.ops.object.mode_set(mode='OBJECT')
            common.select_object_only(name)
            compat.set_active_object(bpy.data.objects[name])
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.uv_texture_add()
            bpy.ops.mesh.select_all(action='SELECT')

        # Select two objects.
        bpy.ops.object.mode_set(mode='OBJECT')
        compat.set_active_object(bpy.data.objects[obj_names[0]])
        common.select_objects_only(obj_names)
        bpy.ops.object.mode_set(mode='EDIT')

        result = bpy.ops.uv.muv_mirror_uv(axis='Y', error=19.4, origin='GLOBAL')
        self.assertSetEqual(result, {'FINISHED'})
