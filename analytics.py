import pandas as pd

def equipment_usage_stats(issued):
    return issued["equipment_name"].value_counts()

def issued_metrics(issued):
    return {
        "total_issued": len(issued),
        "active": len(issued[issued["status"] == "issued"]),
        "returned": len(issued[issued["status"] == "returned"])
    }

    