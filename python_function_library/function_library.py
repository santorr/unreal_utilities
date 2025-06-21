import unreal

@unreal.uclass()
class PythonFunctionLibrary(unreal.BlueprintFunctionLibrary):
    """
    EDITOR ONLY

    Python blueprint library, can create any node as you want.

    Supported :
        - Multiple inputs
        - Unreal engine input and output types
    Not supported :
        - Multiple outputs

    static :
        could be True for a function library
    params :
        params=[unreal.Vector, bool, str]
    ret :
        ret=unreal.Vector
    meta :
        - Category          : display category in palette
        - DisplayName       : display name in palette and graph
        - Tooltip           : simple tooltip function text
        - Keywords          : keywords to search
        - CompactNodeTitle  : set compact node title
    """

    @unreal.ufunction(static=True, ret=int, params=[int, int], meta=dict(Category="Custom library", ToolTip="Simple addition operation", Keywords="Maths"))
    def addition(a, b):
        return a + b
    
    @unreal.ufunction(static=True, ret=int, params=[int, int], meta=dict(Category="Custom library", ToolTip="Simple subtraction operation", Keywords="Maths"))
    def subtraction(a, b):
        return a - b
