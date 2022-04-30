# python-utilities
Python3 によるユーティリティスクリプト

## raise_version.py

### 概要
Ardiono ライブラリの為の[セマンティックバージョニング](https://semver.org/lang/ja/)に基づくバージョン進行  
バージョンを上げ、存在すれば **library.properties** と **library.json** を更新します。  
必要ならば C スタイルのバージョン define ヘッダを出力します。

### 使い方
library.properties か library.json があるディレクトリ上で実行のこと。  

```
python3 raise_version.py [-h] [--execute] [--raising {MAJOR,MINOR,PATCH}] [--source SOURCE] [--prefix PREFIX] [--info] [--verbose]
```

| オプション | 説明 |
----|---- 
| --execute, -e | バージョン進行を実行する **つけない場合は Dry-run(予行)** |
| --raising {MAJOR,MINOR,PATCH}, -r {MAJOR,MINOR,PATCH} | 進行するバージョン区分の指定(デフォルトではPATCH) |
|--source SOURCE, -s SOURCE |  C スタイルヘッダのパス名 |
| --prefix PREFIX, -p PREFIX | C スタイルヘッダのシンボルに付くプレフィクス(--source指定時には必須) |
|  --info, -i | properties,json のバージョンを表示 |


### 例
library.properties and library.json のバージョンが 2.3.4 とする  
```
python3 raise_version.py --execute --raising MINOR --source lib_version.hpp --prefix YOUR_LIBRARY_PREFIX
```

バージョンが **2.3.4** から **2.4.0** へ進行する  
library.properties と library.json が更新される  

library.properties  
```
version=2.4.0
```

library.json  
```
  "version": "2.4.0",
```

C スタイルヘッダ出力  
lib\_version.hpp  
```C
#ifndef YOUR_LIBRARY_PREFIX_VERSION_HPP
#define YOUR_LIBRARY_PREFIX_VERSION_HPP

#define YOUR_LIBRARY_PREFIX_VERSION_MAJOR 2
#define YOUR_LIBRARY_PREFIX_VERSION_MINOR 4
#define YOUR_LIBRARY_PREFIX_VERSION_PATCH 0

#define YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY_AGAIN(x) #x
#define YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY(x) YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY_AGAIN(x)

#define YOUR_LIBRARY_PREFIX_VERSION_VALUE ((YOUR_LIBRARY_PREFIX_VERSION_MAJOR << 16) | (YOUR_LIBRARY_PREFIX_VERSION_MINOR << 8) | (YOUR_LIBRARY_PREFIX_VERSION_PATCH))
#define YOUR_LIBRARY_PREFIX_VERSION_STRING YOUR_LIBRARY_PREFIX_VERSION_STRINGIFY(YOUR_LIBRARY_PREFIX_VERSION_MAJOR.YOUR_LIBRARY_PREFIX_VERSION_MINOR.YOUR_LIBRARY_PREFIX_VERSION_PATCH)

#endif
```
