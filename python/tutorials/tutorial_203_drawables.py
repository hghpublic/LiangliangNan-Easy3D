# -------------------------------------------------------------------------------
# Tutorial: Drawables in Easy3D
# -------------------------------------------------------------------------------
# This tutorial demonstrates how to visualize different types of data using
# Easy3D's drawables WITHOUT explicitly defining a 3D model. We'll cover:
#   1. Visualizing a set of points with `PointsDrawable`.
#   2. Visualizing a set of triangles or a surface using `TrianglesDrawable`.
#   3. Visualizing a set of edges/lines using `LinesDrawable`.
#   4. Visualizing a set of edges/lines in screen coordinates using `LinesDrawable2D`.
#   5. Running the Easy3D MultiViewer to display the visualizations.
# -------------------------------------------------------------------------------

# -------------------------------------------------------------------------------
# Adding Easy3D Python Bindings to the System Path
# -------------------------------------------------------------------------------
# This is required if the bindings are not installed via `pip` but are located in
# a local build directory. For building and installing Python bindings of Easy3D,
# please refer to: https://github.com/LiangliangNan/Easy3D/blob/main/ReadMe.md
# -------------------------------------------------------------------------------
import sys
sys.path.append("../../cmake-build-release/lib/python")

# Importing necessary libraries
import easy3d

import random # for random point generation
import numpy  # for its array

# -------------------------------------------------------------------------------
# Initializing Easy3D
# -------------------------------------------------------------------------------
# The `easy3d.initialize(False)` function initializes the Easy3D library.
# Use `True` to enable detailed logging, which is useful for debugging.
easy3d.initialize(False)

# -------------------------------------------------------------------------------
# Setting Up a Multi-View Layout with Easy3D MultiViewer
# -------------------------------------------------------------------------------
# Create a `MultiViewer` instance with a 2x2 grid layout and a custom window title.
# The MultiViewer allows displaying multiple views in a single window.
viewer = easy3d.MultiViewer(2, 2, "Easy3D Viewer - Drawables")
viewer.set_usage("") # Optional. Just to hide the lengthy manual in console window

# -------------------------------------------------------------------------------
# View (0, 0): A set of random 3D points
# -------------------------------------------------------------------------------
points = [(random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5)) for _ in range(10000)] # Generate 10,000 random 3D points
points_drawable = easy3d.PointsDrawable("points")   # Create a `PointsDrawable` named "points"
points_drawable.update_vertex_buffer(points);       # Upload vertex positions
viewer.add_drawable(points_drawable)                # Add the drawable to the viewer.
viewer.assign(0, 0, points_drawable)                # Assign the drawable to the top-left view (0, 0).

# -------------------------------------------------------------------------------
# View (0, 1): A set of set of triangles (i.e., a surface) representing a unit cube
# -------------------------------------------------------------------------------
cube_vertices = numpy.array([   # Vertices of a unit cube.
    [-0.5, -0.5, -0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [-0.5, 0.5, -0.5],
    [-0.5, -0.5,  0.5], [0.5, -0.5,  0.5], [0.5, 0.5,  0.5], [-0.5, 0.5,  0.5],
])
cube_indices = numpy.array([    # Indices for the 12 triangles (two per face of the cube)
    0, 2, 1,    0, 3, 2,    4, 5, 6,    4, 6, 7,    0, 7, 3,    0, 4, 7,
    1, 2, 6,    1, 6, 5,    0, 1, 5,    0, 5, 4,    2, 3, 7,    2, 7, 6,
])
triangles_drawable = easy3d.TrianglesDrawable("cube")     # Create a `TrianglesDrawable` named "cube"
triangles_drawable.update_vertex_buffer(cube_vertices)    # Upload vertex positions
triangles_drawable.update_element_buffer(cube_indices)    # Upload the vertex indices of the cube faces
viewer.add_drawable(triangles_drawable)  # Add the cube to the viewer
viewer.assign(0, 1, triangles_drawable)  # Assign the cube to the top-right view (0, 1).

# -------------------------------------------------------------------------------
# View (1, 0): A set of 3D line segments
# -------------------------------------------------------------------------------
# In this tutorial, we show the wireframe of the above cube.
wireframe = easy3d.LinesDrawable("wireframe")   # Create a `LinesDrawable` named "wireframe"
wireframe.update_vertex_buffer(cube_vertices)   # Upload vertex positions
wireframe_indices = numpy.array([               # Indices for the 12 edges of the cube
    0, 1,   1, 2,   2, 3,   3, 0,       # Bottom face edges
    4, 5,   5, 6,   6, 7,   7, 4,       # Top face edges
    0, 4,   1, 5,   2, 6,   3, 7        # Vertical edges connecting top and bottom faces
])
wireframe.update_element_buffer(wireframe_indices)  # Upload the vertex indices of the cube edges
viewer.add_drawable(wireframe)  # Add the cube to the viewer
viewer.assign(1, 0, wireframe)  # Assign the wireframe to the bottom-left view (1, 0).

# -------------------------------------------------------------------------------
# View (1, 1): A set of 2D line segments defined in the screen space
# -------------------------------------------------------------------------------
star_vertices = numpy.array([   # The vertices of the star shape (each vertex is a 2D point).
    [505, 480], [411, 104], [317, 480], [600, 245], [223, 245],
    [350, 351], [411, 402], [376, 245], [447, 245], [473, 351]
    ], dtype=numpy.float32)
star = easy3d.LinesDrawable2D("star")   # Create a `LinesDrawable2D` named "star"
star.update_vertex_buffer(star_vertices, viewer.width(), viewer.height())  # Upload vertex positions
star_indices = numpy.array([0, 6,   6, 2,   2, 5,   5, 4,   4, 7,   7, 1,   1, 8,   8, 3,   3, 9,   9, 0])  # Indices for the edges of the star.
star.update_element_buffer(star_indices)  # Upload vertex indices of the star edges
viewer.add_drawable(star)  # Add the star to the viewer
viewer.assign(1, 1, star)  # Assign the star to the bottom-right view (1, 1).

# Running the Viewer
viewer.run()