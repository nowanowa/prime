# prime

正整数の素因数分解です。


## prime/factorization/*.json

0以上999999（=10^6-1）以下の整数の素因数分解を、10万ごとに収録したjsonです。次のようなデータ構造をしています。

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

各ファイル "i.json" には、`i * 100000`から`(i + 1) * 100000 - 1`までの整数の素因数分解が収録されています。


### サンプルコード

与えられた整数`n`（0以上100万未満）の素因数分解をこれらのファイルから取得して、数式文字列にしてコンソールに出力するJavaScriptの関数`getPrimeFactorization()`は、次のようになります。

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
      xml.open('GET','https://raw.githubusercontent.com/nowanowa/prime/factorization/' + d + '.json');
      xml.send();
    }

※`getPrimeFactorization(1)`とするとコンソールに`"1 = "`を出力してしまいますが、あくまでサンプルなので気にしないでください。


## prime/soinsu.py

コマンドラインから

    $ python soinsu.py

を実行すると、./factorization/ディレクトリ以下に、i.json（i=0,1,…,9）を生成します。上記で説明したのと同じjsonファイルです。

### soinsu.bunkai(n)

nまでの素因数分解の辞書を返します。


