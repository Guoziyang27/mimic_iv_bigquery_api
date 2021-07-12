
def retrive_query_result(query_result, with_header, header):
    if with_header:
        return [{header[i]:str(result[i]) for i in range(len(result))} for result in query_result]
    else:
        return [[str(result[i]) for i in range(len(result))] for result in query_result]
