# japanese text augmentor

日本語のテキストを、なるべく違いの無い内容で増幅するスクリプトです。

## Example
```
$ python augmentation.py 10 2 外の天気は晴れなのかもしれないし、曇りなのかもしれません
外の天気は晴天なのかもしれないし、曇なのかもしれません。
外の天気は晴天なのかもしれないし、曇天なのかもしれません。
外の天気は上天気なのかもしれないし、曇天なのかもしれません。
外の天気は上天気なのかもしれないし、曇なのかもしれません。
外の天候は晴れなのかもしれないし、曇天なのかもしれません。
外の天気は快晴なのかもしれないし、曇天なのかもしれません。
外の天候は晴れなのかもしれないし、曇なのかもしれません。
外の天気模様は晴れなのかもしれないし、曇天なのかもしれません。
外の天気は好晴なのかもしれないし、曇天なのかもしれません。
外の天気は好天なのかもしれないし、曇天なのかもしれません。
```

上から表現の近い順番に出力されていきます。文章ベクトルの取得には、`rinna/japanese-gpt2-small`を利用しています。

## Command description
```
$ python augmentation.py [gen_max] [n_max]
```

`gen_max`は基本的に生成される文章の数を示しています。しかし、単語数と類義語の数、また`n_max`によって生成可能なパターンの総数が`gen_max`を下回るとき、スクリプトが生成する文章の量は`gen_max`より少なくなる可能性があります
`n_max`は元となる文章から確実に変更しなければならない単語の量を示しています。たとえば、`n_max=1`ならば、文章のうち1つの単語が類義語に置き換わります。同様に2の場合は、必ず2つの単語が類義語に置き換わります。(この際、単語が1つだけしか変更されない文章を生成することはありません).また、変更可能な単語数が限られる(たとえば、文章が短いなど)ことで、`n_max`の変更部分を確保できない場合は、自動的に変更部分は確保しうる最大数に調整されます。

Use NVIDIA GPU
```
$ DEVICE="cuda" python augmentation.py [size] [n_max]
```

## Requirements
```
mecab-python3
unidic-lite
torch
transformers
sentencepiece
```

torchのインストールをrequirementsでやると、インストールできなかったりするのでrequirements.txtは用意していません。

## Run on docker
### NVIDIA GPU
```
$ docker run --name pytorch --gpus all -d \
        -v $(pwd):/workspace \
        nvcr.io/nvidia/pytorch:22.04-py3 \
        /usr/bin/sleep infinity
$ docker exec -it pytorch /bin/bash
in docker $ pip install mecab-python3 unidic-lite torch transformers sentencepiece
in docker $ DEVICE="cuda" python augmentation.py [size] [n_max] [text]
```

