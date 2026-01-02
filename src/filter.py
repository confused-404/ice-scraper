def eliminate_non_dairy(payload: dict) -> dict:
    def is_non_dairy(product: dict) -> bool:
        desc = (product.get("description") or "").lower()
        receipt = (product.get("receiptDescription") or "").lower()

        mdecl = product.get("manufacturerDeclarations") or []
        mdecl_l = {str(x).lower() for x in mdecl}

        cats = product.get("categories") or []
        cats_l = {str(x).lower() for x in cats}

        return (
            "non-dairy" in desc or "nondairy" in desc or
            "non dairy" in receipt or
            "vegan" in mdecl_l or
            "non-dairy" in cats_l or "nondairy" in cats_l
        )

    data = payload.get("data") or []
    filtered = [p for p in data if not is_non_dairy(p)]

    out = dict(payload)
    out["data"] = filtered

    if isinstance(out.get("meta"), dict) and isinstance(out["meta"].get("pagination"), dict):
        out["meta"] = dict(out["meta"])
        out["meta"]["pagination"] = dict(out["meta"]["pagination"])
        out["meta"]["pagination"]["total"] = len(filtered)

    return out

def get_product_id(payload: dict) -> str:
    data = payload.get("data") or []
    return data[0]["productId"]
