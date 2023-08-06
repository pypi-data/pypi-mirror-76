laylib package for pygame
=========================

.. image:: https://img.shields.io/badge/License-MIT-yellow.svg
	:target: https://opensource.org/licenses/MIT

.. image:: https://img.shields.io/badge/version-1.1.7-red.svg
	:target: https://pypi.org/project/laylib

.. image:: https://travis-ci.org/Layto888/laylib.svg?branch=master
	:target: https://travis-ci.org/Layto888/laylib


 

This package is made to fast prototype your multimedia applications like games on pygame. 
Write clean and pragmatic design. It lets you focus on the game engine itself, so you don't have
to take care about several details like setting up the window, loading and checking data (images,
sound, font, fx, music, resources names...).
All you need to do is to put your resources into a specific data folder and use them 
in your game class 'MyEngine()'.

You don't need to reinvent the wheel, some repetitive parts of code (main loop, getting the delta time, 
closing the window, drawing text...) are already described and ready to use in the 
default engine.

    
Usage example
-------------

.. code-block:: python

    from laylib import Environment
    from engine import Engine

    def main():
	demo = Environment(800, 600, False, 'My game')
	demo.load_complete(Engine(), 'data', 'resources.res')
	demo.gInstance.main_loop()
	demo.destroy()

    if __name__ == "__main__":
	main()

	
INSTALLATION
------------

First, install the dependencies:
- Python3 (3.5 or later) <http://www.python.org>
- Pygame 1.9.1 or later <http://pygame.org/download.shtml>
Or run in terminal:

.. code-block:: bash

    $ pip install -r requirements.txt

Then install laylib: 

.. code-block:: bash

    $ pip install laylib

Or alternatively, you can just copy the "laylib" folder into the same
directory as the Python program that uses it.

USAGE
-----
For usage see examples provided with laylib. 
For more details, all other parts of documentation are described in the source file.

Release History
----------------------------
* 1.1.8
    * version 1.1.7 revision
    * add demo4, rain demo
    * add FPS control, now we can set fps with "self.fps" in the main engine to control frame rate.
* 1.1.7
    * version 1.1.6 revision
    * update demo1
* 1.1.6
    * class Music in resources.py: add the function play() to control the music playlist and the volume
    * update demo1 to integrate music play() function.
    * all private methods prefixed with underscore
    * one common data folder for test and demo, to reduce size.
* 1.1.5
    * in Resources manager: the sound format .ogg is moved to Music class and removed from Sound 'fx' class.
    * relative path to test_laylib changed
    * variable self.all_sprites = pg.sprite.Group() set directly in the DefaultEngine class.
    * add demo1 example to show how to manage resources with laylib
    * updating test_laylib for the 1.1.5 version
    * update documentation in the source files.
* 1.1.4
    * Add Travis CI file
    * bug fix rotate function util.py file
    * changed value 3.14 to math.pi deg2rad function util.py
    * add complete test module
    * changed README.md to README.rst
* 1.1.3
    * Bug version package fix (init.py file).
* 1.1.2
    * Removed functions: `load_global()`/`destroy_global()` from Resources class.
    * Bug version fix (setup.py file).
* 1.1.1
    * Now we can set the 'time_unit' to change the delta_time unit.
    * Minor bugs fix on util.py
* 0.1.0
    * The first proper release
* 0.0.1
    * Work in progress

Meta
----
Amardjia Amine – amardjia.amine@gmail.com
Distributed under the MIT license.





