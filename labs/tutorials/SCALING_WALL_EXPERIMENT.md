# Scaling-Wall Experiment Tutorial

## 目的

この教材の目的は、学生に「大規模ならstreamingが必要」と先に教えることではない。小規模PCAPで便利だったanalysis-first pathを少し大きくし、**どこで、なぜ、息づまるのか**を観察する。

ここでのゴールはPCをクラッシュさせることではない。安全なサイズで傾向を見て、原因を説明できるようにする。

## Learning question

> なぜ、PCAPをPython objectとして積み上げる設計は研究用の大規模PCAPで苦しくなるのか？

## Measurement contract

測るものは次の通り。

| item | 説明 |
|---|---|
| PCAP size | disk上のファイルサイズ |
| packet count | readerが扱ったpacket数 |
| wall-clock time | 処理開始から終了までの時間 |
| peak RSS | Python processが使った最大resident memory |
| retention policy | packet objectやrowをlist等に残したか |
| surviving state | 本当に最後まで必要だった情報 |

重要なのは、PCAP sizeだけを見ることではない。**disk上のbinary capture**と**Python上のdecoded objects**は同じ大きさではない。

## Step W1 — まず予想する

実行前に予想を書く。

- PCAP sizeを10倍にしたら、処理時間は何倍になりそうか？
- peak RSSは何倍になりそうか？
- なぜそう思うか？

## Step W2 — analysis-first codeをそのまま使う

最初はあえて、これまで便利だった設計を使う。

典型的には次の形である。

```python
records = []
for packet in reader:
    records.append(packet)
```

この設計は分かりやすい。後から全packetを見返せる。しかし、処理済みpacketもmemoryに残り続ける。

## Step W3 — peak RSSを測る

環境によって測定方法は異なる。

Unix系では、次のような方法が使える場合がある。

```bash
/usr/bin/time -v python -m labs.lab0_pcap.demo path/to/capture.pcap
```

Pythonから簡易的に測る場合は、`resource` moduleを使える環境もある。

```python
import resource
rss_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
```

OSにより単位が異なるため、授業では同じ環境で相対比較する。

## Step W4 — 観察結果を書く

次の表を埋める。

| capture | size | packets | time | peak RSS | retained objects? | note |
|---|---:|---:|---:|---:|---|---|
| tiny | | | | | | |
| medium | | | | | | |
| larger | | | | | | |

安全のため、trendが見えたらそこで止める。巨大ファイルで無理をしない。

## Step W5 — なぜmemoryが増えるか説明する

次の図を自分の言葉で説明する。

```text
PCAP bytes on disk
      ↓ decode
Python packet objects
      ↓ append
list / DataFrame / materialized rows
      ↓
processed packets also remain resident
```

問い:

> packet Nを処理しているとき、packet 1..N-1の情報は本当に全部必要か？

flow countだけが欲しいなら、全packet objectは不要かもしれない。burstの現在状態だけなら、最後のdirectionと現在burstだけで足りるかもしれない。

## Step W6 — 息づまりの原因を一文で言う

良い説明:

> PCAPが大きいことだけが問題ではない。decodeしたPython objectをlistに積み上げ、処理済みpacketまで保持する設計なので、memoryがpacket数に比例して増える。

弱い説明:

> PCAPが大きいからメモリが足りない。

## Step W7 — 次の設計へ進む

ここまで来て初めて、streaming designを学ぶ理由ができる。

次の問い:

> 全packetを保持せず、1 packetずつ処理し、必要なstateだけ残すにはどうすればよいか？

この問いから、TShark CLI、TSV、`csv.reader`、`subprocess.run`、`Popen`、`PIPE`、generator、`yield`へ進む。

## M1 exit evidence

M1では、次を示す。

- Lab 0–2のpacket / flow / session / burst evidence
- PCAP sizeを変えたmeasurement table
- peak RSSまたはmemory trendの観察
- materializationがなぜ息づまりを生むかの説明
- streamingをまだ実装していなくても、なぜ必要になるかの説明
