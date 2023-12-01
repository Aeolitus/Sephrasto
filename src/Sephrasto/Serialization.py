from lxml import etree
import json

class JsonSerializer:
    def __init__(self, rootName, options = {}):
        root = {}
        if "rootIsList" in options and options["rootIsList"]:
            root[rootName] = []
        else:
            root[rootName] = {}
        self._nodeStack = [root, root[rootName]]
        self._currentNode = self._nodeStack[1]
        self.options = options

    @property
    def root(self): return self._nodeStack[0]

    def listTags(self):
        for node in self._currentNode:
            self._currentNode = node
            yield self._currentNode["@tag"]
        self._currentNode = self._nodeStack[-1]

    # call end when done
    def find(self, name):
        found = self._currentNode.get(name, None)
        if found is not None:
            self._nodeStack.append(found)
            self._currentNode = found
            return True
        return False

    # call end when done
    def begin(self, name):
        if isinstance(self._currentNode, dict):
            self._currentNode[name] = {}
            self._currentNode = self._currentNode[name]       
        else:
            self._currentNode.append({ "@tag" : name })
            self._currentNode = self._currentNode[-1]
        self._nodeStack.append(self._currentNode)

    # call end when done
    def beginList(self, name):
        if isinstance(self._currentNode, dict):
            self._currentNode[name] = []
            self._currentNode = self._currentNode[name]       
        else:
            raise Exception("Not supported") 
        self._nodeStack.append(self._currentNode)

    def end(self):
        self._nodeStack.pop()
        self._currentNode = self._nodeStack[-1]

    def set(self, name, value):
        if isinstance(value, bytes):
            value = str(value)
        self._currentNode[name] = value

    def setNested(self, name, value):
        if isinstance(value, bytes):
            value = str(value)

        if isinstance(self._currentNode, dict):
            self._currentNode[name] = value     
        else:
            self._currentNode.append({ "@tag" : name, "text" : value })

    def writeFile(self, filepath):
        with open(filepath, 'w', encoding="utf-8") as f:
            json.dump(self.root, f, indent=4, ensure_ascii=False)

class XmlSerializerBase:
    def __init__(self, options = {}):
        self._nodeStack = []
        self._currentNode = None
        self.options = options
        self._iterating = True

    @property
    def root(self): return self._nodeStack[0]

    @property
    def currentTag(self): return self._currentNode.tag

    def listTags(self):
        self._iterating = True
        for node in self._currentNode:
            self._currentNode = node
            yield self._currentNode.tag
        self._iterating = False
        self._currentNode = self._nodeStack[-1]

    # call end when done
    def find(self, name):
        found = self._currentNode.find(name)
        if found is not None:
            self._nodeStack.append(found)
            self._currentNode = found
            return True
        return False

    def end(self):
        self._nodeStack.pop()
        self._currentNode = self._nodeStack[-1]

class XmlSerializer(XmlSerializerBase):
    def __init__(self, rootName, options = {}):
        super().__init__(options)
        self._nodeStack.append(etree.Element(rootName))
        self._currentNode = self._nodeStack[0]

    # call end when done
    def begin(self, name):
        self._currentNode = etree.SubElement(self._currentNode, name)
        self._nodeStack.append(self._currentNode)

    # call end when done
    def beginList(self, name):
        self.begin(name)

    def set(self, name, value):
        if name == "text":
            if isinstance(value, bytes):
                self._currentNode.text = value
            elif isinstance(value, bool):
                self._currentNode.set(name, "1" if value else "0")
            else:
                self._currentNode.text = str(value)
        else:
            if isinstance(value, bool):
                self._currentNode.set(name, "1" if value else "0")
            else:
                self._currentNode.set(name, str(value))

    def setNested(self, name, value):
        node = etree.SubElement(self._currentNode, name)
        if isinstance(value, bytes):
            node.text = value
        elif isinstance(value, bool):
            node.text = "1" if value else "0"
        else:
            node.text = str(value)

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

class XmlDeserializer(XmlSerializerBase):
    _cache = {}
    _migrations = {}

    def registerMigration(dataName, migration):
        XmlDeserializer._migrations[dataName] = migration

    def __init__(self, options = {}):
        super().__init__(options)
        self._iterating = False

    def get(self, name, default = None):
        if name == "text":
            return self._currentNode.text or ''
        else:
            return self._currentNode.get(name, default)

    def getBool(self, name, default = False):
        return self._currentNode.get(name, default) == "1"

    def getInt(self, name, default = 0):
        return int(self._currentNode.get(name, default))

    def getFloat(self, name, default = 0.0):
        return float(self._currentNode.get(name, default))

    def getNested(self, name, default = None):
        if self._iterating:
            if self.currentTag == name:
                return self._currentNode.text or ''
            return default
        if self.find(name):
            val = self._currentNode.text or ''
            self.end()
            return val
        return default

    def getNestedBool(self, name, default = False):
        return self.getNested(name, default) == "1"

    def getNestedInt(self, name, default = 0):
        return int(self.getNested(name, default))

    def getNestedFloat(self, name, default = 0.0):
        return float(self.getNested(name, default))

    def readFile(self, filePath, dataName = None):
        useCache = "useCache" in self.options and self.options["useCache"]
        if useCache and filePath in XmlDeserializer._cache:
            self._currentNode = XmlDeserializer._cache[filePath]
        else:
            self._currentNode = etree.parse(filePath).getroot()
            if dataName is None:
                dataName = self._currentNode.tag
            if dataName in XmlDeserializer._migrations:
                if not XmlDeserializer._migrations[dataName](self._currentNode):
                    return False

            if useCache:
                XmlDeserializer._cache[filePath] = self._currentNode
            else:
                XmlDeserializer._cache.pop(filePath, None)
        self._nodeStack = [self._currentNode]
        return True

    def readFileStream(self, filePath, tagFilter = None):
        for event, element in etree.iterparse(filePath, tag=tagFilter):
            self._currentNode = element
            yield self._currentNode.tag

class Serialization:
    _serializers = {
        ".xml" : XmlSerializer,
        ".json" : JsonSerializer
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

