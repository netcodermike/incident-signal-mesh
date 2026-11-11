from errors import Rejected


def operation(data, normalize):
    signals = normalize({"signals": data["signals"]})["signals"]
    groups, seen = {}, {}
    for signal in signals:
        event_id = signal["id"]
        if event_id in seen:
            if seen[event_id] != signal:
                raise Rejected(409, "Conflicting signal ID")
            continue
        seen[event_id] = signal
        key = signal["service"], signal["fingerprint"]
        group = groups.setdefault(key, {"service": key[0], "fingerprint": key[1], "count": 0,
                                       "rank": signal["rank"], "severity": signal["severity"]})
        group["count"] += 1
        if signal["rank"] > group["rank"]:
            group.update(rank=signal["rank"], severity=signal["severity"])
    ranked = sorted(groups.values(), key=lambda group: (-group["rank"], -group["count"], group["service"], group["fingerprint"]))
    top = ranked[0] if ranked else None
    return {"groups": len(ranked), "incidents": ranked,
            "top": f"{top['service']} / {top['fingerprint']}" if top else None,
            "topSeverity": top["severity"] if top else None, "topSignals": top["count"] if top else 0}
