import time  
from selenium import webdriver
#from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import argparse  



#メインの関数、ここで最高得点のanagramを辞書から探して返す
def get_anagram_any_length(random_word,dictionary):
    
    max_score=0
    max_word=""
    
    #与えられた文字列random_wordをソート
    sorted_random_word=sorted(random_word.replace("QU","Q"))
    
    #与えられた文字列に含まれる文字と個数の対応の配列を作る
    dict_random_word=[sorted_random_word.count(chr(ord('A')+i)) for i in range(26)]
    
    #新しい辞書の単語全てに対して以下の処理
    for dictionary_word in dictionary:
        
        #dictionary_word=(単語をソートした配列、単語)であることに注意

        dict_dictionary_word=[dictionary_word[0].count(chr(ord('A')+i)) for i in range(26)]
        flag=True
        
        for i in range(26):
            if dict_random_word[i]<dict_dictionary_word[i]:
                flag=False
                break
                
        #どの文字も与えられた文字列に含まれているなら,その単語のスコアを求める
        if flag:
            score=count_score(dictionary_word[0])

            #点数が現在の最高得点と同じでも長さが長い方に更新
            if score==max_score and len(max_word)<len(dictionary_word[1]):
                max_score=score
                max_word=dictionary_word[1]
            #点が今までの最高得点よりも高ければ更新
            elif score>max_score:
                max_score=score
                max_word=dictionary_word[1]
            
    return max_word,max_score


#スコアを計算する関数
def count_score(word):
    score=0
    for i in word:
        if i in ['A', 'B', 'D', 'E', 'G', 'I', 'N', 'O', 'R', 'S', 'T', 'U']:
            score+=1
        elif i in ['J', 'K', 'X', 'Z','Q']:
            score+=3
        else :
            score+=2
    score=(score+1)**2
    return score


#以下は自動化のための関数

# 16文字の取得
def get_random_word(driver):
    random_word=""
    
    #"//div[@class='letter p1']"が読み込まれるのを待つ
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH,"//div[@class='letter p1']")))
    
    for i in range(1,4):
        #'letter p1'、'letter p2'、'letter p3'に分かれているので取得する
        #この時点で点数も取れるが今回はあとで調べる方式にした
        
        letters = driver.find_elements_by_xpath("//div[@class='letter p"+str(i)+"']")
        for letter in letters:
            if letter.text=="Qu":
                random_word+='Q'
            else:
                random_word+=letter.text

    return random_word.upper()



#自動でゲームを次に進める関数
def continue_game(driver,anagram):
    
    #id='MoveFieldが読み込まれるのを待つ
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@id='MoveField']")))
    
    if anagram=="":
        driver.find_element_by_xpath("//input[@value='PASS']").click()
    else:
        driver.find_element_by_xpath("//input[@id='MoveField']").send_keys(anagram)
        driver.find_element_by_xpath("//input[@value='Submit']").click()

        
        
#自動でレコードする関数
def record_score(driver,myname,email,github_url):
    
    #name='NickNameが読み込まれるのを待つ
    WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "//input[@name='NickName']")))
    
    driver.find_element_by_xpath("//input[@name='NickName']").send_keys(myname)
    driver.find_element_by_xpath("//input[@id='AgentRobot']").click()
    driver.find_element_by_xpath("//input[@name='Name']").send_keys(myname)
    driver.find_element_by_xpath("//input[@name='Email']").send_keys(email)
    
    #Githubs
    driver.find_element_by_xpath("//input[@name='URL']").send_keys(github_url)
    driver.find_element_by_xpath("//input[@type='submit']").click()
    
    
    
    
#以下が実行するコード
if __name__ == '__main__':
    
    #コマンドライン引数の定義
    parser = argparse.ArgumentParser(description='与えられた文字列に対してAnagramを返すプログラム')
    parser.add_argument('-s','--score',type=int,help='目標得点',default=1800)
    parser.add_argument('-i','--max_iter',type=int,help='最大試行回数',default=5)
    parser.add_argument('-m','--myname',type=str,help='名前',default='test')
    parser.add_argument('-e','--email',type=str,help='メールアドレス',default='')
    parser.add_argument('-g','--github_url',type=str,help='githubのURL',default='')

    args = parser.parse_args()

    # 目標得点
    target_score = args.score
    # 最大試行回数
    max_iter = args.max_iter
    # 名前
    myname = args.myname
    #提出用のメールアドレス
    email=args.email
    #提出用のgithubのURL
    github_url=args.github_url

    #辞書の読み込み(大文字に統一)
    sorted_dictionary=[]
    with open("./data/dictionary.words.txt","r") as f:
        for line in f:
            word=line.rstrip('\n').upper()
            sorted_dictionary.append((sorted(word.replace("QU","Q")),word))
        
    #sorted_dictionary.sort()
    
    #max_iter回ゲームをおこなう
    for game in range(max_iter):

        #driverを使ってゲームページにアクセス
        driver = webdriver.Chrome()
        #カレントウインドウのサイズを高さ、幅:200,200に設定する
        driver.set_window_size(200,200)

        driver.get('https://icanhazwordz.appspot.com/')
        
        total_score=0
        
        #10回トライアル
        for i in range(10):
            
            random_word=get_random_word(driver)
            anagram,score=get_anagram_any_length(random_word,sorted_dictionary)
            
            #一度でも120 点未満ならそのゲームはリタイア
            if score<120:
                break

            total_score+=score
            
            #入力と次のトライアルへの移動
            continue_game(driver,anagram)
            
            
        #10回のトライアルが終わった段階で目標点より点数が高ければ記録   
        if total_score>target_score:
            record_score(driver,myname,email,github_url)
            print("Done")
            break
        else:
            print("Failed",game)
            print("score:",total_score)
            driver.close()
    

        