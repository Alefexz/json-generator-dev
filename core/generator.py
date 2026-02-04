import copy
import random
from datetime import datetime
import calendar


def generate_copies(
    base_json,
    quantity,
    month,
    value_range,
    seller_uuid_override=None
):
    results = []

    month_map = {
        "Janeiro": 1,
        "Fevereiro": 2,
        "Março": 3,
        "Abril": 4,
        "Maio": 5,
        "Junho": 6,
        "Julho": 7,
        "Agosto": 8,
        "Setembro": 9,
        "Outubro": 10,
        "Novembro": 11,
        "Dezembro": 12,
    }

    year = datetime.now().year
    month_number = month_map[month]
    last_day = calendar.monthrange(year, month_number)[1]

    for _ in range(quantity):
        new_json = copy.deepcopy(base_json)

        # -------- CREATE AT --------
        day = random.randint(1, last_day)
        created_at = datetime(year, month_number, day, 12, 0, 0)
        new_json["createAt"] = created_at.isoformat()

        # -------- TOTAL VALUE --------
        min_val, max_val = value_range
        new_json["totalValue"] = round(random.uniform(min_val, max_val), 2)

        # -------- SELLER UUID --------
        if seller_uuid_override:
            new_json["seller_uuid"] = seller_uuid_override

        results.append(new_json)

    return results
