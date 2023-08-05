

def parsexml(etree):
    """
    :param etree: XML ElementTree
    :return: dict
    """
    element = dict()
    element['attrib'] = etree.attrib
    element['text'] = etree.text
    if len(list(etree)) == 1:
        element[list(etree)[0].tag] = parsexml(list(etree)[0])
    elif len(list(etree)) > 1:
        for child in etree:
            if child.tag in element.keys():
                if type(element[child.tag]) != list:
                    element[child.tag] = [element[child.tag]]
                element[child.tag].append(parsexml(child))
            else:
                element[child.tag] = parsexml(child)
    return element

