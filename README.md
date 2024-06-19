Import Pixle Art
================

Blender add-on that imports pixle art images as colored cubes or squares.
Pixels with 100% alpha are ignored.

Use the Install button under Edit > Preferences > Add-ons to install this
script and then click the checkbox to activate it.

Features
--------

This add-on imports pixel art images as colored 1x1x1 separate cubes or 1x1
planes in a single mesh. Pixels with 100% alpha are ignored. All pixels of the
same color will share one material. The material can use nodes. The names of
the created cubes and materials can be controlled through format strings.

![](https://i.imgur.com/d9jeYRt.png)

If you use the option 'Separate Cubes' then the imported pixels are all parented
to an empty object so they can be easily transformed as a whole. The cubes have
a size of 1x1x1 so they can be easily moved around pixel-by-pixel while holding
ctrl.

![](https://i.imgur.com/f6kIrQw.png)

If you use the option '2D Mesh' all the pixels will be planes in one single mesh.
If you still want cubes then simply extrude the whole mesh by 1 unit in the Z
direction. Alternatively you simply can use the solidify modifier.

This option imports **much faster** and it seems it is also faster to work with
a single large mesh in blender than to work with many small objects.

![](https://i.imgur.com/C4lITnC.png)

Options
-------

### Import As

* Separate Cubes: Separate cubes where each cube is its own object.
* 2D Mesh: A single mesh that contains all pixels as squares.

### Use material nodes

When this option is checked the materials of the pixels will use nodes.

### Reuse existing materials with matching names

When this option is checked already existing materials that match the
specified name will be used instead of creating new ones.

### Auto down-scaling of up-scaled pixel art

Often pixel art is posted on the internet in an upscaled form, meaning one
apprent pixel are actually 8x8 or more pixels. When this option is checked the
image is analyzed and automatically down-scaled. This might be pretty slow
for big images, since this is all done in Python. Also it only works if the
image was up-scaled to an exact integer multiple of the original and no other
filters where applied. The algorithm is quite primitive, but works for many
pixel art images.

### Object Name

Pattern for the name of the empty object that will be the parent of all the
pixels. This object is helpful when you want to transform the whole pixel art
at once. You can safely delete it if you don't want it.

[Pattern variables](#patterns): `{filename}`, `{use_nodes}`

### Pixel Names

Pattern for the names of the pixel objects.

[Pattern variables](#patterns): `{filename}`, `{use_nodes}`, `{color}`, `{x}`, `{y}`

### Mesh Names

Pattern of the names of the meses of the pixels.

[Pattern variables](#patterns): `{filename}`, `{use_nodes}`, `{color}`, `{x}`, `{y}`

### Material Names

Pattern of the names of the materials of the pixels. Note that pixels of the
same color will also share the same material. This way you can easily change
the material properties of all pixels of the same color.

[Pattern variables](#patterns): `{filename}`, `{use_nodes}`, `{color}`, `{x}`, `{y}`

Patterns
--------

In name patterns certain variables will be replaced with their respective
values. Because these variables use a `{name}`-syntax if you want to include
curly braces in your names you need to escape them as `{{` and `}}`.

* `{filename}` – The name of the file (not including the folder names).
* `{use_nodes}` – The stirng `nodes` if the use material nodes option is
  slected, an empty string otherwise.
* `{color}` – Hexa-decimal string of the color of the pixel (RRGGBBAA).
* `{x}` – X-coordinate of the pixel.
* `{y}` – Y-coordinate of the pixel.

MIT License
-----------

Copyright © 2016-2020 Mathias Panzenböck

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
