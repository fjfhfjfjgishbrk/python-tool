wordList = []
for i in range(26):
  wordList.append([])
alpha = "abcdefghijklmnopqrstuvwxyz"

for line in open("words_alpha.txt"):
    word = line.rstrip()

    wordList[alpha.index(word[0])].append(word)

f = open("words_list.txt", "w")
for i in range(26):
  f.write(" ".join(wordList[i]))
  f.write("\n")
