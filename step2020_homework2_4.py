import time
class Cache:
    # Initializes the cache.
    # |n|: The size of the cache.
    def __init__(self, n):
        self.n = n
        self.data_dict = {"start": ["", "last"], "last": ["start", ""]}
        self.hash_table =[""]*10009

    # Access a page and update the cache so that it stores the most
    # recently accessed N pages. This needs to be done with mostly O(1).
    # |url|: The accessed URL
    # |contents|: The contents of the URL
    
    """"
    メインの関数
    この関数ではdata_dictにurlの順番を入れて、ハッシュテーブルにcontentsをいれる。

    返り値はなし：data_dictとhash_tableを更新することが目的
    data_dict:辞書型
    hash_table:配列型

    例）'a.com','c.com','d.com'というような順番があるときに隣どうしの関係のみdictに保存して位置関係を維持する
    data_dictには、'start','a.com','c.com','d.com','last'というkeyが入っていて、
    valueには上の順で[左のURL,右のURL]が入っている状態になる。
    hash_tableにはそれぞれのurlで各文字に対してasciiコードを使い数値化して、それの10009で割った余りをcontentsを格納する位置とする
    """
    def access_page(self, url, contents):
        
        #もしすでにそのURLがdata_dictに存在するなら元の位置から消す
        if url in self.data_dict.keys():

            left_url = self.data_dict[url][0]
            right_url = self.data_dict[url][1]

            self.data_dict[left_url][1] = right_url
            self.data_dict[right_url][0] = left_url
        
        #長さに余裕がないかつ、data_dictにないURLの場合最後尾のURLを消す
        elif len(self.data_dict)-2>=self.n:
            # lastの左隣を書き換え
            new_last_url = self.data_dict[self.data_dict["last"][0]][0]

            #lastの左隣のURLはもう保存しなくて良いので消す
            del self.data_dict[self.data_dict["last"][0]]
            
            #lastを次の最後尾のURLにつなげる
            self.data_dict["last"][0] = new_last_url
            self.data_dict[new_last_url][1] = "last"

        #先頭に新しいURLを割り込む
        head_url = self.data_dict["start"][1]
        self.data_dict[url] = ["start", head_url]
        self.data_dict["start"][1] = url
        self.data_dict[head_url][0] = url

        
        #ここからハッシュにコンテンツを加える処理
        #ここの計算量がurlの文字数分かかってしまう
        index=""
        for c in url:
            index+=str(ord(c))
        index=int(index)%10009
        if self.hash_table[index]=="":
            self.hash_table[index]=contents
        else:
            return "This memory is occupied"
            

        
    # Return the URLs stored in the cache. The URLs are ordered
    # in the order in which the URLs are mostly recently accessed.
    
    def get_pages(self):
        if self.data_dict["start"][1]=="last":
            return []
        #cache配列を作り、先頭のURLをまず追加する
        cache = [self.data_dict["start"][1]]
    
        #data_dictからURLの右隣を調べて追加していく
        for i in range(1,len(self.data_dict)):
            
            #lastまで来たら終了
            if self.data_dict[cache[i-1]][1]=="last":
                break
            
            cache.append(self.data_dict[cache[i-1]][1])
        
        return cache

# Does your code pass all test cases? :)
def cache_test():
    # Set the size of the cache to 4.
    cache = Cache(4)
    # Initially, no page is cached.
    equal(cache.get_pages(), [])
    # Access "a.com".
    cache.access_page("a.com", "AAA")
    # "a.com" is cached.
    equal(cache.get_pages(), ["a.com"])
    # Access "b.com".
    cache.access_page("b.com", "BBB")
    # The cache is updated to:
    #   (most recently accessed)<-- "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["b.com", "a.com"])
    # Access "c.com".
    cache.access_page("c.com", "CCC")
    # The cache is updated to:
    #   (most recently accessed)<-- "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["c.com", "b.com", "a.com"])
    # Access "d.com".
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
    # Access "d.com" again.
    cache.access_page("d.com", "DDD")
    # The cache is updated to:
    #   (most recently accessed)<-- "d.com", "c.com", "b.com", "a.com" -->(least recently accessed)
    equal(cache.get_pages(), ["d.com", "c.com", "b.com", "a.com"])
    # Access "a.com" again.
    cache.access_page("a.com", "AAA")
    # The cache is updated to:
    #   (most recently accessed)<-- "a.com", "d.com", "c.com", "b.com" -->(least recently accessed)
    equal(cache.get_pages(), ["a.com", "d.com", "c.com", "b.com"])
    cache.access_page("c.com", "CCC")
    equal(cache.get_pages(), ["c.com", "a.com", "d.com", "b.com"])
    cache.access_page("a.com", "AAA")
    equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
    cache.access_page("a.com", "AAA")
    equal(cache.get_pages(), ["a.com", "c.com", "d.com", "b.com"])
    # Access "e.com".
    cache.access_page("e.com", "EEE")
    # The cache is full, so we need to remove the least recently accessed page "b.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "e.com", "a.com", "c.com", "d.com" -->(least recently accessed)
    equal(cache.get_pages(), ["e.com", "a.com", "c.com", "d.com"])
    # Access "f.com".
    cache.access_page("f.com", "FFF")
    # The cache is full, so we need to remove the least recently accessed page "c.com".
    # The cache is updated to:
    #   (most recently accessed)<-- "f.com", "e.com", "a.com", "c.com" -->(least recently accessed)
    equal(cache.get_pages(), ["f.com", "e.com", "a.com", "c.com"])
    print("OK!")

# A helper function to check if the contents of the two lists is the same.


def equal(list1, list2):
    assert(list1 == list2)
    for i in range(len(list1)):
        assert(list1[i] == list2[i])

if __name__ == "__main__":
  cache_test()