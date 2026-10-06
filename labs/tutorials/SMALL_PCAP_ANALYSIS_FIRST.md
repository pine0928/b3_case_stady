# Small-PCAP Observation-First Tutorial

## 目的

この教材では、小さなPCAPを使って **packetを観察し、protocol fieldの意味を確認し、再現可能に抽出する** ところから始める。

Core courseの標準経路は最初から最後まで次である。

```text
PCAP / pcapng
    ↓
Wireshark — 人がprotocol structureとfield meaningを確認する
    ↓
TShark — 同じfieldを再現可能に抽出する
    ↓
Python — fieldをPacketRecordへ写像する
    ↓
FlowKey / Flow → Burst → Analysis
```

Scapyや自作PCAP binary parserはCoreでは使わない。

## Learning question

> PCAPから何を観測でき、その観測をどのように再現可能なPython分析へ渡すのか？

## Step 1 — Wiresharkで1 packetを見る

`labs/data/canonical_smoke.pcap` をWiresharkで開く。まずTCP packetを一つ選び、次を階層として確認する。

```text
Frame
 └─ Ethernet
     └─ IPv4
         └─ TCP
```

UDP packetについても同じことを行う。

最初に確認するfieldは次で十分である。

- IPv4 source / destination address
- IP protocol number
- TCPまたはUDP source / destination port
- IPv4 total length
- TCP flags（TCPの場合）

ここではoffsetやpacket bytesを手作業でparseしない。重要なのは、**値がどのprotocol headerのどのfieldから来るか**を説明できることである。

## Step 2 — 同じfieldをTSharkで取り出す

まず少数のfieldだけを指定する。

```bash
tshark -n -r labs/data/canonical_smoke.pcap \
  -Y "ip && (tcp || udp)" \
  -T fields \
  -e frame.time_epoch \
  -e ip.src -e ip.dst -e ip.proto \
  -e tcp.srcport -e tcp.dstport \
  -e udp.srcport -e udp.dstport
```

ここで説明できるようにする。

- `-r` は何を読むか
- `-Y` はどのpacketを残すか
- `-T fields` は何を出力するか
- `-e ip.src` などのfield名がWiresharkのどこに対応するか
- TCP rowでUDP columnが空になる理由（その逆も同様）

## Step 3 — Lab 0の完全なfield contractを見る

```bash
python -m labs.tools.inspect_pcap labs/data/canonical_smoke.pcap
```

このコマンドはraw TShark TSVを表示するだけであり、`PacketRecord`への変換はしない。

完全なfield contractにはlength、TCP flags、captured/original frame lengthも含まれる。`labs/lab0_pcap/SPECIFICATION.md` とWiresharkを照合して意味を確認する。

## Step 4 — PythonでPacketRecordへ写像する

`labs/lab0_pcap/starter.py` の `parse_tshark_row()` を実装する。

ここで初めて、raw observationをcourse共通表現へ変換する。

```text
TShark TSV row
      ↓
parse_tshark_row()
      ↓
PacketRecord
```

`PacketRecord`はPCAPそのものではない。研究で使うために選んだfieldだけを保持する**representation boundary**である。

考えること:

- `packet_length`をなぜ`frame.len`ではなく`ip.len`とするのか
- TCPとUDPでpayload lengthの意味がどう違うか
- IP addressやportをML featureとしてそのまま使ってよいか
- 何をPacketRecordに入れた時点で、何を捨てたことになるか

## Step 5 — Lab 1への接続

Lab 1以降はPCAP bytesを扱わない。Lab 0で作った`PacketRecord`を入力として、

```text
PacketRecord → bidirectional FlowKey / Flow → Burst → Analysis
```

へ進む。

つまりLab 0の出口が、そのまま後続Labの入口になる。

## Exit condition

次を自分の言葉で説明できればLab 0へ進む準備ができている。

1. Wiresharkで見たfieldとTSharkの`-e` field名の対応。
2. TSharkがPCAPのprotocol dissectionを担当すること。
3. PythonがTSharkの観測を`PacketRecord`へ写像すること。
4. observed fieldとderived representationの違い。

## Scope

Large-PCAP streaming、pipe、generator、memory scalingは研究規模で必要になる発展テーマである。Core Lab 0–3では、まずprotocol observationからtraffic representationまでの一本の流れを確実に身につける。
