# 📝 2022/02/27


やっていることを体系化していきたい


## 今の状況

モジュールシンセ（？）的にやっていきたい

リズムは、シーケンスか？




## GeoGebra 用

### `fract`

```
x-floor(x)
```

# 📝 2022/02/16

## 外装

- 音楽の操作ボタン
  - 再生とストップボタンなど
  - 3分を超える演奏にも、対応できるように
- shaderコードのビュー
  - 鳴っているコードが表示できるように
  - シンタックスハイライトと入力補完は置いておいて、`textarea` で実装


## 内装

- class 化
- コード分割


# 📝 2022/02/14


シーケンス的にするか、モジュール的にするか

3分の壁をどう表現さすか



# 📝 2022/02/03

## 波形の吐き出しが逆？

`0.0 ~ 1.0` で出しているので、真ん中から上に行く予定なのに

下にいってしまう？


```.js
for (let i = 0; i < bufferLength; i++) {
  const v = (255 - dataArray[i]) / 128.0;
  //const v = dataArray[i] / 128.0;
  const y = v * HEIGHT / 2;

  // todo: ショートハンドすぎる？
  i === 0 ? vcctx.moveTo(x, y) : vcctx.lineTo(x, y);
  x += sliceWidth;
}
 
```


とりあえず、`255` で逆にしてる。。。


なぜ`255` や。。。？`fftSize = 2048` なんだけどな。。。


## 音

EQ とか、シンセそのものとか


どっちを勉強するか。。。。



あと、3分制限問題はどうしようかな。。。。



### 関数

#### `fract(beat / 2.0);`
素直に上がっていくイメージ、ピッタリ着地


#### `mod(beat, 2.0);`

`1.0` 以上だと、待ってる感じ


#### vec2(clamp(m, -1.0, 1.0);

行き過ぎた部分をカットしてる、音下げてもカットした形で返ってくる


# 📝 2022/01/28

## 参照をしていきたい一覧

[gaz | Qiita](https://qiita.com/gaziya5)

[Try & Error for Sound Program](https://gaziya.hateblo.jp/entry/2021/12/14/191629)


- 感謝の気持ちを持って読み込む


[GLSL Grapher](https://fordhurley.com/glsl-grapher/)

- 実装したら、視覚的にヒントになりそう


## 雑感

シーケンスや、ピッチの部分への注力が多い印象

音色の部分についても、考えていきたい


あと、サイドチェインも



# 📝 2022/01/25


## 音のおべんきょ


値が`-` だと音が出ない？



# 📝 2022/01/24

## 音の作り方おべんきよ

[GLSLで音を作る | らくとあいすの備忘録](https://raku-phys.hatenablog.com/entry/2020/04/19/002400)



### 円周率


手打ちが面倒なので、`acos(-1.0)`


### 短音


`exp(-f * time)` 指数減衰で、一音でおわらせてる。という理解



### 和音


``` .glsl
vec2 mainSound(float time) {
  float pi = acos(-1.0);
  float pi2 = pi * 2.0;
  float sine_wave = sin(pi2 * 440.0 * time);
  float pitch5 = sin(pi2 * 440.0 * 1.5 * time);
  return vec2(0.4 * (sine_wave + pitch5));
}

```

`0.4 *` と、クリップを自身で調整するのが手間かもね

`normalize` ,`length` でも想定の音とはかけ離れてる

なんか、良い関数ないかな？


### エンベロープ

``` .glsl
vec2 mainSound(float time) {
  float pi = acos(-1.0);
  float pi2 = pi * 2.0;
  float envelope = 4.0;
  float sine_wave = sin(pi2 * 440.0 * time);
  
  return vec2(sine_wave * fract(envelope * time));
}

```

`+` はふわっと、`-` は即立ち上がり

`envelope` が大きいほど早い




BPM で`1.0` が`60` か？

`time` で取ってるからそりゃそうか、、、


todo: 

> powerで形を変形したfract、三項演算子で条件分岐したものなど様々なエンベロープを考えることが出来ます。


### ノイズ


``` .glsl
vec2 mainSound(float time) {
  return vec2(fract(sin(time * 1e3) * 1e6) - 0.5);
}

```

``` .glsl
vec2 mainSound(float time) {
  float noise = fract(sin(time * 1e3) * 1e6) - 0.5;
  
  return vec2(noise * fract(-time * 8.0));
}

```


ずっと鳴らしてると、モジュラーみたいな機械音的なのが乗る



#### 組み合わせ

``` .glsl
vec2 mainSound(float time) {
  return vec2((fract(sin(time * 1e3) * 1e6) - 0.5) * pow(fract(-time * 4.0), mod(time * 4.0, 2.0) * 8.0));
}

```




todo:

よくある、ノイズのやつ調べる




## Pythonista の初期呼び出し以降は、前の音が残ってしまう問題


### 結果から

``` .py
def refresh_webview(self):
    self.wv.clear_cache()
    self.wv.reload()
```

呼び出し、更新、終了時。全てにおいてリフレッシュさせている


`clear_cache()` が意図通りにクリアさせているかは、不明



### 道のり

#### `SFSafariViewController`

`SFSafariViewController` にて、local server を立てるのは、console にログを吐くので却下


ログが出てしまうと、強制的にview が変遷してしまい、更新のめんどくささがあった


#### `WKWebView` を作り直す


ミニマムで実装したところ、同様の現象があったため、当初使用の`WKWebView` で継続



## インタラクティブな操作


view をメインで出してしまうと、ソースコード更新の度にview を閉じる必要があったため`panel` にて出すことにした



#### テストリポジトリ


[draftPythonistaScripts](https://github.com/pome-ta/draftPythonistaScripts) に突っ込んでる


## style

はやり、Shader の情報が見たいので表示


しかし、view からはみ出して、横スクロールが面倒なので

``` .css
canvas {
  width: 100%;
}
```

吐き出す音が変わらなければいいけど、、、(クソ耳の私では違いがわからんかったので、採用してる)




# 📝 2022/01/18

ローカルサーバーを立てて、`SFSafariViewController` で呼び出すことにしてみた


終了時の処理が面倒なので、ハンドリングできたら良き


# 📝 2022/01/17


連続でjs 読んじゃうから、delegate でクラッシュさせてる😇


[GLSLで音を作る | らくとあいすの備忘録](https://raku-phys.hatenablog.com/entry/2020/04/19/002400)


# 📝 2022/01/16


とりあえず、簡単な音だけ作りたいけど


emmit なのか、計算量なのか音が出ないから

class 化してみる

読み込み順番の問題？



# 📝 2022/01/13


音は出るようになったけど、Pythonista でview を消しても、音が残る時がある


# 📝 2022/01/12

`this.post300VS` とか


いるのか、、、いらんのか、、、テクスチャにつかうみたい？

# 📝 2022/01/10

## resize


サイズ取得(描画) が少し変？

```
LOG: 398
LOG: 302
```

```
398
226
```

`DOMContentLoaded` の挙動に違いあり？
- Pythonista
- Play.js


