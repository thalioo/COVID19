import xml.etree.ElementTree as ET
import json
import sys

# Usage: python reverse_engineer_xml.py settings.xml output.json

def get_text(element, default=None):
    return element.text if element is not None else default

def main(xml_path, json_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # 1. multiplicity_of_infection
    user_params = root.find('user_parameters')
    moi = user_params.find('multiplicity_of_infection')
    multiplicity_of_infection = float(get_text(moi, 0))

    # 2. oxygen.initial_condition
    oxygen_var = root.find("microenvironment_setup/variable[@name='oxygen']")
    oxygen_init = oxygen_var.find('initial_condition')
    oxygen_initial_condition = float(get_text(oxygen_init, 0))

    # 3. vaccination (reverse from key parameters)
    # Get key vaccination params
    def get_param(name):
        el = user_params.find(name)
        return float(get_text(el, 0)) if el is not None else None

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
    # Pick a few key params for matching
    def match_vaccination():
        keys = [
            'number_of_CD8_Tcells',
            'number_of_CD4_Tcells',
            'number_of_DCs',
            'BN_init',
            'Ig_init',
            'Ig_recuitment',
            'Ig_degradation',
            'Ig_neutralization_rate',
        ]
        values = {k: get_param(k) for k in keys}
        for label, profile in vaccination_profiles.items():
            if all(abs(values[k] - profile[k]) < 1e-6 for k in keys):
                return label
        # fallback: closest match
        best_label = None
        best_score = float('inf')
        for label, profile in vaccination_profiles.items():
            score = sum(abs(values[k] - profile[k]) for k in keys)
            if score < best_score:
                best_score = score
                best_label = label
        return best_label

    vaccination = match_vaccination()

    # 4. Model type (Mild/Severe/etc): infer from cell_definition cfg_filename
    model_types = {
        'epithelial_cell_C141': 'Mild',
        'epithelial_cell_C143': 'Severe',
        'epithelial_cell_2025': 'Wild Type',
        'epithelial_cell_C141_FADDko': 'Mild KO',
        'epithelial_cell_C143_FADDko': 'Severe KO',
        'epithelial_cell_2025_FADDko': 'Wild Type KO',
        'epithelial_cell_C141_FADDko': 'Mild FADDKO',
        'epithelial_cell_C143_FADDko': 'Severe FADDKO',
        'epithelial_cell_2025_FADDko': 'Wild Type FADDKO',
        'epithelial_cell_C141': 'Mild P38KO',
        'epithelial_cell_C143': 'Severe P38KO',
        'epithelial_cell_2025': 'Wild Type P38KO',
    }
    cell_defs = root.find('cell_definitions')
    model_type = None
    if cell_defs is not None:
        for cell_def in cell_defs.findall("cell_definition"):
            if cell_def.attrib.get('name') == 'lung epithelium':
                intracellular = cell_def.find('phenotype/intracellular')
                if intracellular is not None:
                    cfg_filename = intracellular.find('cfg_filename')
                    if cfg_filename is not None and cfg_filename.text:
                        for key in model_types:
                            if key in cfg_filename.text:
                                model_type = model_types[key]
                                break
    # Compose output
    result = {
        'multiplicity_of_infection': multiplicity_of_infection,
        'oxygen.initial_condition': oxygen_initial_condition,
        'model_type': model_type,
        'vaccination': vaccination
    }
    with open(json_path, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Wrote: {json_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python reverse_engineer_xml.py settings.xml output.json")
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])
