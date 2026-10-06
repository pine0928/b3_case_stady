from labs.common.fixtures import tiny_packet_records
from labs.common.preprocess import build_flows, direction_only_bursts
from labs.lab4_graph.starter import burst_graph, packet_burst_hierarchical_graph, packet_chain_graph

def main():
    flow = next(f for f in build_flows(tiny_packet_records()) if f.key[0] == "TCP")
    bursts = direction_only_bursts(flow)
    for g in (packet_chain_graph(flow), burst_graph(flow, bursts), packet_burst_hierarchical_graph(flow, bursts)):
        print(f"{g.design}: nodes={len(g.nodes)}, edges={len(g.edges)}, provenance={g.provenance_codes}")
        for e in g.edges:
            print(f"  {e.src:>2} -> {e.dst:<2} {e.relation:<12} provenance={','.join(e.provenance)}")
        print("  explicit:", "; ".join(g.explicit_relations))
        print("  loss:", "; ".join(g.information_loss) if g.information_loss else "none", "\n")

if __name__ == "__main__": main()
