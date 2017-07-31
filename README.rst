.. image:: https://img.shields.io/badge/Donate-PayPal-green.svg
    :target: https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=8A2CSLXDJU752

==========
Bizualizer
==========

.. contents::

Tutorial Video
==============

.. image:: http://i.imgur.com/v1rGCHn.png
  :target: https://www.youtube.com/watch?v=8mskAiSiEjk&feature=youtu.be

Installation
============

1. Download the repository
2. Open Blender
3. Got to File > User Preferences > Addons
4. click "Install From File" and navigate to the downloaded .zip folder
5. Check the box next to "bizualizer"
6. Save User Settings

Usage
=====

.. image:: http://i.imgur.com/bL9sj58.png

In the properties window, click the scene button. The UI is at the
bottom. Add a song by clicking the button with a folder icon. You can
adjust the settings and generate the visualizer. Some examples are shown
below.

Batch Bizualizer
================
Setup Bizualizer instructions in a .csv file and convert all in one go.

Installation
------------
Install `ffmpeg`_ and make it available on your system path (edit your system environment variables if needed)

.. _ffmpeg: https://www.ffmpeg.org/

Install `pillow`_ and `mutagen`_ to the blender python library. The 
easiest way may be to run `get-pip.py`_ with the python.exe file in 
Blender's program folder. Then use the pip.exe in a terminal like this:

path/to/blender/pip.exe install pillow mutagen

.. _get-pip.py: https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=1&ved=0ahUKEwjOyLaI4rLVAhWrjlQKHe8VAWMQFggmMAA&url=https%3A%2F%2Fbootstrap.pypa.io%2Fget-pip.py&usg=AFQjCNE8Fo9j_sgo1hBzEoUT39H85hFDrg

.. _pillow: https://python-pillow.org/

.. _mutagen: https://pypi.python.org/pypi/mutagen

Linux users should install mutagen and pillow to their system-wide python.

Usage
-----
* Create a .csv file like the one included in this package.
* Place all mp3 files and png files into the same folder where the .csv file is located
* Open blender and use the 'Config File' browse button to navigate to the .csv file

CSV Options
-----------
:Song: The name of the song, for example: We Belong.mp3
:Background: The name of the background image, for example: birds.png
:Bar Color: (hexcode) The color that will be applied to the visualize bars. 
:Bar Count: (integer) The number of bars that will be displayed in the visualizer
:Bar Style: The visualizer style. Options include: bottom, top, top-bottom, left, right, left-right, horizontal-center, vertical-center
:Space Fraction: (Float from 0.0 to 1.0) Controls the spacing between bars.
:Height Fraction: (Float from 0.0 to 1.0) Controls the amplitude of the bars.
:Fade: (0 or 1) Add Fade in & out to the video
:Opacity: (Float from 0.0 to 1.0) Controls the opacity of the visualizer bars.

Examples
========

.. image:: http://i.imgur.com/duCaEyY.gif

.. image:: http://i.imgur.com/r20zvgY.gif
