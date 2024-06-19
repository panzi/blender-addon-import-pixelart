Import Pixel Art
================

Blender add-on that imports pixel art images as colored cubes or squares.
Pixels with 100% alpha are ignored.

Use the Install button under Edit > Preferences > Add-ons to install this
script and then click the checkbox to activate it.

**NOTE:** For best resuts the imported pixel art should actually have the
apparent pixel be actual pixels in the image. If not, there is an option to
[automaticall down-scale](#auto-down-scaling-of-up-scaled-pixel-art) such
images, but it will not work for lossy images (JPEG) and might be slow. Maybe
you'd rather want to down-scale the image manually (using nearest neighbor
option) in an image editor.

Features
--------

This add-on imports pixel art images as colored 1x1x1 separate cubes or 1x1
planes in a single mesh. Pixels with 100% alpha are ignored. All pixels of the
same color will share one material. The material can use nodes. The names of
the created cubes and materials can be controlled through format strings.

![Screenshot: Select image](https://i.imgur.com/HYQDuXh.png)

If you use the option 'Separate Cubes' then the imported pixels are all parented
to an empty object so they can be easily transformed as a whole. The cubes have
a size of 1x1x1 so they can be easily moved around pixel-by-pixel while holding
ctrl.

![Screenshot: Imported as cubes](https://i.imgur.com/G7shPkv.png)

If you use the option '2D Mesh' all the pixels will be planes in one single mesh.
If you still want cubes then simply extrude the whole mesh by 1 unit in the Z
direction. Alternatively you simply can use the solidify modifier.

This option imports **much faster** and it seems it is also faster to work with
a single large mesh in blender than to work with many small objects.

![Screenshot: Imported as planes](https://i.imgur.com/esBicPn.png)

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
apparent pixel is actually e.g. 8x8 or more pixels in the image. When this
option is checked the image is analyzed and automatically down-scaled. This
might be pretty slow for big images, since this is all done in Python.

**NOTE:** This only works if the image was up-scaled to an exact integer
multiple of the original and no other filters where applied. If the image
was saved as a lossy format like JPEG this will fail pretty much always,
since lossy formats kinda smudge the pixels. The used image should best
be PNG, BMP, or GIF.

The algorithm is quite primitive, but works for many pixel art images.

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
* `{use_nodes}` – The string `nodes` if the use material nodes option is
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
