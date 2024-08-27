from typing import Dict, Any, List
from hypergo.transaction import Transaction
from hypergo.utility import organize_tokens

__all__ = ["converge"]


def converge(input_keys: List[str], routingkey: str, payload: Any, transaction: Transaction) -> Dict[str, Any]:
    merged_data = {}
    transaction.set(routingkey, payload)
    for input_key in input_keys:
        input_key = organize_tokens(input_key)
        merged_data[input_key] = transaction.get(input_key, None)
        if not merged_data[input_key]:
            return
    return merged_data


if __name__ == "__main__":
    tx = Transaction()
    result = None
    result = converge(["b.a.c", "x.y.z"], "a.b.c", "First Message", tx)
    result = converge(["b.a.c", "x.y.z"], "x.y.z", "Second Message", tx)
    print(result)
