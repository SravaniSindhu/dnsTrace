import dns.message
import dns.query
import dns.rdatatype
import dns.resolver
import dns.reversename
import random


ROOT_SERVERS = [
    "198.41.0.4",
    "199.9.14.201",
    "192.33.4.12",
    "199.7.91.13",
    "192.203.230.10"
]


def query(server, name, rdtype):
    q = dns.message.make_query(name, rdtype)
    return dns.query.udp(q, server, timeout=3)


def get_ns_name(ip):
    try:
        rev = dns.reversename.from_address(ip)
        ans = dns.resolver.resolve(rev, "PTR")
        return str(ans[0]).rstrip(".")
    except:
        return ip


def extract_ns(response):
    ns_names = []
    for rrset in response.authority:
        if rrset.rdtype == dns.rdatatype.NS:
            for item in rrset:
                ns_names.append(str(item.target).rstrip("."))
    return ns_names


def resolve_ns_to_ip(ns_list):
    ips = []
    for ns in ns_list:
        try:
            answers = dns.resolver.resolve(ns, "A")
            for r in answers:
                ips.append(r.to_text())
        except:
            pass
    return ips


def extract_answer(response):
    return [item.to_text() for rrset in response.answer for item in rrset]


def trace_domain(domain, record_type):
    domain = domain.strip()
    if not domain:
        return []

    # ✅ EARLY VALIDATION
    try:
        test = dns.resolver.resolve(domain, record_type)
        if not test:
            return []
    except Exception:
        return []  # No such record → stop immediately

    rdtype = dns.rdatatype.from_text(record_type)
    steps = []

    # ---------------- STEP 1: ROOT ----------------
    root_server = random.choice(ROOT_SERVERS)

    steps.append({
        "level": "root",
        "server": root_server,
        "server_name": get_ns_name(root_server),
        "authority": [],
        "answer": [],
        "rcode": 0,
    })

    # ---------------- STEP 2: TLD ----------------
    tld = domain.split(".")[-1] + "."

    root_response = query(root_server, tld, dns.rdatatype.NS)

    tld_ns_names = extract_ns(root_response)
    tld_ns_ips = resolve_ns_to_ip(tld_ns_names)

    if not tld_ns_ips:
        return steps

    tld_server = random.choice(tld_ns_ips)

    steps.append({
        "level": "tld",
        "server": tld_server,
        "server_name": get_ns_name(tld_server),
        "authority": tld_ns_names,
        "answer": [],
        "rcode": int(root_response.rcode()),
    })

    # ---------------- STEP 3: AUTHORITATIVE ----------------
    tld_response = query(tld_server, domain, dns.rdatatype.NS)

    auth_ns_names = extract_ns(tld_response)
    auth_ns_ips = resolve_ns_to_ip(auth_ns_names)

    if not auth_ns_ips:
        return steps

    auth_server = random.choice(auth_ns_ips)

    steps.append({
        "level": "authoritative",
        "server": auth_server,
        "server_name": get_ns_name(auth_server),
        "authority": auth_ns_names,
        "answer": [],
        "rcode": int(tld_response.rcode()),
    })

    # ---------------- STEP 4: ANSWER ----------------
    final_response = query(auth_server, domain, rdtype)
    answers = extract_answer(final_response)

    steps.append({
        "level": "answer",
        "server": auth_server,
        "server_name": get_ns_name(auth_server),
        "authority": [],
        "answer": answers,
        "rcode": int(final_response.rcode()),
    })

    return steps

