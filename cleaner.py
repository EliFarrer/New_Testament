class Cleaner:
    def __init__(self, books):
        self.books = books

    def clean_books(self, summarized=False, save=False):
        c_bks = []
        
        for book in self.books:
            if summarized:
                c_bks += self.clean_book_summarized(book + "_summarized.txt")
            else:
                c_bks += self.clean_book(book + ".txt")

        self.cleanBooks = c_bks

        if save:
            cond = "_summarized" if summarized else ""
            with open("clean_books" + cond + ".txt", "w") as f:
                print(self.cleanBooks, file=f)
        return self.cleanBooks

    def clean_books_p(self, save=False):
        clean = []
        for book in self.books:
            with open("./perplexity/p_" + book + ".txt", "r") as f:
                cleaned = self.removeSpecialChars(f.readlines())
                clean += cleaned

        self.cleanBooks = clean
        if save:
            with open("./perplexity/p_cleaned_books.txt", "w") as f:
                print(self.cleanBooks, file=f)

        return self.cleanBooks



    def _removeSpecialCharsFromVerse(self, arr):
        bad = "!.?;,():'"
        for char in bad:
            arr = arr.replace(char, "")
        return arr.lower()

    def removeSpecialChars(self, arr):
        cleaned = []
        for verse in arr:
            verse = verse.strip()
            cleaned.append(self._removeSpecialCharsFromVerse(verse))
        return cleaned

    def clean_book(self, bookFile):
        verses = []
        with open(bookFile) as file:
            lines = file.readlines()
            for line in lines:
                if line[0] == "[": # if we are in a verse.
                    pos = line.find(" ")
                    verses.append(line[pos+1:].strip())
        # print(verses)
        clean_verses = self.removeSpecialChars(verses)
        return clean_verses

    def clean_book_summarized(self, bookFile):
        lines = []
        cleanLines = []
        with open(bookFile) as f:            
            lines = f.readlines()
        for line in lines:
            line = line.strip()
            if line == "":
                continue
            elif line[0:5] == "Story":
                continue
            else:
                cleanLines.append(line)
        cleanLines = self.removeSpecialChars(cleanLines)
        return cleanLines


# helper function to write the book lines (not useful right now)
def writeBookLines(book):
    lines = []
    with open(book + ".txt") as readFile:
        lines = readFile.readlines()
    outLine = ""
    for line in lines:
        if len(line) <= 7:
            continue
        idx = line.find(" ")
        outLine += line[idx+1:].strip() + "\n"
        # print(line[idx+1:])
    with open(book + "_line.txt", "w") as f:
        print(outLine[:-1], file=f)

# def cleanBookStories(book):
#     lines = []
#     cleanLines = []
#     with open(book + "_summarized.txt") as f:            
#         lines = f.readlines()
#     for line in lines:
#         line = line.strip()
#         if line == "":
#             continue
#         elif line[0:5] == "Story":
#             continue
#         else:
#             cleanLines.append(line)
#     with open(book + "_cleaned_summarized.txt", "w") as f:
#         print(cleanLines, file=f)

def save_Arr(filePath, data, save=True):
    if save:
        with open(filePath, "w") as f:
            f.write(str(data))

if __name__ == "__main__":
    # clean = Cleaner("matt.txt")
    # out = clean.clean()
    # verse = "Teaching them to observe all things whatsoever I have commanded you: and, lo, I am with you alway, even unto the end of the world. Amen."
    # print(out)

    # Will update the lined version of the NT
    cleanBooksArray = []
    for book in books:
        writeBookLines(book)
        cleanBooksArray += Cleaner(book + ".txt").cleaned
    cleanBookStories("matt")
    save_Arr("clean_books.txt", cleanBooksArray)




