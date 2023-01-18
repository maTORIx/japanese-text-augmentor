# japanese text augmentor

日本語のテキストを、なるべく違いの無い内容で増幅するスクリプトです。

## Example
```
$ python augmentation.py 100 2 今日の天気は晴れなのかもしれないし、雨なのかもしれません
```

## Command description
```
$ python augmentation.py [size] [n_max]
```

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

