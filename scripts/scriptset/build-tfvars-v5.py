import yaml
import json
import sys
import ipaddress

# Define the sizing strategy
SIZING_STRATEGY = {
    'XS': {'vnet': 24, 'subnets': 26},
    'S':  {'vnet': 23, 'subnets': 25},
    'M':  {'vnet': 22, 'subnets': 24},
    'L':  {'vnet': 21, 'subnets': 23},
    'XL': {'vnet': 20, 'subnets': 22},
    'XXL': {'vnet': 19, 'subnets': 21}
}

def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def save_yaml(data, file_path):
    with open(file_path, 'w') as file:
        yaml.dump(data, file, default_flow_style=False)

def allocate_cidr(cidr_pools, size):
    vnet_size = SIZING_STRATEGY[size]['vnet']
    if str(vnet_size) not in cidr_pools['available'] or not cidr_pools['available'][str(vnet_size)]:
        raise ValueError(f"No available /{vnet_size} CIDR for size {size}")
    
    cidr = cidr_pools['available'][str(vnet_size)].pop(0)
    if str(vnet_size) not in cidr_pools['allocated']:
        cidr_pools['allocated'][str(vnet_size)] = []
    cidr_pools['allocated'][str(vnet_size)].append(cidr)
    return cidr

def generate_subnets(cidr, subnet_size):
    network = ipaddress.ip_network(cidr)
    subnets = list(network.subnets(new_prefix=subnet_size))
    return {
        'web': str(subnets[0]),
        'app': str(subnets[1]),
        'data': str(subnets[2])
    }

def get_next_subnet_number(vnet_subnets, base_name):
    max_num = 0
    for subnet in vnet_subnets:
        if subnet['name'].startswith(base_name):
            parts = subnet['name'].rsplit('-', 1)
            if len(parts) == 2 and parts[1].isdigit():
                num = int(parts[1])
                if num > max_num:
                    max_num = num
    return max_num + 1

def persist_vnet_details(vnet_name, vnet_address_spaces, subnets, yaml_file):
    data = load_yaml(yaml_file)
    
    if 'vnet' not in data:
        data['vnet'] = {}

    if vnet_name not in data['vnet']:
        data['vnet'][vnet_name] = {
            'cidr': vnet_address_spaces[0],
            'address_spaces': vnet_address_spaces,
            'subnets': []
        }
    else:
        data['vnet'][vnet_name]['address_spaces'] = vnet_address_spaces

    vnet_subnets = data['vnet'][vnet_name]['subnets']

    for subnet_name, cidr in subnets.items():
        base_name = f"{vnet_name}-{subnet_name}-subnet"
        next_subnet_num = get_next_subnet_number(vnet_subnets, base_name)
        new_subnet_name = f"{base_name}-{next_subnet_num}"
        vnet_subnets.append({
            'name': new_subnet_name,
            'cidr': cidr
        })
    
    save_yaml(data, yaml_file)

def generate_tfvars(vnet_name, cidr_pools_file, vnet_size, extend_vnet, vnet_details_file):
    cidr_pools = load_yaml(cidr_pools_file)
    vnet_data = load_yaml(vnet_details_file)

    # Check if VNet already exists and if extend_vnet is false, raise an error
    if not extend_vnet and vnet_name in vnet_data.get('vnet', {}):
        print(f"Error: VNet '{vnet_name}' has already been provisioned. Use 'true' for extend_vnet to add more address spaces.")
        sys.exit(1)

    vnet_address_spaces = []
    
    if extend_vnet and vnet_name in vnet_data.get('vnet', {}):
        vnet_address_spaces = vnet_data['vnet'][vnet_name]['address_spaces']
        additional_vnet_cidr = allocate_cidr(cidr_pools, vnet_size)
        vnet_address_spaces.append(additional_vnet_cidr)
    else:
        primary_vnet_cidr = allocate_cidr(cidr_pools, vnet_size)
        vnet_address_spaces.append(primary_vnet_cidr)

    # Generate subnets from the last allocated CIDR (for extension or initial creation)
    subnet_size = SIZING_STRATEGY[vnet_size]['subnets']
    subnets = generate_subnets(vnet_address_spaces[-1], subnet_size)

    # Prepare tfvars data
    vnet_subnets = vnet_data.get('vnet', {}).get(vnet_name, {}).get('subnets', [])
    tfvars_data = {
        "vnet_name": vnet_name,
        "vnet_address_spaces": vnet_address_spaces,
        "subnet_details": []
    }
    
    print(tfvars_data)
    # Write to tfvars file
    # Save updated CIDR pools and persist VNet details
    save_yaml(cidr_pools, cidr_pools_file)
    persist_vnet_details(vnet_name, vnet_address_spaces, subnets, vnet_details_file)

    vnet_data = load_yaml(vnet_details_file)
    vnet_subnets = vnet_data.get('vnet', {}).get(vnet_name, {}).get('subnets', [])
    for vnet_subnet in vnet_subnets:
        tfvars_data['subnet_details'].append(vnet_subnet)
    print(tfvars_data)

    with open('terraform.tfvars', 'w') as file:
        for key, value in tfvars_data.items():
            file.write(f'{key} = {json.dumps(value)}\n')

    print(f"Successfully generated terraform.tfvars")
    print(f"Allocated CIDR(s) to VNet: {vnet_address_spaces}")
    print(f"Generated subnets: {subnets}")

if __name__ == "__main__":
    if len(sys.argv) != 6:
        print("Usage: python script.py <vnet_name> <cidr_pools_yaml> <vnet_size> <extend_vnet> <vnet_details_yaml>")
        sys.exit(1)

    vnet_name = sys.argv[1]
    cidr_pools_file = sys.argv[2]
    vnet_size = sys.argv[3].upper()  # Convert to uppercase
    extend_vnet = sys.argv[4].lower() == 'true'
    vnet_details_file = sys.argv[5]

    if vnet_size not in SIZING_STRATEGY:
        print(f"Invalid size. Choose from: {', '.join(SIZING_STRATEGY.keys())}")
        sys.exit(1)

    generate_tfvars(vnet_name, cidr_pools_file, vnet_size, extend_vnet, vnet_details_file)
