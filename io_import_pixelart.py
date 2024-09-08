# coding: UTF-8
#
#    Import pixel art as colored cubes or squares for each pixel
#    Copyright (C) 2016-2024  Mathias Panzenböck
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

bl_info = {
	"name": "Import Pixel Art",
	"author": "Mathias Panzenböck",
	"version": (1,  2, 0),
	"blender": (2, 80, 0),
	"location": "File > Import > Pixel Art",
	"description": "Imports pixel art images, creating colored cubes or squares for each pixel.",
	"doc_url": "https://github.com/panzi/blender-addon-import-pixelart/blob/master/README.md",
	"tracker_url": "https://github.com/panzi/blender-addon-import-pixelart/issues",
	"category": "Import-Export"
}

from array import array
from time import perf_counter
from math import nan
import os.path
import bpy

from bpy_extras.io_utils import ImportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator

PARENT_NAME = '{filename}'
MATERIAL_NAME = 'pixel_art_{color}'
CUBE_NAME = '{filename}_{x}_{y}'
MESH_NAME = '{filename}_{x}_{y}_mesh'

def read_pixel_art(context,
		filepath: str,
		import_as: str = 'CUBES',
		use_nodes: bool = True,
		reuse_materials: bool = False,
		material_name: str = MATERIAL_NAME,
		cube_name: str = CUBE_NAME,
		mesh_name: str = MESH_NAME,
		parent_name: str = PARENT_NAME,
		auto_scale: bool = False):

	timestamp = perf_counter()

	struse_nodes = 'nodes' if use_nodes else ''
	filename = os.path.split(filepath)[1]

	# reduce property lookups in loop:
	bpy_data_materials     = bpy.data.materials
	bpy_data_materials_get = bpy_data_materials.get
	bpy_data_materials_new = bpy_data_materials.new
	bpy_data_objects_new   = bpy.data.objects.new
	bpy_data_meshes_new    = bpy.data.meshes.new
	material_name_format   = material_name.format
	bpy_context_collection_objects_link = bpy.context.collection.objects.link

	def get_or_create_material(name:str, color:tuple):
		material = materials_get(color)

		if material is None:
			if reuse_materials:
				material = bpy_data_materials_get(name)

			if material is not None:
				materials[color] = material
			else:
				material = materials[color] = bpy_data_materials_new(name=name)
				material.diffuse_color = color
				material.use_nodes = use_nodes

				if use_nodes:
					tree = material.node_tree
					tree_nodes = tree.nodes
					tree_nodes_new = tree_nodes.new
					tree_nodes.clear()

					diffuse_node = tree_nodes_new('ShaderNodeBsdfDiffuse')
					diffuse_node.inputs[0].default_value = color

					output_node = tree_nodes_new('ShaderNodeOutputMaterial')

					a = color[3]
					tree_links_new = tree.links.new
					if a < 1:
						mix_node = tree_nodes_new('ShaderNodeMixShader')
						mix_node.inputs[0].default_value = a

						transparent_node = tree_nodes_new('ShaderNodeBsdfTransparent')
						transparent_node.inputs[0].default_value = color

						tree_links_new(diffuse_node.outputs[0], mix_node.inputs[1])
						tree_links_new(transparent_node.outputs[0], mix_node.inputs[2])
						tree_links_new(mix_node.outputs[0], output_node.inputs[0])

					else:
						tree_links_new(diffuse_node.outputs[0], output_node.inputs[0])

		return material

	image = bpy.data.images.load(filepath)

	try:
		channels = image.channels
		if channels not in (1, 3, 4):
			raise IOError(f"Cannot handle image with {channels} channels!")

		width, height = image.size
		pixels = image.pixels[:]

		if auto_scale:
			strides: set[int] = set()
			y_cols: list[list] = [[nan, nan, nan, nan, 0]] * width

			a = 1.0
			for y in range(height):
				offset = y * channels * width

				curr_r = curr_g = curr_b = curr_a = -1
				curr_stride = 0

				for x in range(width):
					if channels == 1:
						r = g = b = pixels[offset + x]
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

					if r == curr_r and g == curr_g and b == curr_b and a == curr_a:
						curr_stride += 1
					else:
						strides.add(curr_stride)
						if curr_stride == 1:
							break
						curr_stride = 1
						curr_r = r
						curr_g = g
						curr_b = b
						curr_a = a

					curr_y = y_cols[x]
					curr_y_r, curr_y_g, curr_y_b, curr_y_a, curr_y_stride = curr_y

					if r == curr_y_r and g == curr_y_g and b == curr_y_b and a == curr_y_a:
						curr_y[4] = curr_y_stride + 1
					else:
						strides.add(curr_y_stride)
						if curr_y_stride == 1:
							break
						curr_y[0] = r
						curr_y[1] = g
						curr_y[2] = b
						curr_y[3] = a
						curr_y[4] = 1

				strides.add(curr_stride)
				if curr_stride == 1:
					break

			for curr_y in y_cols:
				strides.add(curr_y[4])

			strides.remove(0)

			if strides:
				sorted_strides = sorted(strides)
				min_stride = sorted_strides[0]

				if min_stride <= 1:
					print(f"[Import Pixel Art] auto scale faild, minimum stride {min_stride} isn't bigger than 1")
				else:
					print(f'[Import Pixel Art] auto scale: found minimum stride: {min_stride}')
					all_ok = True

					rem = width % min_stride
					if rem:
						print(f'[Import Pixel Art] auto scale faild, width {width} is not a multiple of {min_stride}, remainder: {rem}')
						all_ok = False

					rem = height % min_stride
					if rem:
						print(f'[Import Pixel Art] auto scale faild, height {height} is not a multiple of {min_stride}, remainder: {rem}')
						all_ok = False

					if all_ok:
						for stride in sorted_strides:
							rem = stride % min_stride
							if rem:
								print(f'[Import Pixel Art] auto scale faild, stride {stride} is not a multiple of {min_stride}, remainder: {rem}')
								all_ok = False
								break

					if all_ok:
						new_width  = width  // min_stride
						new_height = height // min_stride
						print(f'[Import Pixel Art] auto scaling pixel art {width} x {height} -> {new_width} x {new_height}')

						new_pixels = array('f', (nan for _ in range(new_width * new_height * channels)))

						for new_y in range(new_height):
							y = new_y * min_stride
							new_offset = new_y * channels * new_width
							offset = y * channels * width

							for new_x in range(new_width):
								x = new_x * min_stride
								if channels == 1:
									new_pixels[new_offset + new_x] = pixels[offset + x]
								elif channels == 3:
									index = offset + x * channels
									new_index = new_offset + new_x * channels
									new_pixels[new_index]     = pixels[index]
									new_pixels[new_index + 1] = pixels[index + 1]
									new_pixels[new_index + 2] = pixels[index + 2]
								else:
									index = offset + x * channels
									new_index = new_offset + new_x * channels
									new_pixels[new_index]     = pixels[index]
									new_pixels[new_index + 1] = pixels[index + 1]
									new_pixels[new_index + 2] = pixels[index + 2]
									new_pixels[new_index + 3] = pixels[index + 3]

						width  = new_width
						height = new_height
						pixels = new_pixels
	finally:
		image.user_clear()
		bpy.data.images.remove(image)

	for other in bpy.context.selected_objects:
		other.select_set(False)

	params = dict(filename=filename, use_nodes=struse_nodes)
	obj_name = parent_name.format(**params)

	materials = {}
	materials_get = materials.get
	a = 1.0

	prev_color = None

	if import_as == 'CUBES':
		cube_verts = (
			(0, 0, 0), # 0
			(1, 0, 0), # 1
			(1, 1, 0), # 2
			(0, 1, 0), # 3
			(0, 0, 1), # 4
			(1, 0, 1), # 5
			(1, 1, 1), # 6
			(0, 1, 1), # 7
		)

		cube_edges = ()

		cube_faces = (
			(0, 1, 2, 3),
			(0, 1, 5, 4),
			(1, 2, 6, 5),
			(4, 5, 6, 7),
			(2, 3, 7, 6),
			(0, 3, 7, 4),
		)

		parent = bpy_data_objects_new(name=obj_name, object_data=None)
		bpy_context_collection_objects_link(parent)
		params = dict(filename=filename, color='', x=0, y=0, use_nodes=struse_nodes)

		cube_name_format = cube_name.format
		mesh_name_format = mesh_name.format

		for y in range(height):
			offset = y * channels * width
			for x in range(width):
				if channels == 1:
					r = g = b = pixels[offset + x]
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

				color = (r, g, b, a)
				params['x'] = x

				if color != prev_color:
					params['color'] = '%02X%02X%02X%02X' % (int(r * 255), int(g * 255), int(b * 255), int(a * 255))
					prev_color = color

				name = material_name_format(**params)

				material = get_or_create_material(name, color)

				cube_mesh_name = mesh_name_format(**params)
				mesh = bpy_data_meshes_new(cube_mesh_name)
				mesh.from_pydata(cube_verts, cube_edges, cube_faces)
				mesh.materials.append(material)
				mesh.update()

				cube_object_name = cube_name_format(**params)
				obj = bpy_data_objects_new(name=cube_object_name, object_data=mesh)
				bpy_context_collection_objects_link(obj)
				obj.location = (x, y, 0)
				obj.parent = parent
				obj.select_set(True)

		parent.select_set(True)
		bpy.context.view_layer.objects.active = parent

	elif import_as == '2D_MESH':

		pixel_verts = []
		pixel_edges = []
		pixel_faces = []
		face_materials = []
		material_slots = {}

		pixel_verts_append    = pixel_verts.append
		pixel_faces_append    = pixel_faces.append
		face_materials_append = face_materials.append
		material_slots_get    = material_slots.get

		mesh = bpy_data_meshes_new(obj_name)
		vert_index = 0
		params = dict(filename=filename, color='', use_nodes=struse_nodes)

		for y in range(height):
			offset = y * channels * width
			for x in range(width):
				r = g = b = 1
				if channels == 1:
					r = g = b = pixels[offset + x]
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

				color = (r, g, b, a)

				if color != prev_color:
					params['color'] = '%02X%02X%02X%02X' % (int(r * 255), int(g * 255), int(b * 255), int(a * 255))
					prev_color = color

				name = material_name_format(**params)

				pixel_verts_append((x,     y,     0))
				pixel_verts_append((x + 1, y,     0))
				pixel_verts_append((x + 1, y + 1, 0))
				pixel_verts_append((x,     y + 1, 0))

				pixel_faces_append((vert_index, vert_index + 1, vert_index + 2, vert_index + 3))
				vert_index += 4

				material = get_or_create_material(name, color)
				material_slot = material_slots_get(material.name)
				if material_slot is None:
					material_slot = len(mesh.materials)
					mesh.materials.append(material)
					material_slots[material.name] = material_slot

				face_materials_append(material_slot)

		mesh.from_pydata(pixel_verts, pixel_edges, pixel_faces)

		for polygon, material_slot in zip(mesh.polygons, face_materials):
			polygon.material_index = material_slot

		mesh.update()

		obj = bpy_data_objects_new(name=obj_name, object_data=mesh)
		bpy_context_collection_objects_link(obj)

		obj.select_set(True)
		bpy.context.view_layer.objects.active = obj

	else:
		assert False, f"Illegal import_as value: {import_as}"

	duration = perf_counter() - timestamp
	print(f"Imported pixel art {obj_name} in {duration} seconds")

	return {'FINISHED'}

class ImportPixelArt(Operator, ImportHelper):
	"""Imports pixel art images, creating colored cubes or squares for each pixel."""

	bl_idname  = "import_image.pixel_art"
	bl_label   = "Import Pixel Art"
	bl_options = {'REGISTER', 'UNDO'}

	filter_glob: StringProperty(default="*.png;*.gif;*.bmp", options={'HIDDEN'})

	import_as: EnumProperty(
		items=(
			('2D_MESH', '2D Mesh',        "A single mesh that contains all pixels as squares.\n"
			                              "To get cubes extrude it by 1 unit in the Z direction or use the solidify modifer.",
			                              "MESH_PLANE", 1),
			('CUBES',   'Separate Cubes', "Separate cubes where each cube is its own object.\n"
			                              "Can be very slow.", "CUBE", 2),
		),
		name="Import As",
		default='2D_MESH',
	)

	use_nodes:       BoolProperty(default=True, name="Use material nodes")
	reuse_materials: BoolProperty(default=False, name="Reuse existing materials with matching names")
	auto_scale:      BoolProperty(default=False, name="Auto down-scaling of up-scaled pixel art (might be slow)")

	parent_name:   StringProperty(default=PARENT_NAME, name="Object Name")
	cube_name:     StringProperty(default=CUBE_NAME, name="Pixel Names")
	mesh_name:     StringProperty(default=MESH_NAME, name="Mesh Names")
	material_name: StringProperty(default=MATERIAL_NAME, name="Material Names")

	def execute(self, context):
		# validate inputs
		pix_params = dict(filename='', color='AABBCCDD', x=0, y=0, use_nodes='')
		for name, value, params in [
				('object name', self.parent_name, dict(filename='', use_nodes='')),
				('material names', self.material_name, pix_params),
				('mesh names', self.mesh_name, pix_params),
				('pixel names', self.cube_name, pix_params),
		]:
			try:
				value.format(**params)
			except ValueError as e:
				self.report({'ERROR'}, f"Format error in {name}: {e}")
				return {'CANCELLED'}
			except KeyError as e:
				self.report({'ERROR'}, f"Illegal key used in {name}: {e}")
				return {'CANCELLED'}

		return read_pixel_art(context, self.filepath,
			import_as=self.import_as,
			use_nodes=self.use_nodes,
			reuse_materials=self.reuse_materials,
			material_name=self.material_name,
			cube_name=self.cube_name,
			mesh_name=self.mesh_name,
			parent_name=self.parent_name,
			auto_scale=self.auto_scale)


def menu_func_import(self, context):
	self.layout.operator(ImportPixelArt.bl_idname, text="Import Pixel Art (.png/.gif/.bmp)")


def register():
	bpy.utils.register_class(ImportPixelArt)
	bpy.types.TOPBAR_MT_file_import.append(menu_func_import)


def unregister():
	bpy.utils.unregister_class(ImportPixelArt)
	bpy.types.TOPBAR_MT_file_import.remove(menu_func_import)


if __name__ == "__main__":
	try:
		unregister()
	except:
		pass
	register()
