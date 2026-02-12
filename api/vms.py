from fastapi import APIRouter
from data.vm_data import load_vm_data

router = APIRouter()


# ================= DASHBOARD =================

@router.get("/dashboard")
def dashboard():

    vms = load_vm_data()

    total_cost = sum(vm["monthly_cost"] for vm in vms)

    metrics = {
        "total_cost": total_cost,

        "cost_savings":
        total_cost * 0.19,

        "used_capacity": (
            sum(vm["cpu_usage"] for vm in vms) / len(vms) +
            sum(vm["memory_usage"] for vm in vms) / len(vms)
        ) / 2
    }

    return {
        "metrics": metrics,
        "vms": vms[:100]
    }


# ================= VM DETAILS =================

@router.get("/vm/{vm_id}")
def vm_details(vm_id: str):

    vms = load_vm_data()

    for vm in vms:
        if vm["vm_id"].endswith(vm_id):
            return vm

    return {"error": "VM not found"}


# ================= RIGHTSIZING =================

@router.get("/rightsizing")
def rightsizing():

    vms = load_vm_data()

    recommendations = []

    for vm in vms:

        cpu = vm["cpu_usage"]
        mem = vm["memory_usage"]

        utilization = (cpu + mem) / 2

        # ===== Decision Logic =====

        if cpu < 30 and mem < 30:
            action = "Downsize"
            saving = vm["monthly_cost"] * 0.35
            resized_cost = vm["monthly_cost"] - saving

        elif cpu > 80 or mem > 80:
            action = "Upsize"
            saving = -(vm["monthly_cost"] * 0.25)
            resized_cost = vm["monthly_cost"] - saving

        else:
            action = "Optimal"
            saving = 0
            resized_cost = vm["monthly_cost"]

        recommendations.append({
            "vm_id": vm["vm_id"],
            "cpu_usage": cpu,
            "memory_usage": mem,
            "utilization": utilization,

            "current_cost": vm["monthly_cost"],
            "resized_cost": resized_cost,

            "recommendation": action,
            "estimated_saving": saving
        })

    return {
        "total_vms": len(recommendations),
        "recommendations": recommendations[:100]
    }

# ================= ALERTS =================

@router.get("/alerts")
def alerts():

    vms = load_vm_data()

    alerts = []

    for vm in vms:

        # CPU anomaly
        if vm["cpu_usage"] > 85:
            alerts.append({
                "vm_id": vm["vm_id"],
                "type": "High CPU Usage",
                "severity": "Critical",
                "value": vm["cpu_usage"]
            })

        # Memory anomaly
        if vm["memory_usage"] > 85:
            alerts.append({
                "vm_id": vm["vm_id"],
                "type": "High Memory Usage",
                "severity": "Critical",
                "value": vm["memory_usage"]
            })

        # Cost anomaly
        if vm["monthly_cost"] > 250:
            alerts.append({
                "vm_id": vm["vm_id"],
                "type": "High Cost",
                "severity": "Warning",
                "value": vm["monthly_cost"]
            })

    return {
        "total_alerts": len(alerts),
        "alerts": alerts
    }
# ================= ALERTS =================

@router.get("/alerts")
def alerts():

    vms = load_vm_data()

    alert_list = []

    for vm in vms:

        cpu = vm["cpu_usage"]
        mem = vm["memory_usage"]
        cost = vm["monthly_cost"]

        # ===== Alert Logic =====

        if cpu > 85:
            alert_list.append({
                "vm_id": vm["vm_id"],
                "type": "CPU Spike",
                "severity": "High",
                "value": cpu
            })

        if mem > 85:
            alert_list.append({
                "vm_id": vm["vm_id"],
                "type": "Memory Spike",
                "severity": "High",
                "value": mem
            })

        if cpu < 10 and mem < 10:
            alert_list.append({
                "vm_id": vm["vm_id"],
                "type": "Underutilized",
                "severity": "Medium",
                "value": (cpu+mem)/2
            })

        if cost > 300:
            alert_list.append({
                "vm_id": vm["vm_id"],
                "type": "High Cost",
                "severity": "Medium",
                "value": cost
            })

    return {
        "total_alerts": len(alert_list),
        "alerts": alert_list[:100]
    }
