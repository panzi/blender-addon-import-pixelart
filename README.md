Import Pixle Art
================

Blender add-on that imports pixle art images as colored cubes. Pixels
with 100% alpha are ignored.

Copy this script to your scripts/addons folder and activate the script in
blenders addon settings to use.

Features
--------

This add-on imports pixel art images as colored 1x1 cubes. Pixels with 100%
alpha are ignored. All pixels of the same color will share one material. The
material can use nodes (blender internal or cycles nodes, depending on what
renderer is used while importing). The names of the created cubes and materials
can be controlled through format strings.

![](http://i.imgur.com/oP7vGTL.png)

The imported pixels are all paranted to an empty object so they can be easily
transformed as a whole. The cubes have a size of 1x1 so they can be easily
moved around pixel-by-pixel while holding ctrl.

![](http://i.imgur.com/eHTEk6a.png)

MIT License
-----------

Copyright © 2016 Mathias Panzenböck

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
