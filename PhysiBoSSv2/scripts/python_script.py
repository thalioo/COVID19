from pandas import DataFrame

# Mandatory main function. This example expects a single input followed by the
# parameter dictionary.
table ={
  "name": "Custom Python Transformer",
  "dropSpecial": False,
  "parameters": [
    {
      "name": "Vaccined",
      "type": "boolean",
      "description": "By default parameters are of type string.",
      "optional": True
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
        "Severe",
        "Mild",
        "Wild Type"
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
def rm_main(data, parameters):
	# Create a new data frame containing parameters.
	table = DataFrame({
		'Key': list(parameters.keys()),
		'Value': list(parameters.values())
	})
	print(table)
 # Find the "Vaccined" parameter in the list
    vaccined_param = next((param for param in parameters if param["name"] == "Vaccined"), None)
    if vaccined_param and vaccined_param.get("value") == True:
        print("Vaccined")

	# Return the new data frame and pass through the input data.
	return table, data


rm_main([], table)