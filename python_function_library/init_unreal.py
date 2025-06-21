import unreal
import function_library # Important to import the module to initialize it

"""
Make sure to place this file as well as the module in a Python folder that will be initialized at launch by Unreal Engine.
By default unreal engine initialize "Python" folder at the root of "Content" or "Plugins" (eg. "/Game/Python/" or "/Plugin/Python/").
If you don't do this, Unreal won't be able to recognize your function library, and all the nodes will be broken every time the engine starts.
https://dev.epicgames.com/documentation/en-us/unreal-engine/scripting-the-unreal-editor-using-python?application_version=5.3#pythonenvironmentandpathsintheunrealeditor
"""

unreal.log("Module loaded")
