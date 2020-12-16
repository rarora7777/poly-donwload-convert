# Scripts to download and process Tilt Brush models from Poly

**NOTE.** You need to set up a Google API Key with permission to access the Poly API first. Please see instructions here: https://developers.google.com/poly/develop/api.

Once you have set up the key, set an environment variable named `POLY_API_KEY` with your API Key as the value.

## How to use

`poly_download_tilt`: Download a Tilt Brush model from Poly. Usage:

    python poly_download_tilt.py <assetID> <download_filename>
  
`tiltbrush_basic.py`: Convert a `.tilt` file to a human-readable and easily-processable `.dat` file. Usage:

    python tiltbrush_basic.py <downloaded_filename>
    
saves to `<downloaded_filename>.dat`. Calling:

    python tiltbrush_basic.py <downloaded_filename> <converted_filename>
    
saves to `<converted_filename>`.

The latter requires Google's [`tilt_brush_toolkit`](https://github.com/rarora7777/tilt-brush-toolkit), and the environment
variable `TILT_BRUSH_TOOLKIT_ROOT` should point to its root folder. Note that we use the forked version of the toolkit, which
has been converted to python3.

The converted file has the following format:

    # number of strokes
    num_stroke
    
    # for each stroke, the first line contains the following info:
    brush_name brush_type brush_color_r brush_color_g brush_color_b brush_color_a brush_size stroke_scale num_control_points
    
    # each control point is given as a position (3-vector in metres), an orientation (quaternion), and a timestamp
    pos_x pos_y pos_z rot_x rot_y rot_z rot_w time

Note that strokes created using effect brushes (where the brush geometry type is `Effect` or the brush style is `Anim`) are ignored and not included in the converted file.
