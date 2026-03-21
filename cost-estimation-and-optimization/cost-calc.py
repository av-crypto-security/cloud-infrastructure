import math

MINUTES_PER_MONTH = 60 * 24 * 30


def monitoring_cost(metrics, values_per_minute, price_per_million=9.8):
    total_values = metrics * values_per_minute * MINUTES_PER_MONTH
    millions = total_values / 1_000_000
    cost = millions * price_per_million

    return {
        "total_values": total_values,
        "millions": round(millions, 3),
        "cost_units": round(cost, 2)
    }


def vm_cost_estimate(cpu, ram_gb, hours=720):
    # Simplified model (approximate)
    cpu_price = 2.5   # units/hour for vCPU
    ram_price = 0.5   # units/hour for GB

    cost = hours * (cpu * cpu_price + ram_gb * ram_price)

    return round(cost, 2)


if __name__ == "__main__":
    m = monitoring_cost(metrics=35, values_per_minute=2)
    print("Monitoring:", m)

    vm = vm_cost_estimate(cpu=4, ram_gb=16)
    print("VM estimate:", vm)