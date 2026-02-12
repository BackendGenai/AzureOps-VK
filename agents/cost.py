def calculate_costs(vms):
    return sum(vm["monthly_cost"] for vm in vms)
