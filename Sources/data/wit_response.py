
def wit_response(data):                     #gelen mesajdan intenti getirme
    nlp = data
    dic = {}
    for r in nlp:
        if nlp[r][0]["confidence"] > 0.5: #dogruluk orani 60tan buyuk sartiyla

            dic[nlp[r][0]["value"]] = nlp[r][0]["confidence"]


    if bool(dic) != False:
        return max(dic, key=dic.get)      # En yuksek Dogruluk orani olan intenti ayiklama
    else:
        return False


