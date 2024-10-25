from lxml import etree
import json


class JsonSerializerBase:
    fileExtension = ".json"

    def __init__(self, options = {}):
        self._nodeStack = []
        self._tagStack = []
        self._currentNode = None
        self.options = options
        self._iterating = False


    @property
    def root(self): return self._nodeStack[0]

    @property
    def currentTag(self):
        if isinstance(self._currentNode, dict) and "@tag" in self._currentNode:
            return self._currentNode["@tag"]
        else:
            return self._tagStack[-1]


    def listTags(self):
        print("listTags")
        self._iterating = True
        for node in self._currentNode:
            print("cchanging node and yielding tag")
            print("node", node)
            print("tag", self.currentTag)
            self._currentNode = node
            yield self._currentNode.get("@tag", "")
        self._currentNode = self._nodeStack[-1]
        self._iterating = False

    # call end when done
    def find(self, name):
        found = self._currentNode.get(name, None)
        if found is not None:
            self._nodeStack.append(found)
            self._currentNode = found
            self._tagStack.append(name)
            return True
        return False

    def end(self):
        self._nodeStack.pop()
        self._tagStack.pop()
        self._currentNode = self._nodeStack[-1]


class JsonSerializer(JsonSerializerBase):

    def __init__(self, rootName, options = {}):
        super().__init__(options)
        root = {}
        if "rootIsList" in options and options["rootIsList"]:
            root[rootName] = []
        else:
            root[rootName] = {}
        self._nodeStack = [root, root[rootName]]
        self._currentNode = self._nodeStack[1]
        self.options = options
        # self._currentTag = rootName
        # track tags (are this keys that point to current node? if not list elemets where its @tag?)
        self._tagStack = [rootName]

    # call end when done
    def begin(self, name):
        if isinstance(self._currentNode, dict):
            self._currentNode[name] = {}
            self._currentNode = self._currentNode[name]       
        else:
            self._currentNode.append({ "@tag" : name })
            self._currentNode = self._currentNode[-1]
        self._nodeStack.append(self._currentNode)
        self._tagStack.append(name)

    # call end when done
    def beginList(self, name):
        if isinstance(self._currentNode, dict):
            self._currentNode[name] = []
            self._currentNode = self._currentNode[name]       
        else:
            raise Exception("Not supported") 
        self._nodeStack.append(self._currentNode)
        self._tagStack.append(name)

    def set(self, name, value):
        if isinstance(value, bytes):
            value = str(value)
        self._currentNode[name] = value
    
    # helper method for adding a key/value pair as a child node
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


class JsonDeserializer(JsonSerializerBase):
    def __init__(self, options = {}):
        self._nodeStack = []
        self._currentNode = None
        self.options = options
        self._iterating = False

    def initFromSerializer(self, serializer):
        self._nodeStack = [serializer._nodeStack[0]]
        self._tagStack = []
        self._currentNode = serializer._nodeStack[0]  # TODO: should this be current or stack[0]?

    def get(self, name, default = None):
        return self._currentNode.get(name, default)

    def getBool(self, name, default = False):
        return bool(self._currentNode.get(name, False))

    def getInt(self, name, default = 0):
        return int(self._currentNode.get(name, default))

    def getFloat(self, name, default = 0.0):
        return float(self._currentNode.get(name, default))

    # helper method for getting a key/value pair set as a child node
    def getNested(self, name, default = None):
        # if self._iterating:
        #     if self.currentTag == name:
        #         return self._currentNode.get('text', default)
        #     return default
        # if self.find(name):
        #     val = self._currentNode
        #     self.end()
        #     return val
        return self._currentNode.get(name, default)
        if name in self._currentNode:
            return self._currentNode[name]
        elif "@tag" in self._currentNode:
            return self._currentNode.get("text", default)
        # if self.find(name):
        #     val = self._currentNode.get("text", default)
        #     self.end()
        #     return val
        # return default
        else:
            print("Don't know how to get nested value for", name)
            print("I'm at: ", self._currentNode)
            return default

    def getNestedBool(self, name, default = False):
        value = self.getNested(name)
        return default if value is None else value

    def getNestedInt(self, name, default = 0):
        return int(self.getNested(name, default))

    def getNestedFloat(self, name, default = 0.0):
        return float(self.getNested(name, default))

    def readFile(self, filePath, dataName = None):
        with open(filePath, 'r', encoding="utf-8") as f:
            self._currentNode = json.load(f)
        self._nodeStack = [self._currentNode]
        return True

    def readFileStream(self, filePath, tagFilter = None):
        pass

class XmlSerializerBase:
    fileExtension = ".xml"

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

    # helper method for adding a key/value pair as a child node
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

    def initFromSerializer(self, serializer):
        self._nodeStack = [serializer._nodeStack[0]]
        self._currentNode = serializer._currentNode

    def get(self, name, default = None):
        if name == "text":
            return self._currentNode.text or ''
        else:
            return self._currentNode.get(name, default)

    def getBool(self, name, default = False):
        value = self._currentNode.get(name)
        return default if value is None else value == "1"

    def getInt(self, name, default = 0):
        return int(self._currentNode.get(name, default))

    def getFloat(self, name, default = 0.0):
        return float(self._currentNode.get(name, default))

    # helper method for getting a key/value pair set as a child node
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
        value = self.getNested(name)
        return default if value is None else value == "1"

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
        XmlSerializer.fileExtension : XmlSerializer,
        JsonSerializer.fileExtension : JsonSerializer
    }
    _deserializers = {
        XmlDeserializer.fileExtension : XmlDeserializer,
        JsonDeserializer.fileExtension : JsonDeserializer
    }

    def registerSerializer(type):
        Serialization._serializers[type.fileExtension] = type

    def registerDeserializer(type):
        Serialization._deserializers[type.fileExtension] = type

    def getSerializer(fileExtension, rootName, options = {}):
        return Serialization._serializers[fileExtension.lower()](rootName, options)

    def getDeserializer(fileExtension, options = {}):
        return Serialization._deserializers[fileExtension.lower()](options)

    def getSupportedSerializeFileExtensions():
        return list(Serialization._serializers.keys())

    def getSupportedDeserializeFileExtensions():
        return list(Serialization._deserializers.keys())