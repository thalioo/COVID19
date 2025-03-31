import xml.etree.ElementTree as ET
from pandas import DataFrame

table  = {
  "name": "Custom Python Transformer",
  "dropSpecial": False,
  "parameters": [
    {
      "name": "vaccinated",
      "type": "category",
      "description": "An example of a categorical parameter.",
      "categories": [
        "fully_vaccinated",
        "mildly_vaccinated",
        "non_vaccinated"
      ],
      "value": "fully_vaccinated"
    },
    {
      "name": "multiplicity_of_infection",
      "type": "integer",
      "description": "This is an example of an mandatory integer parameter with a default value 100.",
      "value": 1
    },
    {
      "name": "patient_type",
      "type": "category",
      "description": "An example of a categorical parameter.",
      "categories": [
        "Mild",
        "Severe",
        "Wild Type",
        "Mild KO",
        "Severe KO",
        "Wild Type KO",
        "Mild FADDKO",
        "Severe FADDKO"
        "Wild Type FADDKo",
        "Mild P38KO",
        "Severe P38KO",
        "Wild Type P38KO"
      ],
      "value": "Wild Type"
    }
  ],
  "inputs": [
    {
      "name": "data",
      "type": "table"
    }
  ],
  "outputs": [
    {
      "name": "out",
      "type": "table"
    },
    {
      "name": "through",
      "type": "table"
    }
  ]
}
vaccinated_scenarios = {
        'fully_vaccinated': {
            'number_of_CD8_Tcells': 100,
            'number_of_CD4_Tcells': 100,
            'number_of_DCs': 50,
            'BN_init': 5000,
            'Ig_init': 1000,
            'Ig_recuitment': 5,
            'Ig_degradation': 0.0005,
            'Ig_neutralization_rate': 10,
            'BCell_activation': 0.01,
            'BCell_DC_proliferation': 0.01,
            'PCell_recuitment': 0.001,
            'TC_activation': 0.01,
            'DC_induced_CD8_proliferation': 0.01,
            'max_activation_TC': 0.01,
            'DC_leave_prob': 0.00001,
            'virions_needed_for_DC_activation': 5,
            'interferon_secretion_rate_via_infection': 0.1,
            'activated_cytokine_secretion_rate': 20,
        },
        'mildly_vaccinated': {
            'number_of_CD8_Tcells': 50,
            'number_of_CD4_Tcells': 50,
            'number_of_DCs': 30,
            'BN_init': 2500,
            'Ig_init': 500,
            'Ig_recuitment': 2,
            'Ig_degradation': 0.0008,
            'Ig_neutralization_rate': 5,
            'BCell_activation': 0.005,
            'BCell_DC_proliferation': 0.005,
            'PCell_recuitment': 0.0005,
            'TC_activation': 0.005,
            'DC_induced_CD8_proliferation': 0.005,
            'max_activation_TC': 0.005,
            'DC_leave_prob': 0.00002,
            'virions_needed_for_DC_activation': 7,
            'interferon_secretion_rate_via_infection': 0.05,
            'activated_cytokine_secretion_rate': 10,
        },
        'non_vaccinated': {
            'number_of_CD8_Tcells': 0,
            'number_of_CD4_Tcells': 0,
            'number_of_DCs': 28,
            'BN_init': 1000,
            'Ig_init': 0,
            'Ig_recuitment': 1,
            'Ig_degradation': 0.00139,
            'Ig_neutralization_rate': 3,
            'BCell_activation': 0.0021,
            'BCell_DC_proliferation': 0.002,
            'PCell_recuitment': 0.0002,
            'TC_activation': 0.001,
            'DC_induced_CD8_proliferation': 0.00208,
            'max_activation_TC': 0.0018,
            'DC_leave_prob': 0.000033,
            'virions_needed_for_DC_activation': 10,
            'interferon_secretion_rate_via_infection': 0.01,
            'activated_cytokine_secretion_rate': 10,
        }
    }
def modify_xml(xml_path, output_path, patient_type=None,vaccinated = False,virus=0):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    
    # Define model mappings based on patient type
    model_mappings = {
        "Mild": ["epithelial_cell_C141", "macrophage_C141"],
        "Severe": ["epithelial_cell_C143", "macrophage_C143"],
        "Wild Type": ["epithelial_cell", "macrophage_2025"],
        "Mild KO": ["epithelial_cell_C141_FADDko", "macrophage_C141_p38ko"],
        "Severe KO": ["epithelial_cell_C143_FADDko", "macrophage_C143_p38ko"],
        "Wild Type KO": ["epithelial_cell_2025_FADDko", "macrophage_2025_p38ko"],
        "Mild FADDKO": ["epithelial_cell_C141_FADDko", "macrophage_C141"],
        "Severe FADDKO": ["epithelial_cell_C143_FADDko", "macrophage_C143"],
        "Wild Type FADDKO": ["epithelial_cell_2025_FADDko", "macrophage_2025"],
        "Mild P38KO": ["epithelial_cell_C141", "macrophage_C141"],
        "Severe P38KO": ["epithelial_cell_C143", "macrophage_C143"],
        "Wild Type P38KO": ["epithelial_cell_2025", "macrophage_2025"]
    }
    
    if patient_type in model_mappings:
        # print(patient_type)
        selected_models = model_mappings[patient_type]
        
        for cell_definition in root.findall(".//cell_definition[@name='lung epithelium']"):
            intracellular = cell_definition.find(".//intracellular")
    
            if intracellular is not None:
                cfg_filename = intracellular.find('cfg_filename')
                if cfg_filename is not None:
                    cfg_filename.text = './config/boolean/' + selected_models[0] + '.cfg'  # New filename path
        for cell_definition in root.findall(".//cell_definition[@name='macrophage']"):
            intracellular = cell_definition.find(".//intracellular")
    
            if intracellular is not None:
                cfg_filename = intracellular.find('cfg_filename')
                if cfg_filename is not None:
                    cfg_filename.text = './config/boolean/' + selected_models[1] + '.cfg'  # New filename path
    multiplicity_element = root.find(".//user_parameters//div_initialization//multiplicity_of_infection")
    if multiplicity_element is not None:
        multiplicity_element.text = str(virus)  # Set the new value (convert virus to string if necessary)
    for param, value in vaccinated_scenarios[vaccinated].items():
        user_params = root.find(".//user_parameters")
        elem = user_params.find(param)
        if elem is not None:
            elem.text = str(value)
        else:
            for cell_definition in root.findall(".//cell_definition[@name='default']"):
                custom = cell_definition.find(".//custom_data")
                elem =custom.find(param)
                if elem is not None:
                    elem.text = str(value)
                else:
                    print(f"Warning: Parameter '{param}' not found in XML.")
            
    # user_parameters//div_initialization//multiplicity_of_infection
    # Save modified XML
    tree.write(output_path)
    # return tree 
    print(f"Modified XML saved to {output_path}")


# Example usage



# Mandatory main function. This example expects a single input followed by the
# parameter dictionary.
def rm_main(data, parameters):
	# Create a new data frame containing parameters.
    # table = DataFrame({
    #     'Key': list(parameters.keys()),
    #     'Value': list(parameters.values())
    # })
    # print(table["parameters"])
    print(parameters['parameters'])
    modify_xml("./config/tester.xml", "input.xml", patient_type = table["parameters"][2]["value"], vaccinated=table["parameters"][0]["value"], virus=table["parameters"][1]["value"])
	# Return the new data frame and pass through the input data.
    return table, data

rm_main(table, table)