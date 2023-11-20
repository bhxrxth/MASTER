emotions = input("> ").capitalize()
words = emotions.split(" ")
emoji = {
    ":)": "😁",
    ":(": "😢"
}
output = ""
for words in words:
    output += emoji.get(words, words) + " "
print(output)
