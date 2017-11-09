#!/usr/bin/env python3

"""Shorinji Kempo bot
Attempts to answer questions about Shorinji Kempo.
"""


from enforsml.text import nlp


def main():
    """Main function of the script.
    """

    all_intents = []

    training_data = [["Vad är Shorinji Kempo",
                      "Vad är Shorinji Kempo för något",
                      "Vad är Shorinji Kempo för slags kampsport",
                      "Shorinji Kempo är en mångsidig japansk kampsport."],

                     ["Hur blir man medlem",
                      "Hur blir man medlem i Shorinji Kempo",
                      "Vad krävs för att bli medlem",
                      "Hur blir man medlem i klubben",
                      "Hur går man med i Shorinji Kempo",
                      "Hur går man med i klubben",
                      "Information om hur man blir medlem hittar du på "
                      "http://shorinjikempo.net/traning/borja-trana."],

                     ["Vem grundade Shorinji Kempo",
                      "Vem var det som grundade Shorinji Kempo",
                      "Vem är Shorinji Kempos grundare",
                      "Vem var det som startade Shorinji Kempo",
                      "Vem var det som uppfann Shorinji Kempo",
                      "Vem hittade på Shorinji Kempo",
                      "Vem startade Shorinji Kempo",
                      "Shorinji Kempo grundades av So Doshin."],

                     ["Vad skiljer Shorinji Kempo från andra kampsporter",
                      "Vad är det för skillnad mellan Shorinji Kempo och "
                      "andra kampsporter",
                      "Vad är det för skillnad mellan Shorinji Kempo och "
                      "karate",
                      "Shorinji Kempo brukar kallas \"Den tänkande människans "
                      "kampsport\", eftersom vi lägger relativt stor vikt "
                      "vid filosofi."],

                     ["Finns det sparkar och slag i Shorinji Kempo",
                      "Finns det slag i Shorinji Kempo",
                      "Slår man i Shorinji Kempo",
                      "Finns det sparkar i Shorinji Kempo",
                      "Sparkar man i Shorinji Kempo",
                      "Shorinji Kempo innehåller sparkar, slag, "
                      "losstagningar, nedtagningar och kast."],

                     ["Gör det ont att träna Shorinji Kempo",
                      "Får man ont av att träna",
                      "Gör det ont när man tränar",
                      "Hur ont gör det att träna",
                      "Vissa tekniker som tränas i vuxengruppen kan göra lite "
                      "ont, så det är viktigt att vi är försiktiga med "
                      "varandra."],

                     ["Vad kostar det att vara medlem",
                      "Vad kostar det att bli medlem i klubben",
                      "Vad kostar träningen",
                      "Hur mycket kostar träningen",
                      "Vad kostar medlemsskapet",
                      "Vad kostar det att vara med",
                      "Hur mycket kostar det att träna Shorinji Kempo",
                      "Är det dyrt att vara med",
                      "Hur dyrt är det att träna",
                      "Alla priser finns på "
                      "http://shorinjikempo.net/traning/borja-trana."],

                     ["Kan man provträna gratis",
                      "Måste man bli medlem innan man tränar",
                      "Kan man prova innan man blir medlem",
                      "Kan man testa utan att det kostar något",
                      "Måste man betala om man bara vill testa",
                      "Om man betalar månadsavgiften, så kan man provträna en "
                      "månad utan att behöva betala träningsavgift."],

                     ["Var ligger träningslokalen",
                      "Var finns dojon",
                      "Var håller ni till",
                      "Var tränar ni",
                      "Var ligger klubbens träningslokal",
                      "Vi tränar i Kvarnbergsskolans gymnastiksal, på "
                      "Ölmegatan 10 i Karlstad."],

                     ["Är Shorinji Kempo svårt",
                      "Är det en svår sport",
                      "Är det svårt att träna Shorinji Kempo",
                      "Hur svårt är det",
                      "Hur svårt är Shorinji Kempo",
                      "Är det svårt",
                      "Det finns mycket att lära sig, men det är också det "
                      "som gör det intressant."],

                     ["Vilka träningstider har ni",
                      "När tränar ni",
                      "När är träningarna",
                      "När slutar träningarna",
                      "Vilka tider tränar ni",
                      "Hur länge håller träningarna på",
                      "Träningstiderna hittar du på "
                      "http://shorinjikempo.net/traning/traningstider."]]

    for data in training_data:
        intent = nlp.Intent(data[0])
        intent.train(data[:-1])
        intent.response_data = data[-1]
        all_intents.append(intent)

    questions = (["Hur blir jag medlem",
                  "Vad är Shorinji Kempo för nåt",
                  "Vem var det som skapade Shorinji Kempo",
                  "Finns det sparkar och slag i Shorinji Kempo",
                  "Gör det ont att träna",
                  "Vad kostar det att bli medlem",
                  "Kan man testa utan att behöva betala något",
                  "Vad har ni för träningstider",
                  "foobar"])

    parser = nlp.Parser(all_intents)

    for question in questions:
        print("Q:", question)
        results = parser.parse(question)
        if len(results) < 1:
            print("   [Jag förstår inte den frågan]")
            continue

        scored_intent = results[0]
        score = scored_intent.score
        intent = scored_intent.intent

        print("  %4d: %s" % (score, intent.response_data))


if __name__ == "__main__":
    main()
