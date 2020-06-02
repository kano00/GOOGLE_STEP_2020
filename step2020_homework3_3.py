def readNumber(line, index):
  number = 0
  while index < len(line) and line[index].isdigit():
    number = number * 10 + int(line[index])
    index += 1
  if index < len(line) and line[index] == '.':
    index += 1
    keta = 0.1
    while index < len(line) and line[index].isdigit():
      number += int(line[index]) * keta
      keta /= 10
      index += 1
  token = {'type': 'NUMBER', 'number': number}
  return token, index


def readPlus(line, index):
  token = {'type': 'PLUS'}
  return token, index + 1


def readMinus(line, index):
  token = {'type': 'MINUS'}
  return token, index + 1


def readTimes(line, index):
  token = {'type': 'Times'}
  return token, index + 1


def readDivision(line, index):
  token = {'type': 'Division'}
  return token, index + 1

def readBracketLeft(line, index):
  token = {'type': 'BracketLeft'}
  return token, index + 1

def readBracketRight(line, index):
  token = {'type': 'BracketRight'}
  return token, index + 1

def tokenize(line):
  tokens = []
  index = 0
  while index < len(line):
    if line[index].isdigit():
      (token, index) = readNumber(line, index)
    elif line[index] == '+':
      (token, index) = readPlus(line, index)
    elif line[index] == '-':
      (token, index) = readMinus(line, index)
    elif line[index] == '*':
      (token, index) = readTimes(line, index)
    elif line[index] == '/':
      (token, index) = readDivision(line, index)
    elif line[index] == '(':
      (token, index) = readBracketLeft(line, index)
    elif line[index] == ')':
      (token, index) = readBracketRight(line, index)
    else:
      print('Invalid character found: ' + line[index])
      exit(1)
    tokens.append(token)
  return tokens

"""
字句の並びで乗算除算のみ計算して新しいtokensを返す関数
引数：tokens　list型　ただしBracketRightやBracketLeftの無いtokens
返り値：tokens　list型　TimesやDivisionのないtokensを返す
"""
def evaluateTimesDivision(tokens):
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'Times':
        # 乗算記号の前の数字を計算結果で書き換える
        tokens[index - 2]['number'] *= tokens[index]['number']
        # 乗算記号と乗算記号の後ろの数字をtokensから消す
        del tokens[index-1:index+1]
        index -= 2

      elif tokens[index - 1]['type'] == 'Division':
        # 0除算があれば計算を止める
        if tokens[index]['number'] == 0:
            print("Don't divide number by 0")
            exit(1)

        tokens[index - 2]['number'] /= tokens[index]['number']
        del tokens[index-1:index+1]
        index -= 2
      else:
        pass
    index += 1
  return tokens

"""
字句の並びで括弧内のみを計算して新しいtokensを返す関数
引数：tokens　list型
返り値：tokens　list型　BracketRightやBracketLeftの無いtokensを返す
"""
def evaluateBrackets(tokens):
  index = 1
  while index < len(tokens):
    #まず右括弧を探す
    if tokens[index]['type'] == 'BracketRight':
      right=index
      #右括弧があれば左に向かって左括弧を探す
      while tokens[index]['type'] != 'BracketLeft':
          index-=1
          #左括弧がなければ計算を止める
          if index >= len(tokens):
            print('Invalid syntax')
            exit(1)

      #左括弧から右括弧までを計算する
      left=index
      number=evaluate(tokens[left+1:right])
      tokens[left]={'type': 'NUMBER', 'number': number}

      # ()と括弧内の数字をtokensから消す
      del tokens[left+1:right+1]

    else:
      pass
    index += 1
  return tokens


"""
字句の並びを計算する関数
引数：tokens　list型
返り値：answer　float型　字句の並びの計算結果
"""
def evaluate(tokens):
  answer = 0
  tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token

  #括弧内の計算を行う
  tokens=evaluateBrackets(tokens)

  # 乗算除算のみを行う
  tokens=evaluateTimesDivision(tokens)
  
  # 字句の並びを計算する（メインの計算）
  index = 1
  while index < len(tokens):
    if tokens[index]['type'] == 'NUMBER':
      if tokens[index - 1]['type'] == 'PLUS':
        answer += tokens[index]['number']
      elif tokens[index - 1]['type'] == 'MINUS':
        answer -= tokens[index]['number']
      else:
        print('Invalid syntax')
        exit(1)
    index += 1
  return answer


def test(line):
  tokens = tokenize(line)
  actualAnswer = evaluate(tokens)
  expectedAnswer = eval(line)
  if abs(actualAnswer - expectedAnswer) < 1e-8:
    print("PASS! (%s = %f)" % (line, expectedAnswer))
  else:
    print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
  print("==== Test started! ====")
  # 加算減算
  test("1+2")
  test("1.0+2.1")
  test("1.0+2.1-3.0")
  # 乗算除算
  test("1*2")
  test("1.0*2.1")
  test("0*2.0")
  test("3.0-1.0*2.1")
  test("3.0+4.0/2.0")

  # 括弧内計算
  test("2*(2+3)")
  test("2.0*(2.0+3.0)")
  test("2.0*(2.0*3.0)/3.0")
  test("2.0*(2.0*(1.0+2.0))/3.0")
  test("2.0*(2.0*(1.0+2.0))-(2+3)*2")

  # 0除算
  #test("2/0+5")

  print("==== Test finished! ====\n")

runTest()

while True:
  print('> ', end="")
  line = input()
  tokens = tokenize(line)
  answer = evaluate(tokens)
  print("answer = %f\n" % answer)
