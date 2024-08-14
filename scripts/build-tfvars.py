import yaml
import json

def yaml_to_tfvars(yaml_file, tfvars_file):
    # Read the YAML file
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)

    # Prepare tfvars data
    tfvars_data = {
        "vnet_name": "",
        "vnet_address_spaces": [],
        "web_subnet_names": [],
        "app_subnet_names": [],
        "data_subnet_names": [],
        "web_cidrs": [],
        "app_cidrs": [],
        "data_cidrs": []
    }

    # Process VNets
    tfvars_data["vnet_name"] = yaml_data['vnet']['name']
    tfvars_data["vnet_address_spaces"].extend(yaml_data['vnet']['address_spaces'])

    # Process Subnets
    for subnet_type, subnets in yaml_data['subnets'].items():
        for subnet in subnets:
            tfvars_data[f"{subnet_type}_subnet_names"].append(subnet['name'])
            tfvars_data[f"{subnet_type}_cidrs"].extend(subnet['cidrs'])

    # Write to tfvars file
    with open(tfvars_file, 'w') as file:
        for key, value in tfvars_data.items():
            file.write(f'{key} = {json.dumps(value)}\n')

    print(f"Successfully generated {tfvars_file}")

# Usage
yaml_to_tfvars('input.yaml', 'terraform.tfvars')