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
                      "Vad är Shorinji Kempo för slags kampsport"],

                     ["Hur blir man medlem",
                      "Hur blir man medlem i Shorinji Kempo",
                      "Vad krävs för att bli medlem",
                      "Hur blir man medlem i klubben",
                      "Hur går man med i Shorinji Kempo",
                      "Hur går man med i klubben"],

                     ["Vem grundade Shorinji Kempo",
                      "Vem var det som grundade Shorinji Kempo",
                      "Vem är Shorinji Kempos grundare",
                      "Vem var det som startade Shorinji Kempo",
                      "Vem var det som uppfann Shorinji Kempo",
                      "Vem hittade på Shorinji Kempo",
                      "Vem startade Shorinji Kempo"],

                     ["Vad skiljer Shorinji Kempo från andra kampsporter",
                      "Vad är det för skillnad mellan Shorinji Kempo och "
                      "andra kampsporter",
                      "Vad är det för skillnad mellan Shorinji Kempo och "
                      "karate"],

                     ["Finns det sparkar och slag i Shorinji Kempo",
                      "Finns det slag i Shorinji Kempo",
                      "Slår man i Shorinji Kempo",
                      "Finns det sparkar i Shorinji Kempo",
                      "Sparkar man i Shorinji Kempo"],

                     ["Gör det ont att träna Shorinji Kempo",
                      "Får man ont av att träna",
                      "Gör det ont när man tränar",
                      "Hur ont gör det att träna"],

                     ["Vad kostar det att vara medlem",
                      "Vad kostar det att bli medlem i klubben",
                      "Vad kostar träningen",
                      "Hur mycket kostar träningen",
                      "Vad kostar medlemsskapet",
                      "Vad kostar det att vara med",
                      "Hur mycket kostar det att träna Shorinji Kempo",
                      "Är det dyrt att vara med",
                      "Hur dyrt är det att träna"],

                     ["Kan man provträna gratis",
                      "Måste man bli medlem innan man tränar",
                      "Kan man prova innan man blir medlem",
                      "Kan man testa utan att det kostar något",
                      "Måste man betala om man bara vill testa"],

                     ["Var ligger träningslokalen",
                      "Var finns dojon",
                      "Var håller ni till",
                      "Var tränar ni",
                      "Var ligger klubbens träningslokal"],

                     ["Vilka träningstider har ni",
                      "När tränar ni",
                      "När är träningarna",
                      "När slutar träningarna",
                      "Vilka tider tränar ni",
                      "Hur länge håller träningarna på"]]

    for data in training_data:
        intent = nlp.Intent(data[0])
        intent.train(data)
        all_intents.append(intent)

    questions = (["Hur blir jag medlem",
                  "Vad är Shorinji Kempo för nåt",
                  "Vem var det som skapade Shorinji Kempo",
                  "Finns det sparkar och slag i Shorinji Kempo",
                  "Gör det ont att träna",
                  "Vad kostar det att bli medlem",
                  "Kan man testa utan att behöva betala något",
                  "Vad har ni för träningstider"])

    for question in questions:
        print("Q:", question)

        results = []

        for intent in all_intents:
            results.append([sum(intent.check(question)), intent.name])

        results = sorted(results, key=lambda l: l[0], reverse=True)
        num_shown = 0

        for result in results:
            if result[0] > 30 and num_shown < 3:
                print("  %4d: %s" % (result[0], result[1]))
                num_shown += 1


if __name__ == "__main__":
    main()
