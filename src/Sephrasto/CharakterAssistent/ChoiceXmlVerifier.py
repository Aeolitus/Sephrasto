import lxml.etree as etree
import logging

class ChoiceXmlVerifier(object):
    def __init__(self):
        pass

    allowedAttributesVarianten = ["pflichtwahl"]
    allowedAttributesVariante = ["name", "beschreibung", "geschlecht"]
    allowedAttributesAuswahl = ["name", "beschreibung", "geschlecht", "varianten", "keine-varianten"]
    allowedChoicesAttributes = {
        "Vorteil" : ["name", "wert", "kommentar"],
        "Talent" : ["name", "wert", "kommentar"],
        "Fertigkeit" : ["name", "wert"],
        "Übernatürliche-Fertigkeit" : ["name", "wert"],
        "Freie-Fertigkeit" : ["name", "wert"],
        "Attribut" : ["name", "wert"],
        "Eigenheit" : ["name"]
    }

    def validateXmlChoices(node):
        errors = []
        for child in node.getchildren():
            if not child.tag in ChoiceXmlVerifier.allowedChoicesAttributes.keys():
                errors.append("Unbekanntes XML element " + child.tag)
                logging.warn(errors[-1])

            for attrib in child.attrib:
                if not attrib in ChoiceXmlVerifier.allowedChoicesAttributes[child.tag]:
                    errors.append("Unbekanntes XML attribut " + attrib)
                    logging.warn(errors[-1])
        return errors


    def validateXml(node):
        errors = []
        for child in node.getchildren():
            if child.tag != "Auswahl" and child.tag != "Varianten":
                errors.append("Unbekanntes XML element " + child.tag)
                logging.warn(errors[-1])

            if child.tag == "Auswahl":
                for attrib in child.attrib:
                    if not attrib in ChoiceXmlVerifier.allowedAttributesAuswahl:
                        errors.append("Unbekanntes XML attribut " + attrib)
                        logging.warn(errors[-1])

                errors.extend(ChoiceXmlVerifier.validateXmlChoices(child))
            elif child.tag == "Varianten":
                for attrib in child.attrib:
                    if not attrib in ChoiceXmlVerifier.allowedAttributesVarianten:
                        errors.append("Unbekanntes XML attribut " + attrib)
                        logging.warn(errors[-1])

                for child2 in child.getchildren():
                    if child2.tag != "Variante":
                        errors.append("Unbekanntes XML element " + child2.tag)
                        logging.warn(errors[-1])

                    for attrib in child2.attrib:
                        if not attrib in ChoiceXmlVerifier.allowedAttributesVariante:
                            errors.append("Unbekanntes XML attribut " + attrib)
                            logging.warn(errors[-1])

                    errors.extend(ChoiceXmlVerifier.validateXmlChoices(child2))
        return errors