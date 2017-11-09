# EnforsML - Enfors Machine Learning library

Project state: Planning

# text - text-related classes

## word

## ngram

## bagofwords

## utils

## nlp

Functionality related to natural language processing for chatbots and
the like.

### How to create a parser

1. Identify, in general terms, the commands that the parser should
   recognize. These are the Intents.
   
2. For each Intent, amass a collection of sentences that the user
   could be expected to type when they want to invoke this command.
   These sentences will be used to train the Intent to recognize
   similar sentences.
   
3. Add each of these Intents to a Parser.
   
3. When you have text input from a user that you want to parse, give
   it to a Parser and the parser will feed this text to each Intent in
   turn, and the Intents will return an object indicating (among other
   things) how likely the Intent thinks it is that the user was trying
   to invoke that specific Intent. This is called the confidence
   score. The Parser will then return a list of Intents with a
   confidence score higher than zero, sorted by the confidence score
   (descending - highest first).

