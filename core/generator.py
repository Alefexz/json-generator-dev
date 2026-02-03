import copy
import uuid
import random
from datetime import datetime


def random_decimal(min_val: float, max_val: float) -> str:
    value = random.uniform(min_val, max_val)
    return f"{value:.2f}"


def random_date_in_month(year: int, month: int) -> str:
    day = random.randint(1, 28)  # evita problema com meses menores
    base_time = datetime.utcnow().time()

    dt = datetime(
        year=year,
        month=month,
        day=day,
        hour=base_time.hour,
        minute=base_time.minute,
        second=base_time.second
    )

    return dt.isoformat() + "Z"


def generate_copies(base_json: dict, quantity: int, options: dict):
    results = []

    for _ in range(quantity):
        data = copy.deepcopy(base_json)

        # _id.$oid
        if options.get("oid"):
            data["_id"]["$oid"] = uuid.uuid4().hex[:24]

        # TransactionId
        if options.get("transaction"):
            data["TransactionId"] = str(uuid.uuid4())

        # ContractNumber (mantém CDP)
        if options.get("contract"):
            data["ContractNumber"] = f"CDP{random.randint(1000000000, 9999999999)}"

        # TotalValue
        if options.get("total_value"):
            min_v, max_v = options["total_value_range"]
            data["FinancialInfos"]["TotalValue"]["$numberDecimal"] = random_decimal(
                min_v, max_v
            )

        # MDRPercent
        if options.get("mdr"):
            data["FinancialInfos"]["MDRPercent"]["$numberDecimal"] = str(
                random.randint(1, 10)
            )

        # CreatedAt
        if options.get("created_at"):
            year = options["year"]
            month = options["month"]
            data["CreatedAt"]["$date"] = random_date_in_month(year, month)

        results.append(data)

    return results
