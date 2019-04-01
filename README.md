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

<pre>
<code>import versionMaker.application.maya.export.animation</code>
<code>afp = versionMaker.application.maya.export.animation.AnimationFilmPublish()</code>
<code>afp.show_folder_location="D:/Google Drive/Projects"</code>
<code>afp.show_folder = "sol"</code>
<code>afp.partition="3D"</code>
<code>afp.division="sequences"</code>
<code>afp.sequence="SF"</code>
<code>afp.shot="0010"</code>
<code>afp.task="layout"</code>
<code>afp.asset="ni"</code>
<code>afp.message="testing publish"</code>
<code>afp.start_frame=1013</code>
<code>afp.end_frame=1013</code>
<code>afp()</code>
</pre>