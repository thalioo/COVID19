import json
import os

# Define vaccinated_scenarios
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

# Define model mappings
model_mappings = {
    "Mild": ["epithelial_cell_C141", "macrophage_C141"],
    "Severe": ["epithelial_cell_C143", "macrophage_C143"],
    "Wild Type": ["epithelial_cell_2025", "macrophage_2025"],

    "Mild p38KO": ["epithelial_cell_C141", "macrophage_C141_p38ko"],
    "Severe p38KO": ["epithelial_cell_C143", "macrophage_C143_p38ko"],
    "Wild Type p38KO": ["epithelial_cell_2025", "macrophage_2025_p38ko"],

    "Mild AKT1_FADD_MAPK14 KO": ["epithelial_cell_C141_AKT1_FADD_MAPK14_ko", "macrophage_C141"],
    "Severe AKT1_FADD_MAPK14 KO": ["epithelial_cell_C143_AKT1_FADD_MAPK14_ko", "macrophage_C143"],
    "Mild ALL KO ": ["epithelial_cell_C141_AKT1_FADD_MAPK14_ko", "macrophage_C141_p38ko"],
    "Severe ALL KO ": ["epithelial_cell_C143_AKT1_FADD_MAPK14_ko", "macrophage_C143_p38ko"],
    
    
    
    "Mild FADDKO": ["epithelial_cell_C141_FADDko", "macrophage_C141"],
    "Mild FADDKO p38ko": ["epithelial_cell_C141_FADDko", "macrophage_C141_p38ko"],
    "Severe FADDKO": ["epithelial_cell_C143_FADDko", "macrophage_C143"],
    "Severe FADDKO p38ko": ["epithelial_cell_C143_FADDko", "macrophage_C143_p38ko"],
    "Wild Type FADDKO": ["epithelial_cell_2025_FADDko", "macrophage_2025"],
    "Wild Type FADD p38KO": ["epithelial_cell_2025_FADDko", "macrophage_2025_p38ko"],

    "Mild AKT1KO": ["epithelial_cell_C141_AKT1ko", "macrophage_C141"],
    "Severe AKT1KO": ["epithelial_cell_C143_AKT1ko", "macrophage_C143"],
    "Mild AKT1KO p38ko": ["epithelial_cell_C141_AKT1ko", "macrophage_C141_p38ko"],
    "Severe AKT1KO p38ko": ["epithelial_cell_C143_AKT1ko", "macrophage_C143_p38ko"],

    "Mild MAPK14KO": ["epithelial_cell_C141_MAPK14ko", "macrophage_C141"],
    "Severe MAPK14KO": ["epithelial_cell_C143_MAPK14ko", "macrophage_C143"],
    "Mild MAPK14KO p38ko": ["epithelial_cell_C141_MAPK14ko", "macrophage_C141_p38ko"],
    "Severe MAPK14KO p38ko": ["epithelial_cell_C143_MAPK14ko", "macrophage_C143_p38ko"],

    "Mild MAPK14 AKT1KO": ["epithelial_cell_C141_MAPK14_AKT1ko", "macrophage_C141"],
    "Severe MAPK14 AKT1KO": ["epithelial_cell_C143_MAPK14_AKT1ko", "macrophage_C143"],
    "Mild MAPK14 AKT1KO p38ko": ["epithelial_cell_C141_MAPK14_AKT1ko", "macrophage_C141_p38ko"],
    "Severe MAPK14 AKT1KO p38ko": ["epithelial_cell_C143_MAPK14_AKT1ko", "macrophage_C143_p38ko"],
    
    "Mild MAPK14 FADDKO": ["epithelial_cell_C141_MAPK14_FADDko", "macrophage_C141"],
    "Severe MAPK14 FADDKO": ["epithelial_cell_C143_MAPK14_FADDko", "macrophage_C143"],
    "Mild MAPK14 FADDKO p38ko": ["epithelial_cell_C141_MAPK14_FADDko", "macrophage_C141_p38ko"],
    "Severe MAPK14 FADDKO p38ko": ["epithelial_cell_C143_MAPK14_FADDko", "macrophage_C143_p38ko"],

    "Mild AKT1 FADDKO": ["epithelial_cell_C141_AKT1_FADDko", "macrophage_C141"],
    "Severe AKT1 FADDKO": ["epithelial_cell_C143_AKT1_FADDko", "macrophage_C143"],
    "Mild AKT1 FADDKO p38ko": ["epithelial_cell_C141_AKT1_FADDko", "macrophage_C141_p38ko"],
    "Severe AKT1 FADDKO p38ko": ["epithelial_cell_C143_AKT1_FADDko", "macrophage_C143_p38ko"]
}

# Multiplicities to consider
multiplicities = [0, 5, 10, 20, 40, 50, 70, 80, 90,100]
oxygen = [25,38,60,75,100]
# Output file path
output_path = "combinations_correct.jsonl"

# Start generating combinations
with open(output_path, 'w') as f:
    for vac_label, vac_params in vaccinated_scenarios.items():
        for model_label, (epithelial_cfg, macrophage_cfg) in model_mappings.items():
            for multiplicity in multiplicities:
                for oxy in oxygen:
                    combo = {}

                    # Add multiplicity
                    combo["user_parameters.multiplicity_of_infection"] = multiplicity
                    combo['microenvironment_setup.variable.oxygen.initial_condition'] = oxy
                    combo['microenvironment_setup.variable.oxygen.Dirichlet_boundary_condition']=oxy
                    # Add model mapping paths
                    combo["cell_definition[@name='lung epithelium'].intracellular.cfg_filename"] = f"../boolean_network/{epithelial_cfg}.cfg"
                    combo["cell_definition[@name='macrophage'].intracellular.cfg_filename"] = f"../boolean_network/{macrophage_cfg}.cfg"

                    # Add vaccinated parameters
                    for param, value in vac_params.items():
                        # Assume parameters go to user_parameters
                        combo[f"user_parameters.{param}"] = value

                    # Dump JSON string
                    f.write(json.dumps(combo) + "\n")

print(f" All combinations saved to {output_path} (total: {3*12*9} lines)")
