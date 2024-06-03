from typing import Dict, Any, List
from hypergo.transaction import Transaction

__all__ = ["merge_transactions", "converge"]


def converge(routingkeys: List[str], routingkey: str, payload: Any, transaction: Transaction) -> Dict[str, Any]:
    merged_data = {}
    transaction.set(routingkey, payload)
    for rk in routingkeys:
        merged_data[rk] = transaction.get(rk, None)
        if not merged_data[rk]:
            return
    return merged_data


if __name__ == "__main__":
    tx = Transaction()
    result = None
    result = converge(["a.b.c", "x.y.z"], "a.b.c", "First Message", tx)
    result = converge(["a.b.c", "x.y.z"], "x.y.z", "Second Message", tx)
    print(result)
