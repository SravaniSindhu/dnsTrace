import dns.resolver

DNS_PROVIDERS = {
"google": ["8.8.8.8", "8.8.4.4"],
"cloudflare": ["1.1.1.1", "1.0.0.1"],
"opendns": ["208.67.222.222", "208.67.220.220"],
"safedns": ["195.46.39.39", "195.46.39.40"]
}

SUPPORTED_TYPES = [
"A", "AAAA", "MX", "TXT", "NS", "CNAME", "CAA", "SRV"
]

def resolve_domain(domain, record_type, provider="google"):

    results = {}

    resolver = dns.resolver.Resolver()

    resolver.nameservers = DNS_PROVIDERS.get(provider, DNS_PROVIDERS["google"])

    resolver.timeout = 2
    resolver.lifetime = 3

    if record_type == "ALL":
        types_to_query = SUPPORTED_TYPES
    else:
        types_to_query = [record_type]

    for rtype in types_to_query:

        try:
            answers = resolver.resolve(domain, rtype)
            records = []
            for r in answers:
                record = {
                    "value": str(r),
                    "ttl": answers.rrset.ttl
                }

                if rtype == "MX":
                    record["priority"] = r.preference

                if rtype == "SRV":
                    record["priority"] = r.priority
                    record["port"] = r.port

                records.append(record)

            results[rtype] = records

        except Exception:
            continue

    return results
