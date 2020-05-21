#辞書を二分探索する関数
def binary_search(sorted_word,dictionary):
    
    #dictionaryが二次元配列であることに注意する
    left,right=0,len(dictionary)
    while left<=right:
        
        mid=(left+right)//2
        
        if dictionary[mid][0]==sorted_word:
            return dictionary[mid][1]
        elif dictionary[mid][0]<sorted_word:
            left=mid+1
        else :
            right=mid-1
    
    return None


#メインの関数（与えられた文字列のアナグラムを返す）

def get_anagram(random_word,dictionary):
    #与えられた文字列をソート
    sorted_random_word=sorted(random_word)
    
    #新しい辞書の中を二分探索で探索して一致する単語を見つける
    anagram=binary_search( sorted_random_word,dictionary)

    return anagram



#以下が実行するコード
if __name__ == '__main__':

    random_word=input("Input a string:")

    #辞書の読み込み(大文字に統一)
    sorted_dictionary=[]
    with open("./data/dictionary.words.txt","r") as f:
        for line in f:
            word=line.rstrip('\n').upper()
            #辞書の単語を二次元配列にして保管
            sorted_dictionary.append((sorted(word),word))
        
    #辞書全体をソートする
    sorted_dictionary.sort()

    #アナグラムを取得
    anagram=get_anagram(random_word.upper(),sorted_dictionary)
    if anagram==None:
        print("No anagram")
    else:
        print("Anagram is "+anagram)