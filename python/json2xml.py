import xml.etree.ElementTree as ET
import json
import argparse

def update_param(path, value, root):
    parts = path.split('.')

    # === 1. Special case: cell_definition with [@name=...] ===
    # Handle special model mapping cases
    if path.startswith("cell_definition[@name='lung epithelium'].intracellular.cfg_filename") or \
       path.startswith("cell_definition[@name='macrophage'].intracellular.cfg_filename"):

        cell_name = path.split("[@name='")[1].split("']")[0]
        cfg_val = str(value)

        for cell_def in root.findall(f".//cell_definition[@name='{cell_name}']"):
            intracellular = cell_def.find(".//intracellular")
            if intracellular is not None:
                cfg_filename = intracellular.find("cfg_filename")
                if cfg_filename is not None:
                    cfg_filename.text = cfg_val
                else:
                    print(f"cfg_filename tag missing under {cell_name}")
        return
    if parts[0].startswith("cell_definition[@name="):
        tag = parts[0].split("[@name=")[0]
        name = parts[0].split("[@name=")[1].strip("']").strip('"')
        sub_path = parts[1:]

        for cd in root.findall(f".//{tag}"):
            if cd.get("name") == name:
                current = cd
                for subtag in sub_path:
                    current = current.find(subtag)
                    if current is None:
                        return
                current.text = str(value)
                return
        return

    # === 2. microenvironment_setup.variable.oxygen.XXX ===
    elif parts[0] == "microenvironment_setup" and parts[1] == "variable" and parts[2] == "oxygen":
        param_name = parts[3]
        for var in root.findall(".//microenvironment_setup//variable"):
            if var.get("name") == "oxygen":
                target = var.find(param_name)
                if target is not None:
                    target.text = str(value)
                    return
        return

    # === 3. user_parameters.XXX ===
    elif parts[0] == "user_parameters":
        param_name = parts[1]
        user_params = root.find(".//user_parameters")
        if user_params is not None:
            target = user_params.find(param_name)
            if target is not None:
                target.text = str(value)
                return

        # fallback: check custom_data in default cell_definition
        for cd in root.findall(".//cell_definition[@name='default']"):
            custom = cd.find(".//custom_data")
            if custom is not None:
                target = custom.find(param_name)
                if target is not None:
                    target.text = str(value)
                    return

        return



def json_to_xml(params, default_xml, xml_out):
    """
    
    :param params: input parameter values dictionary - key is parameter name, value is
    formatted string "type:units:val", or "val".
    """
    root = ET.parse(default_xml)
    for p in params:
        update_param(p, params[p], root)
    root.write(xml_out)
