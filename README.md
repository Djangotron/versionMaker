# Version Maker
A repository to create versions of any type of asset.

This is designed to be used with arbitrary projects however its initially designed for film.


# Instructions

# DCC Application integration
- For creation via a DCC you should create a sub directory to the application folder.

# Structure
- All folder structures should be saved to a folder in constants
- eg: 'Film' has a directory with a hierarchy.py file
- hierarchy.py files with define path structure in a project




# Examples

## Maya Alembic Export


<p><code>import versionMaker.application.maya.export.animation<code></p>
<p><code>afp = versionMaker.application.maya.export.animation.AnimationFilmPublish()<code></p>
<p><code>afp.show_folder_location="D:/Google Drive/Projects"<code></p>
<p><code>afp.show_folder = "sol"<code></p>
<p><code>afp.partition="3D"<code></p>
<p><code>afp.division="sequences"<code></p>
<p><code>afp.sequence="SF"<code></p>
<p><code>afp.shot="0010"<code></p>
<p><code>afp.task="layout"<code></p>
<p><code>afp.asset="ni"<code></p>
<p><code>afp.message="testing publish"<code></p>
<p><code>afp.start_frame=1013<code></p>
<p><code>afp.end_frame=1013<code></p>
<p><code>afp()<code></p>