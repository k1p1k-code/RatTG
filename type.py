from typing import Literal


class TypeInfo():
    on_pc='on_pc'
    off_pc='off_pc'
    polling='polling'
    literal=Literal[on_pc, off_pc, polling]



class TypeTasks():
    screenshot='screenshot'
    messagebox='messagebox'
    info_pc='info_pc'
    collection_pc='collection_pc'