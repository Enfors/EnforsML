#!/usr/bin/env python3

"""Shorinji Kempo bot
Attempts to answer questions about Shorinji Kempo.
"""

import textwrap

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
                      "Vad är speciellt med Shorinji Kempo",
                      "Vad är det som gör Shorinji Kempo unikt",
                      "Varför ska jag träna just Shorinji Kempo",
                      "Vad har Shorinji Kempo för kännetecken",
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
                      "varandra. Dessa tekniker tränas dock inte i "
                      "juniorgruppen."],

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
                      "Var finns er dojo",
                      "Var ligger er dojo",
                      "Var finns er träningslokal",
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
                      "Vilka dagar tränar ni",
                      "När är träningarna",
                      "När slutar träningarna",
                      "Vilka tider tränar ni",
                      "Hur länge håller träningarna på",
                      "Hur många gånger tränar ni per vecka",
                      "Hur många träningspass har ni",
                      "Träningstiderna hittar du på "
                      "http://shorinjikempo.net/traning/traningstider."],

                     ["Hur gammal måste man vara",
                      "Vad har ni för åldersgränser",
                      "Har ni någon åldersgräns",
                      "För liten",
                      "För ung",
                      "Tillräcklingt stor",
                      "Tillräcklingt gammal",
                      "När är man stor nog",
                      "När är man gammal nog",
                      "När är man för gammal",
                      "Kan man bli för gammal",
                      "För att träna måste man vara minst åtta år. "
                      "Vi har ingen övre åldersgräns, och vi har "
                      "aktiva medlemmar som är 60+."],

                     ["Måste man kunna japanska",
                      "Behöver man lära sig japanska",
                      "Får man lära sig japanska",
                      "Man behöver inte kunna japanska för att träna "
                      "Shorinji Kempo, men vissa ord och fraser kommer man "
                      "att lära sig av sig själv."],

                     ["Vem är tränaren",
                      "Vem är instruktör",
                      "Vad har ni för tränare",
                      "Vilka tränare har ni",
                      "Vad har er tränare för grad",
                      "Vem är er sensei",
                      "Vad heter er sensei",
                      "Vilka är era instruktörer",
                      "Vem är er instruktör",
                      "Vem är Anders",
                      "Vem är Anders-sensei",
                      "Vår huvudinstruktör heter Anders Pettersson, "
                      "och han har graden rokudan - svart bälte av "
                      "sjätte graden."],

                     ["När grundades klubben",
                      "Vilket år grundades klubben",
                      "Vem grundade klubben",
                      "Vem startade klubben",
                      "När startades klubben",
                      "Vem var det som grundade klubben",
                      "Klubben grundades av bland andra Anders Pettersson, "
                      "1981."],

                     ["Hur många medlemmar har ni",
                      "Hur stort är medlemsantalet",
                      "Hur många aktiva medlemmar har ni i klubben",
                      "I nuläget har vi c:a 40 aktiva medlemmar i vår klubb."],

                     ["Hur många aktiva finns det i Sverige",
                      "Hur många medlemmar finns det totalt i Sverige",
                      "Totalt finns det c:a 300 aktiva utövare i Sverige."],

                     ["Hur många klubbar finns det i Sverige",
                      "Hur många föreningar finns det i Sverige",
                      "Det finns ett tiotal Shorinji Kempo-föreningar i "
                      "Sverige."],

                     ["Hur kontaktar man er",
                      "Kan man ringa till er",
                      "Vad är era kontaktuppgifter",
                      "Jag vill ringa er",
                      "Har ni någon epostadress",
                      "Har ni någon emailadress",
                      "Har ni någon email-adress",
                      "Vad är er email-adress",
                      "Vad har Anders för telefonnummer",
                      "Vad har Christer för telefonnummer",
                      "Kan du Anders telefonnummer",
                      "Kan du Christers telefonnummer",
                      "Våra kontaktuppgifter hittar du på "
                      "http://shorinjikempo.net/kontakt."],

                     ["Finns ni på Facebook",
                      "Har ni någon Facebook-sida",
                      "Har ni någon Facebook sida",
                      "Vad är adressen till er Facebook"
                      "Adressen till klubbens Facebook-sida"
                      "Klubbens Facebook sida",
                      "Vår Facebook-sida finns på "
                      "http://www.facebook.com/ShorinjiKempoKarlstad."]]

    for data in training_data:
        intent = nlp.Intent(data[0])
        intent.train(data[:-1])
        intent.response_data = data[-1]
        all_intents.append(intent)

    parser = nlp.Parser(all_intents)

    print("""Hej! Jag är en chatbot som kan svara på frågor om Shorinji Kempo,
och om Shorinji Kempo-klubben i Karlstad.""")

    while True:
        try:
            user_txt = input("\nDin fråga: ")
        except (KeyboardInterrupt, EOFError):
            print()
            raise SystemExit

        if not len(user_txt):
            continue

        if "shorinjo" in user_txt.lower():
            print("OBS! Det heter Shorinji, inte Shorinjo. :-)")
            user_txt = user_txt.replace("shorinjo", "Shorinji")
            user_txt = user_txt.replace("Shorinjo", "Shorinji")

        try:
            result = parser.parse(user_txt)[0]
            print("\n".join(textwrap.wrap(result.intent.response_data)))
        except IndexError:
            print("Tyvärr förstår jag inte din fråga.")


if __name__ == "__main__":
    main()
