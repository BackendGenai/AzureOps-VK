def recommend_rightsizing(vms):

    recommendations = []

    for vm in vms:

        cpu = vm.get("cpu_usage", 0)
        memory = vm.get("memory_usage", 0)
        cost = vm.get("monthly_cost", 0)

        # Rightsizing Logic
        if cpu < 30 and memory < 40:
            action = "Downsize"
            new_cost = cost * 0.7
            savings = cost - new_cost

        elif cpu > 80 or memory > 85:
            action = "Upsize"
            new_cost = cost * 1.3
            savings = 0

        else:
            action = "No Change"
            new_cost = cost
            savings = 0

        recommendations.append({
            "vm_id": vm["vm_id"],
            "cpu_usage": cpu,
            "memory_usage": memory,
            "current_cost": cost,
            "recommended_cost": round(new_cost, 2),
            "savings": round(savings, 2),
            "action": action
        })

    return recommendations
