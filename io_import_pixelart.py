# coding: UTF-8

bl_info = {
	"name": "Import Pixel Art",
	"author": "Mathias Panzenböck",
	"version": (1, 0, 0),
	"blender": (2, 76, 0),
	"location": "File > Import > Pixel Art",
	"description": "Imports pixel art images, creating colored cubes for each pixel.",
	"category": "Import-Export"
}

import os.path
import bpy

def read_pixel_art(context, filepath):
	filename = os.path.split(filepath)[1]
	image = bpy.data.images.load(filepath)

	try:
		channels = image.channels
		if channels not in (1, 3, 4):
			raise Exception("cannot handle number of channels in image")

		layers = bpy.context.scene.layers
		parent = bpy.data.objects.new(name=filename, object_data=None)
		parent.layers = layers
		bpy.context.scene.objects.link(parent)

		width, height = image.size
		pixels = image.pixels
		a = 1.0
		for y in range(height):
			offset = y * channels * width
			for x in range(width):
				if channels == 1:
					r = g = b = image.pixels[offset + x]
				elif channels == 3:
					index = offset + x * channels
					r = pixels[index]
					g = pixels[index + 1]
					b = pixels[index + 2]
				else:
					index = offset + x * channels
					r = pixels[index]
					g = pixels[index + 1]
					b = pixels[index + 2]
					a = pixels[index + 3]

				if a == 0:
					continue

				name = 'pixel_art_%d_%d_%d_%d' % (int(r * 255), int(g * 255), int(b * 255), int(a * 255))
				if name in bpy.data.materials:
					material = bpy.data.materials[name]
				else:
					material = bpy.data.materials.new(name=name)
					material.diffuse_color = (r, g, b)
					material.alpha = a

				object_name = '%s_%d_%d' % (filename, x, y)
				mesh = bpy.data.meshes.new(object_name+'_mesh')
				mesh.from_pydata([
					(0, 0, 0), # 0
					(1, 0, 0), # 1
					(1, 1, 0), # 2
					(0, 1, 0), # 3
					(0, 0, 1), # 4
					(1, 0, 1), # 5
					(1, 1, 1), # 6
					(0, 1, 1)  # 7
				], [], [
					(0, 1, 2, 3),
					(0, 1, 5, 4),
					(1, 2, 6, 5),
					(4, 5, 6, 7),
					(2, 3, 7, 6),
					(0, 3, 7, 4)
				])
				mesh.materials.append(material)
				mesh.update()
				obj = bpy.data.objects.new(name=object_name, object_data=mesh)
				obj.layers = layers
				obj.location = (x, y, 0)
				obj.parent = parent
				bpy.context.scene.objects.link(obj)


	finally:
		#bpy.data.images.remove(image)
		pass

	return {'FINISHED'}


# ImportHelper is a helper class, defines filename and
# invoke() function which calls the file selector.
from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator


class ImportPixelArt(Operator, ImportHelper):
	"""Imports pixel art images, creating colored cubes for each pixel."""
	bl_idname = "import_image.pixel_art"
	bl_label = "Import Pixel Art"

	# ImportHelper mixin class uses this
	filename_ext = ".png"

	filter_glob = StringProperty(
			default="*.png",
			options={'HIDDEN'})

	def execute(self, context):
		return read_pixel_art(context, self.filepath)


# Only needed if you want to add into a dynamic menu
def menu_func_import(self, context):
	self.layout.operator(ImportPixelArt.bl_idname, text="Import Pixel Art")


def register():
	bpy.utils.register_class(ImportPixelArt)
	bpy.types.INFO_MT_file_import.append(menu_func_import)


def unregister():
	bpy.utils.unregister_class(ImportPixelArt)
	bpy.types.INFO_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
	register()
