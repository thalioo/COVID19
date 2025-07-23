import xml.etree.ElementTree as ET


def update_param(name, val, root):
    xpath = name.replace(".", "/")
    el = root.findall("./{}".format(xpath))
    splited = []
    if(len(el) == 1):
        el = el[0]
    elif(len(el)==0):
        splited = xpath.rsplit("/")
        name = splited[-2]
        tag = '/'.join(splited[:-2])
        cand_el = root.findall("./{}".format(tag))
        print(cand_el)
        for e in cand_el:
            if e.attrib['name']==name:
                print(e.attrib)
                el = e

    elif(len(el)>1):
        el = el[1]
    #print("{}: {}, {}".format(name, el.text, el.get('units')))
    value = str(val)
    if value.find(':') == -1:
        if splited:
            print("in")
            for i in el:
                print(i.tag)
                if i.tag == splited[-1]:
                    i.text = value
        else:
            el.text = value
    else:
        t, u, v = value.split(':')
        el.set('type', t)
        el.set('units', u)
        el.text = v

def params_to_xml(params, default_xml, xml_out):
    """
    
    :param params: input parameter values dictionary - key is parameter name, value is
    formatted string "type:units:val", or "val".
    """
    root = ET.parse(default_xml)
    for p in params:
        update_param(p, params[p], root)
    root.write(xml_out)

