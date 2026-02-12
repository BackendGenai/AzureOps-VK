def analyze_usage(vms):
    for vm in vms:
        vm["avg_utilization"] = (
            vm["cpu_usage"] + vm["memory_usage"]
        ) / 2
    return vms
