from agents.ingestion_agent import ingest_vm_data
from agents.usage_analysis_agent import analyze_usage
from agents.cost import calculate_costs
from agents.rightsizing import recommend_rightsizing
from agents.response_agent import assemble_response


def run_pipeline():

    vms = ingest_vm_data()

    total_cost = calculate_costs(vms)

    rightsizing = recommend_rightsizing(vms)

    total_savings = sum(r["savings"] for r in rightsizing)

    used_capacity = sum(vm["cpu_usage"] for vm in vms) / len(vms)

    return {
        "metrics": {
            "total_cost": total_cost,
            "cost_savings": total_savings,
            "used_capacity": round(used_capacity, 2)
        },
        "vms": vms,
        "rightsizing": rightsizing
    }
