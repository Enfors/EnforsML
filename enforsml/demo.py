#!/usr/bin/env python3

"""Classes for words and sentences.
"""

import doctest

import text.utils
import text.ngram
import text.bagofwords

swedish_stop_words = ["den", "en", "ett", "och",
                      "det", "att"]


def demo():
    """Demonstrate the functionality in action.
    """

    results = []

    min_n = 1
    max_n = 3
    bag = text.bagofwords.BagOfWords()
    matrix = text.ngram.NGramMatrix(min_n, max_n)

    print("min_n: %d, max_n: %d" % (min_n, max_n))

    train_data = [
        ["helt klart århundradets bästa film", 95],
        ["en film i absolut världsklass", 90],
        ["det här är årets bästa film alla kategorier", 85],
        ["så jävla bra", 83],
        ["jag är övertygad om att om 20 år kommer alla säga att detta "
         "är en klassiker", 80],
        ["det är helt klart en hysteriskt kul film", 80],
        ["en fantastiskt bra film", 85],
        ["en fantastisk film", 80],
        ["en jättebra film helt enkelt", 78],
        ["en mycket bra film", 75],
        ["den var riktigt bra måste jag säga", 75],
        ["jättebra film skulle vilja se fler av samma regisör", 75],
        ["en riktigt bra film", 70],
        ["den är jätterolig", 70],
        ["perfekt för en mysig hemmakväll", 65],
        ["definitivt en kultklassiker", 60],
        ["den var förvånande nog ganska bra ändå", 60],
        ["den här filmen var helt okej tycker jag", 50],
        ["jag skulle gärna se fler såna här filmer", 40],
        ["det är en rolig film", 35],
        ["jag tyckte väl att den var ganska bra", 30],
        ["jag tycker den är ganska rolig", 25],
        ["den duger en regning kväll", 25],
        ["godkänd men inte mer än så skulle jag säga", 20],
        ["den var lite rolig måste jag erkänna", 20],
        ["knappt godkänd men har sina poänger", 15],
        ["den kunde ha varit värre", 10],
        ["inte den bästa jag sett men inte det sämsta heller", 0],
        ["vad ska man säga det var inget man vill se igen direkt", -15],
        ["en småtråkig film måste jag säga", -10],
        ["den här filmen är inte särskilt rolig", -15],
        ["den är inget vidare", -20],
        ["den var tråkig vill inte se den igen", -20],
        ["dålig film som inte alls är rolig", -25],
        ["mycket tråkig film tycker jag", -30],
        ["den var jättetråkig", -30],
        ["den var ganska dålig faktiskt", -30],
        ["jag tycker den är ganska kass faktiskt", -35],
        ["det här var inget mästerverk direkt", -35],
        ["den sunkigaste film jag sett på länge", -40],
        ["denna så kallade komedi är inte ett dugg rolig", -40],
        ["en riktigt dålig film", -50],
        ["rent skräp finns inget annat att säga", -65],
        ["så himla trist", -60],
        ["så trist att jag nästan somnade", -65],
        ["hur sopig som helst", -70],
        ["asdålig film fattar inte att de gör sånt", -75],
        ["den här filmen suger helt enkelt", -75],
        ["fattar inte hur en film kan vara så dålig", -75],
        ["filmen suger stenhårt", -80],
        ["det var 90 minuter av mitt liv jag aldrig kommer att få "
         "tillbaka", -80],
        ["detta var rent skräp finns inget annat att säga", -80],
        ["en riktig jävla skitfilm", -85],
        ["den var riktigt jävla sämst", -87],
        ["århundradets sämsta film alla kategorier", -90],
        ["det är den sämsta film jag någonsin sett", -90],
        ["aldrig har mänligheten utsatts för värre smörja än detta", -95],
        ]

    test_data = [
        "århundradets bästa film enligt min mening",
        "det här är min nya favoritfilm",
        "jag tyckte den var jättebra",
        "en ganska bra film",
        "vill gärna se den igen någon gång",
        "den var väl okej",
        "den var skitdålig",
        "sämsta jag har sett på länge",
        "århundradets skitfilm alla kategorier",
        "skräp helt enkelt",
        "den är lite rolig",
        "den är ganska rolig",
        "den är jätterolig",
        "åh gud vilken tråkig film",
        "fy fan vilken tråkig film",
        "en väldigt bra film som visar hur en del invandrare "
        "har det i det här landet",
        "den var verkligen inspirerande och viktig att titta på "
        "om fördomar",
        "man kan verkligen relatera till filmen och det var det "
        "bästa med den",
        "det var en helt fantastisk film och den var väldigt "
        "bra gjord",
        "den bästa filmen jag har sett",
        "den sämsta filmen jag har sett",
        "jag tycker att det är bra filmen",
        "jag ger 5 betyg till filmen eftersom filmen är rolig",
        ]

    for sentence, score in train_data:
        sentence = text.utils.remove_words(sentence, swedish_stop_words)
        matrix.set_sentence_value(sentence, score)
        bag.add_words(sentence.split(" "))

    # print("word frequencies:")
    # for k, v in bag.sorted_matrix(reverse=True):
    #     if v > 2:
    #         print("%-16s: %3d" % (k, v))

    for sentence in test_data:
        sentence = text.utils.remove_words(sentence, swedish_stop_words)
        results.append([sentence, matrix.get_sentence_value(sentence)])

    for sentence, score in sorted(results, key=lambda l: l[1], reverse=True):
        print("%3d: %s" % (score, sentence))


if __name__ == "__main__":
    demo()
    doctest.testmod()
