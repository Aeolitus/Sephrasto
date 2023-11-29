import bisect

class PriotizedCallback():
    def __init__(self):
        self.priority = 0
        self.callback = None

    def __lt__(self, other):
        return self.priority < other.priority

class EventBus:
    actionCallbacks = {}
    filterCallbacks = {}
    _deprecated = { "charakter_xml_laden", "charakter_xml_geladen", "charakter_xml_schreiben", "datenbank_xml_laden", "datenbank_xml_schreiben" }

    @staticmethod
    def addFilter(filterName, callback, priority=0):
        if filterName in EventBus._deprecated:
            raise Exception(f"Der Filter {filterName} wird nicht mehr unterstützt.")

        if not (filterName in EventBus.filterCallbacks):
            EventBus.filterCallbacks[filterName] = []
        cb = PriotizedCallback()
        cb.priority = priority
        cb.callback = callback
        bisect.insort(EventBus.filterCallbacks[filterName], cb)

    @staticmethod
    def applyFilter(filterName, filterValue, paramDict = {}):
        if not (filterName in EventBus.filterCallbacks):
            return filterValue

        for cb in EventBus.filterCallbacks[filterName]:
            filterValue = cb.callback(filterValue, paramDict)

        return filterValue

    @staticmethod
    def addAction(actionName, callback, priority=0):
        if actionName in EventBus._deprecated:
            raise Exception(f"Die Action {actionName} wird nicht mehr unterstützt.")

        if not (actionName in EventBus.actionCallbacks):
            EventBus.actionCallbacks[actionName] = []
        cb = PriotizedCallback()
        cb.priority = priority
        cb.callback = callback
        bisect.insort(EventBus.actionCallbacks[actionName], cb)

    @staticmethod
    def doAction(actionName, paramDict = {}):
        if not (actionName in EventBus.actionCallbacks):
            return
        for cb in EventBus.actionCallbacks[actionName]:
            cb.callback(paramDict)