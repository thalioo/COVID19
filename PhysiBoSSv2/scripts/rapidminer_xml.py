import xml.etree.ElementTree as ET
import json
import os

xml_file = "/home/tntiniak/Work/Covid-19/new/PhysiBoSSv2/config/tester.xml"
tree = ET.parse(xml_file)
root = tree.getroot()
condition = "mild"
suffix = "_C141" if condition == "mild" else "_C143"
ko = True
table = {
  "parameters": [
    {
      "name": "1st_parameter",
      "type": "string",
      "description": "By default parameters are of type string.",
      "optional": true
    },
    {
      "name": "2nd_parameter",
      "type": "integer",
      "description": "This is an example of an mandatory integer parameter with a default value 100.",
      "value": 100
    },
    {
      "name": "3rd_parameter",
      "type": "category",
      "description": "An example of a categorical parameter.",
      "categories": [
        "Category A",
        "Category B",
        "Category C",
        "Default Category"
      ],
      "value": "Default Category"
    }
  ]

}
for elem in root.iter():
    # print(elem.tag)
    if elem.get("name") == 'lung epithelium':
        print(f"Found 'lung epithelium' tag: {ET.tostring(elem, encoding='unicode')}")
    if elem.tag == 'intracellular':
        print(f"Found 'extracellular' tag: {ET.tostring(elem, encoding='unicode')}")

for cell_def in root.findall(".//cell_definitions//cell_definition"):
    cell_name = cell_def.get("name")
    if cell_name == "lung epithelium" or cell_name=="macrophage":
    # Find intracellular tag inside phenotype
        intracellular = cell_def.find(".//phenotype//intracellular")
        if intracellular is not None:
            # Modify bnd and cfg filenames
            bnd = intracellular.find("bnd_filename")
            cfg = intracellular.find("cfg_filename")
            if bnd is not None:
                base, ext = bnd.text.rsplit(".", 1)
                print(f"base: {base}, ext: {ext}")
                bnd.text = f"{base}{suffix}.{ext}"
            if cfg is not None:
                base, ext = cfg.text.rsplit(".", 1)
                cfg.text = f"{base}{suffix}.{ext}"

            print(f"Updated intracellular for '{cell_name}':")
            print(f"  - bnd_filename: {bnd.text}")
            print(f"  - cfg_filename: {cfg.text}")
# parameter 1 maps to personalization
    # category a :mild patient
    # category b :severe patient
    # category c :NOT PERSONALIZED

# C141	Mild patient
# C143	Severe patient

# parameter 2 maps to the concentration of the virus
    # Category 1 : low concentration
    # Category 2 : high concentration
    # Category 3 : very high concentration
# parameter 3 maps to the immunization or not
    # Category 1 : immunized
    # Category 2 : not immunized    

# if parameter.personalization == "a":
#     boolean_model = 
# elif parameter.personalization == "b":
# elif parameter.personalization == "c":parameters