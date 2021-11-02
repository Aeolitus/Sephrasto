import bisect


class PriotizedCallback:
    def __init__(self):
        self.priority = 0
        self.callback = None

    def __lt__(self, other):
        return self.priority < other.priority


class EventBus:
    actionCallbacks = {}
    filterCallbacks = {}

    @staticmethod
    def addFilter(filterName, callback, priority=0):
        if not (filterName in EventBus.filterCallbacks):
            EventBus.filterCallbacks[filterName] = []
        cb = PriotizedCallback()
        cb.priority = priority
        cb.callback = callback
        bisect.insort(EventBus.filterCallbacks[filterName], cb)

    @staticmethod
    def applyFilter(filterName, filterValue, paramDict={}):
        if not (filterName in EventBus.filterCallbacks):
            return filterValue

        for cb in EventBus.filterCallbacks[filterName]:
            filterValue = cb.callback(filterValue, paramDict)

        return filterValue

    @staticmethod
    def addAction(actionName, callback, priority=0):
        if not (actionName in EventBus.actionCallbacks):
            EventBus.actionCallbacks[actionName] = []
        cb = PriotizedCallback()
        cb.priority = priority
        cb.callback = callback
        bisect.insort(EventBus.actionCallbacks[actionName], cb)

    @staticmethod
    def doAction(actionName, paramDict={}):
        if not (actionName in EventBus.actionCallbacks):
            return
        for cb in EventBus.actionCallbacks[actionName]:
            cb.callback(paramDict)
