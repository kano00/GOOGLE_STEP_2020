from collections import deque

#テキストファイルを読み込む

#nicknamesはidとニックネームの対応関係の入るdict型
nicknames={}

#edgesは矢印で繋がるidとidの方向も含む対応関係の入る配列
edges=[]

file_name = "nicknames.txt"
with open(file_name,"r", encoding="utf-8-sig") as f:
    data=f.read()
    lines = data.split('\n')
    for line in lines:
        id,name= line.split('\t')
        nicknames[name]=int(id)

file_name = "links.txt"
with open(file_name,"r", encoding="utf-8-sig") as f:
    data=f.read()
    lines = data.split('\n')
    for line in lines:
        start,goal= line.split('\t')
        edges.append([int(start),int(goal)])


#グラフ作成
Gragh=[[] for _ in range(len(nicknames))]

#Gragh[id]
for edge in edges:
    Gragh[edge[0]].append(edge[1])



"""
start_idから他のidまでの距離を幅優先探索で調べて返す関数
引数：int型
返り値：list型　中身はstart_idからの距離、index=idという対応
"""
def bfs(start_id):
    #まず起点のidをキューに入れる
    queue=deque([start_id])
    
    #start_idからの距離を保持する配列(-1ならまだ訪れてないidであることを表す)
    dis=[-1]*len(nicknames)
    
    #自分との距離は０
    dis[start_id]=0
    
    #幅優先探索を始める
    while queue:
        #idをqueueから取り出す
        search_id=queue.popleft()
        for i in Gragh[search_id]:
            #まだ訪れていないなら距離を更新
            if dis[i] ==-1:
                dis[i]=dis[search_id]+1
                #新たにidをキューに追加して今度これと繋がるidを探索する
                queue.append(i)
    return dis



if __name__ == "__main__":

    #"adrian"から自分"cecil"までの距離を求める
    start_name="adrian"
    goal_name="cecil"
    my_name="cecil"

    dis_to_everyone_from_adrian=bfs(nicknames[start_name])
    result=format(dis_to_everyone_from_adrian[nicknames[goal_name]])
    print("{}から{}までの距離:".format(start_name,goal_name),result)
    print()
    #2となるので間に1人挟んで"adrianから"cecil"へフォロー関係がつながっている


    #自分を起点として一番遠い人を探す
    dis_to_everyone_from_me=bfs(nicknames[my_name])

    max_dis=max(dis_to_everyone_from_me)
    farthest_id=dis_to_everyone_from_me.index(max_dis)
    farthest_name = [k for k, v in nicknames.items() if v == farthest_id]

    print("{}から他者への最長距離：".format(my_name),format(max_dis))#自分から他者への最長距離： 3
    print("最も遠い人:",farthest_name)#最も遠い人: ['adrian']
    print()



    #他者を起点として一番遠い人を探す

    #全員から自分への距離を記録する配列
    dis_from_everyone_to_me=[bfs(id_)[nicknames[my_name]] for id_ in range(len(nicknames))]

    max_dis_=max(dis_from_everyone_to_me)
    farthest_id_=dis_from_everyone_to_me.index(max_dis_)
    farthest_name_ = [k for k, v in nicknames.items() if v == farthest_id_]

    print("他者から{}への最長距離：".format(my_name),format(max_dis_))#他者から自分への最長距離： 3
    print("最も遠い人:",farthest_name_)#最も遠い人: ['alan']
    print()



    #配列の中身見る用
    #print(dis_from_everyone_to_me==dis_to_everyone_from_me)
    #print(dis_from_everyone_to_me)
    #print(dis_to_everyone_from_me)