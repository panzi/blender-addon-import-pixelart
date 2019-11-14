Import Pixle Art
================

Blender add-on that imports pixle art images as colored cubes. Pixels
with 100% alpha are ignored.

In use the Install button under Edit > Preferences > Add-ons to install this
script and then click the checkbox to activate it.

Features
--------

This add-on imports pixel art images as colored 1x1x1 cubes. Pixels with 100%
alpha are ignored. All pixels of the same color will share one material. The
material can use nodes. The names of the created cubes and materials can be
controlled through format strings.

![](https://i.imgur.com/Swuoy3s.png)

The imported pixels are all paranted to an empty object so they can be easily
transformed as a whole. The cubes have a size of 1x1x1 so they can be easily
moved around pixel-by-pixel while holding ctrl.

![](https://i.imgur.com/Ypj7pAK.png)

Options
-------

### Use material nodes

When this option is checked the materials of the pixels will use nodes.

### Reuse existing materials with matching names

When this option is checked already existing materials that match the
specified name will be used instead of creating new ones.

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

Copyright © 2016-2019 Mathias Panzenböck

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
