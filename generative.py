from sklearn.cluster import KMeans
from sklearn.neighbors import KNeighborsClassifier
from sklearn.feature_extraction.text import CountVectorizer
import cleaner as cl
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.decomposition import SparsePCA
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# The next things TODO:
# use the original greek text
# include john
# get longer summaries
# better model?
matt11_nkjv = ["Now after Jesus was born in Bethlehem of Judea in the days of Herod the king, behold, wise men from the East came to Jerusalem.",
               "saying, Where is He who has been born King of the Jews? For we have seen His star in the East and have come to worship Him.", 
               "When Herod the king heard this, he was troubled, and all Jerusalem with him.",
               "And when he had gathered all the chief priests and scribes of the people together, he inquired of them where the Christ was to be born.",
               ]
matt11_kjv = ["Now when Jesus was born in Bethlehem of Judaea in the days of Herod the king, behold, there came wise men from the east to Jerusalem,",
              "Saying, Where is he that is born King of the Jews? for we have seen his star in the east, and are come to worship him.",
              "When Herod the king had heard these things, he was troubled, and all Jerusalem with him.",
              "And when he had gathered all the chief priests and scribes of the people together, he demanded of them where Christ should be born."
              ]



def save_Arr(filePath, data, save=True):
    if save:
        with open(filePath, "w") as f:
            f.write(str(data))

def save_NpArr(filePath, data, save=True):
    if save:
        with open(filePath, "w") as f:
            for line in data:
                f.write("[")
                for ele in line:
                    f.write(str(ele))
                f.write("]")

def print_Sentence_and_Prediction(rng, vectorized, print_sentence = False):
    for i in rng: # this will print whatever sentences you choose (numerically) and give a prediction for them.
        vector = vectorized[i]
        sentence = []
        for j, val in enumerate(vector):
            if val != 0:
                sentence.append(features[j])
        prediction = kmeans.predict(vectorized[i].reshape(1, -1)) # gives a prediction for the current sentence
        actual = 0
        for k in range(len(books)):
            if i in verses_In_Books[k]:
                actual = books[k]
        
        print(f"Index: {i}, Prediction: {books[prediction[0]]}, Actual: {actual}" + ("Sentence: {sentence}" if print_sentence else ""))


def plot_pcs(pcs, numPoints, ranges, clusters):
    x = pcs[:,0]
    y = pcs[:,1]
    z = pcs[:,2]

    colors = []
    markerList = ('o', 's', '^')
    markers = [markerList[clusters[i]] for i in range(numPoints)]
    # print(markers)
    for i in range(numPoints):
        if i in ranges[0]:
            colors.append("blue")   # matthew
        elif i in ranges[1]:
            colors.append("green")  # mark
        else:
            colors.append("red")    # luke

    fig1 = plt.figure(figsize=(10, 8)) # both
    fig2 = plt.figure(figsize=(10, 8)) # book only
    fig3 = plt.figure(figsize=(10, 8)) # cluster only
    ax1 = fig1.add_subplot(111, projection='3d')
    ax2 = fig2.add_subplot(111, projection='3d')
    ax3 = fig3.add_subplot(111, projection='3d')


    colorDict = {0:"red",1:"blue",2:"green"}
    clusterList = [colorDict[clusters[i]] for i in range(numPoints)]

    # both
    for i in range(numPoints):
        ax1.scatter(x[i], y[i], z[i], c=colors[i], marker=markers[i])
    ax1.set_xlabel('PC 1')
    ax1.set_ylabel('PC 2')
    ax1.set_zlabel('PC 3')
    ax1.set_title("MML plotted according to book and cluster")

    # book
    for i in range(numPoints):
        ax2.scatter(x[i], y[i], z[i], c=colors[i])
    ax2.set_xlabel('PC 1')
    ax2.set_ylabel('PC 2')
    ax2.set_zlabel('PC 3')
    ax2.set_title("MML plotted according to book")
    # plt.savefig("./figures/book")
    # plt.show()


    # cluster
    for i in range(numPoints):
        ax3.scatter(x[i], y[i], z[i], c=clusterList[i])
    ax3.set_xlabel('PC 1')
    ax3.set_ylabel('PC 2')
    ax3.set_zlabel('PC 3')
    ax3.set_title("MML plotted according to cluster")

    plt.show()

update = True
books = ("matt", "mark", "luke")#, "john")
chatRanges = (range(1071), range(1071, 1749), range(1749,2900))
chatPoints = 2900
perpRanges = (range(10), range(10,25), range(25,35))
perpPoints = 35

if __name__ == "__main__":
    clean_books = cl.Cleaner(books).clean_books_p(save=True)
    #    # use a sparse matrix.
    vec = CountVectorizer()
    # clean_books += cleanUserInput                          # add the user input so we know what words to train for

    vectorized = vec.fit_transform(clean_books).toarray() # this is the vectorized list of verses
    
    save_NpArr("./perplexity/p_vectorized_books.txt", vectorized, update)

    print(f"m: {len(vectorized)}, n: {len(vectorized[0])}")

    # This is KMEANS STUFF
    kmeans = KMeans(n_clusters=3, n_init='auto', random_state=100).fit(vectorized)   # creates a kmeans on just the actual input
    features = vec.get_feature_names_out()  # this is a alphabetical list of all the words we trained on
    
    # getting the 'predictions'
    clusterArray = []
    for line in vectorized:
        clusterArray.append(kmeans.predict(line.reshape(1,-1))[0])
    # print(clusterArray)
    # This is PCA STUFF
    pca = PCA(n_components=3)
    # pca.fit(vectorized)
    pcs = pca.fit_transform(vectorized)

    plot_pcs(pcs, perpPoints, perpRanges, clusterArray)
    print(pca.explained_variance_ratio_)
    # print(pca.singular_values_)


    # calculate variance
    # do one for John



# # translation may help with this

# # get the character context and how they write, do a similar thing to what I am doing now.
# # have the llm give me a nice subset of good words
# # give the llm the story and have it remove the the's and and's and all that...
# # rows are the different stories.
# # ask the llm to split up the whole book of matthew into different stories.
# # have it split it up for me. Use the title as this

# # context space

# # it is possible that the authors took different sources and interpreted them differently and so used different words to describe them. This is why we need to find the "meaning" of the words rather than the words themselves.


# Ask it to expand on the stories a little bit.
# high level is like context (naming objects)
# low level feature ()
# most significant feature for the car thing is the background.
# can I get it to a point where, write this in the style of mark, or the style of luke. Could I subtract off their voices to get a 'unified' voice.
# translate NT into Dr. Suess
# Llama
# use the original greek.