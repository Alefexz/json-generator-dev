import copy
import random
from datetime import datetime

def generate_copies(
    base_json,
    quantity,
    month,
    value_range,
    seller_uuid_override=None
):
    results = []

    for i in range(quantity):
        new_json = copy.deepcopy(base_json)

        # TotalValue
        if value_range == "50 a 100":
            total_value = round(random.uniform(50, 100), 2)
        elif value_range == "100 a 150":
            total_value = round(random.uniform(100, 150), 2)
        else:
            total_value = round(random.uniform(150, 300), 2)

        new_json["FinancialInfos"]["TotalValue"]["$numberDecimal"] = str(total_value)

        # MDRPercent aleatório
        new_json["FinancialInfos"]["MDRPercent"]["$numberDecimal"] = str(
            round(random.uniform(1, 10), 2)
        )

        # CreatedAt (Janeiro)
        day = random.randint(1, 28)
        created_at = datetime(2026, 1, day, 12, 0, 0).isoformat() + "Z"
        new_json["CreatedAt"]["$date"] = created_at

        # Seller UUID (opcional)
        if seller_uuid_override:
            new_json["SellerUuid"] = seller_uuid_override

        results.append(new_json)

    return results
