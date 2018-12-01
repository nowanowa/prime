# prime

1,000,000までの素因数分解を収録したjsonデータと、それを出力するためのpythonコードがあります。


## prime/factorization/*.json

0以上999999（=10^6-1）以下の整数の素因数分解を10万ごとに収録した10個のjsonファイルです。各ファイル**i.json**（i=0,1,…,9）には、i\*100000からi\*100000+99999までの整数の素因数分解が収録されていて、次のようなデータ構造をしています。

    {
      "767": [
        {"p": 13, "e": 1},
        {"p": 59, "e": 1}
      ],
      "768": [
        {"p": 2, "e": 8},
        {"p": 3, "e": 1}
      ],
      "769": [
        {"p": 769, "e": 1}
      ]
    }

`"p"`は prime factor（素因数）、`"e"`は exponent（指数）の頭文字です。上記の例なら、次のような素因数分解を意味します。

- 767 = 13^1 * 59^1
- 768 = 2^8 * 3^1
- 769 = 769^1

なお、実装の都合により`"0"`と`"1"`のフィールドが存在します。次のような配列が格納されています。

    {
      "0": [{"p": 0, "e": 1}],
      "1": []
    }


### サンプルコード

与えられた整数`n`（0以上100万未満）の素因数分解をこれらのファイルから取得して、素因数分解を表す数式（文字列）にしてコンソールに出力するJavaScriptの関数`getPrimeFactorization`は、次のようになります。

    function getPrimeFactorization(n){
      const d = Math.floor(n / 100000);
      const xml = new XMLHttpRequest();
      xml.onreadystatechange = function(){
        if (xml.readyState == 4 && xml.status == 200) {
          const numbers = JSON.parse(xml.response);
          const factors = numbers[n];
          let formula = n + ' = ';
          const l = factors.length;
          for (let i = 0; i < l; i++) {
            const f = factors[i];
            const p = f.p;
            const e = f.e;
            formula += (i == 0 ? '' : ' * ') + p + (e == 1 ? '' : '^' + e);
          }
          console.log(formula);
        }
      };
      xml.open('GET','https://raw.githubusercontent.com/nowanowa/prime/master/factorization/' + d + '.json');
      xml.send();
    }

※`getPrimeFactorization(1)`とするとコンソールに`1 = `を出力してしまいますが、あくまでサンプルなので気にしないでください。


## prime/soinsu.py

素因数分解を収録したjsonファイルを生成するための関数たちです。

    $ python
    >>> import soinsu

- **soinsu.bunkai(sup, numbers=None)**

0以上sup未満の整数の素因数分解が収録された辞書オブジェクトを返します。この辞書オブジェクトを第2引数として与えることで、それまでの結果を再利用して計算を進めることができます。

    >>> numbers = soinsu.bunkai(1000)
    >>> numbers[768]
    [{"p": 2, "e": 8}, {"p": 3, "e": 1}]

- **soinsu.letterall(numbers)**
- **soinsu.letter(n)**
- **soinsu.checkall(numbers)**
- **soinsu.calc(n)**

素因数分解を表す配列`n`、もしくは配列が格納された辞書オブジェクト`numbers`に対して、チェックをするための関数です。**letter**は素因数分解の数式をprintし、**calc**は実際に計算をします。

    >>> soinsu.letter(numbers[768])
    768 = 1 * 2^8 * 3^1
    >>> soinsu.calc(numbers[768])
    768

- **soinsu.slice(numbers, inf, sup)**

`numbers`に収録された素因数分解のうち、`inf`以上`sup`未満の整数に対応するものを取り出します。

    >>> soinsu.slice(numbers, 7, 10)
    {"7": [{"p": 7, "e": 1}], "8": [{"p": 2, "e": 3}], "9": [{"p": 3, "e": 2}]}

- **soinsu.dump(numbers, path='./factorization-dump.json')**

`path`で指定されたファイルへ、json形式に変換した`numbers`を出力します。


### 自動生成

コマンドラインから

    $ python soinsu.py

を実行すると、./factorization/ディレクトリ以下に、i.json（i=0,1,…,9）を生成します（はじめに説明したものと同じ10個のjsonファイルです）。


