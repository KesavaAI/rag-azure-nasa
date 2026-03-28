ACRONYMS = {
    "TRL": "Technology Readiness Level",
    "PDR": "Preliminary Design Review",
    "CDR": "Critical Design Review",
    "SRR": "System Requirements Review"
}

def expand_query(query):
    queries = [query]

    for k, v in ACRONYMS.items():
        if k in query:
            queries.append(query.replace(k, v))

    queries.append(query + " NASA systems engineering")

    return queries