from lxml import etree

class XmlSerializer:
    def __init__(self, rootName, options = {}):
        self._nodeStack = [etree.Element(rootName)]
        self._currentNode = self._nodeStack[0]
        self.options = options

    @property
    def root(self): return self._nodeStack[0]

    def begin(self, name):
        self._currentNode = etree.SubElement(self._currentNode, name)
        self._nodeStack.append(self._currentNode)

    def end(self):
        self._nodeStack.pop()
        self._currentNode = self._nodeStack[-1]

    def set(self, name, value):
        if name != "text":
            if type(value) == bool:
                self._currentNode.set(name, "1" if value else "0")
            else:
                self._currentNode.set(name, str(value))
        else:
            self._currentNode.text = str(value)

    def writeFile(self, filepath):
        doc = etree.ElementTree(self.root)
        with open(filepath, 'wb') as file:
            file.seek(0)
            file.truncate()
            doctype = """<!DOCTYPE xsl:stylesheet [
   <!ENTITY nbsp "&#160;">
]>"""
            doc.write(file, xml_declaration=True, encoding='UTF-8', pretty_print=True, doctype=doctype)
            file.truncate()

class XmlDeserializer:
    _cache = {}
    _migrations = {}

    def registerMigration(dataName, migration):
        XmlDeserializer._migrations[dataName] = migration

    def __init__(self, options = {}):
        self._root = None
        self._currentNode = None
        self.options = options

    @property
    def root(self): return self._root

    @property
    def currentName(self): return self._currentNode.tag

    def next(self):
        for node in self.root.iter():
            self._currentNode = node
            yield self._currentNode.tag

    def find(self, name):
        found = self._root.find(name)
        if found is not None:
            self._currentNode = found
            return True
        return False

    def get(self, name, default = None):
        if name == "text":
            return self._currentNode.text or ''
        else:
            return self._currentNode.get(name, default)

    def getBool(self, name, default = None):
        return self._currentNode.get(name, default) == "1"

    def getInt(self, name, default = None):
        return int(self._currentNode.get(name, default))

    def getFloat(self, name, default = None):
        return float(self._currentNode.get(name, default))

    def readFile(self, filePath, dataName = None):
        useCache = "useCache" in self.options and self.options["useCache"]
        if useCache and filePath in XmlDeserializer._cache:
            self._root = XmlDeserializer._cache[filePath]
        else:
            self._root = etree.parse(filePath).getroot()
            if dataName is None:
                dataName = self._root.tag
            if dataName in XmlDeserializer._migrations:
                if not XmlDeserializer._migrations[dataName](self._root):
                    return False

            if useCache:
                XmlDeserializer._cache[filePath] = self._root
            else:
                XmlDeserializer._cache.pop(filePath, None)
        self._currentNode = self._root

class Serialization:
    _serializers = {
        ".xml" : XmlSerializer
    }
    _deserializers = {
        ".xml" : XmlDeserializer
    }

    def registerSerializer(type, fileExtension):
        Serialization._serializers[fileExtension.lower()] = type

    def registerDeserializer(type, fileExtension):
        Serialization._deserializers[fileExtension.lower()] = type

    def getSerializer(fileExtension, rootName, options = {}):
        return Serialization._serializers[fileExtension.lower()](rootName, options)

    def getDeserializer(fileExtension, options = {}):
        return Serialization._deserializers[fileExtension.lower()](options)

    def getSupportedSerializeFileExtensions():
        return list(Serialization._serializers.keys())

    def getSupportedDeserializeFileExtensions():
        return list(Serialization._deserializers.keys())

