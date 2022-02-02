import lxml.etree as etree
import logging

class XmlVerifier(object):
    def __init__(self):
        pass

    allowedAttributesVarianten = ["pflichtwahl"]
    allowedAttributesVariante = ["name", "beschreibung", "geschlecht"]
    allowedAttributesAuswahl = ["name", "beschreibung", "geschlecht", "varianten", "keine-varianten"]
    allowedChoicesAttributes = {
        "Vorteil" : ["name", "wert", "kommentar"],
        "Talent" : ["name"],
        "Fertigkeit" : ["name", "wert"],
        "Übernatürliche-Fertigkeit" : ["name", "wert"],
        "Freie-Fertigkeit" : ["name", "wert"],
        "Attribut" : ["name", "wert"],
        "Eigenheit" : ["name"]
    }

    def validateXmlChoices(node):
        for child in node.getchildren():
            if not child.tag in XmlVerifier.allowedChoicesAttributes.keys():
                logging.warn("CharakterAssistent: Unbekanntes XML element " + child.tag)

            for attrib in child.attrib:
                if not attrib in XmlVerifier.allowedChoicesAttributes[child.tag]:
                    logging.warn("CharakterAssistent: Unbekanntes XML attribut " + attrib)


    def validateXml(node):
        for child in node.getchildren():
            if child.tag != "Auswahl" and child.tag != "Varianten":
                logging.warn("CharakterAssistent: Unbekanntes XML element " + child.tag)

            if child.tag == "Auswahl":
                for attrib in child.attrib:
                    if not attrib in XmlVerifier.allowedAttributesAuswahl:
                        logging.warn("CharakterAssistent: Unbekanntes XML attribut " + attrib)

                XmlVerifier.validateXmlChoices(child)
            elif child.tag == "Varianten":
                for attrib in child.attrib:
                    if not attrib in XmlVerifier.allowedAttributesVarianten:
                        logging.warn("CharakterAssistent: Unbekanntes XML attribut " + attrib)

                for child2 in child.getchildren():
                    if child2.tag != "Variante":
                        logging.warn("CharakterAssistent: Unbekanntes XML element " + child2.tag)

                    for attrib in child2.attrib:
                        if not attrib in XmlVerifier.allowedAttributesVariante:
                            logging.warn("CharakterAssistent: Unbekanntes XML attribut " + attrib)

                    XmlVerifier.validateXmlChoices(child2)