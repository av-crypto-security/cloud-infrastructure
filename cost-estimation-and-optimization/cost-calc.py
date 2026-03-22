# This is a simplified cost model for estimation purposes only.
# It is not connected to real cloud billing APIs.

MINUTES_PER_MONTH = 60 * 24 * 30


def monitoring_cost(metrics, values_per_minute, price_per_million=9.8):
    total_values = metrics * values_per_minute * MINUTES_PER_MONTH
    millions = total_values / 1_000_000
    cost = millions * price_per_million

    return {
        "metrics": metrics,
        "values_per_minute": values_per_minute,
        "total_values": total_values,
        "millions": round(millions, 3),
        "cost_units": round(cost, 2)
    }


def vm_cost_model(cpu, ram_gb, hours=720):
    cpu_price = 2.5   # units/hour per vCPU
    ram_price = 0.5   # units/hour per GB

    cost = hours * (cpu * cpu_price + ram_gb * ram_price)

    return {
        "cpu": cpu,
        "ram_gb": ram_gb,
        "monthly_cost": round(cost, 2)
    }


def scenario_analysis():
    scenarios = [
        {"name": "low", "metrics": 10, "freq": 1},
        {"name": "baseline", "metrics": 35, "freq": 2},
        {"name": "high", "metrics": 100, "freq": 5},
    ]

    results = []

    for s in scenarios:
        results.append({
            "scenario": s["name"],
            "monitoring": monitoring_cost(s["metrics"], s["freq"])
        })

    return results


if __name__ == "__main__":
    print("=== Monitoring Scenarios ===")
    for r in scenario_analysis():
        print(r)

    print("\n=== VM Models ===")
    configs = [
        {"cpu": 2, "ram": 4},
        {"cpu": 4, "ram": 16},
        {"cpu": 8, "ram": 32},
    ]

    for c in configs:
        print(vm_cost_model(c["cpu"], c["ram"]))
