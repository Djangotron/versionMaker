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

<code>
<p>import versionMaker.application.maya.export.animation</P>
<p>afp = versionMaker.application.maya.export.animation.AnimationFilmPublish()</P>
<p>afp.show_folder_location="D:/Google Drive/Projects"</P>
<p>afp.show_folder = "sol"</P>
<p>afp.partition="3D"</P>
<p>afp.division="sequences"</P>
<p>afp.sequence="SF"</P>
<p>afp.shot="0010"</P>
<p>afp.task="layout"</P>
<p>afp.asset="ni"</P>
<p>afp.message="testing publish"</P>
<p>afp.start_frame=1013</P>
<p>afp.end_frame=1013</P>
<p>afp()</P>
</code>