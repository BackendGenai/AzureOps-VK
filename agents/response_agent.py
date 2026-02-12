def assemble_response(vms, total_cost, rightsizing):
    count = len(vms)

    avg_capacity = (
        sum(vm["avg_utilization"] for vm in vms) / count
        if count else 0
    )

    savings = sum(
        r.get("estimated_savings", 0) for r in rightsizing
    )

    return {
        "metrics": {
            "total_cost": round(total_cost, 2),
            "cost_savings": round(savings, 2),
            "used_capacity": round(avg_capacity, 2)
        },
        "vms": vms,
        "rightsizing": rightsizing
    }
