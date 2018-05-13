
def wit_response(data):
    nlp = data # messaging_event["message"]["nlp"]["entities"]
    dic = {}
    for r in nlp:
        if nlp[r][0]["confidence"] > 0.5: #dogrulama orani
            dic[nlp[r][0]["value"]] = nlp[r][0]["confidence"]

    if bool(dic) != False:
        return max(dic, key=dic.get)
    else:
        return False
