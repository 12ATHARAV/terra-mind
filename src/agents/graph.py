from langgraph.graph import StateGraph, END
from src.agents.state import AgentGraphState
from src.agents.nodes import (
    triage_intake_node, clarification_node, spatial_reasoning_node,
    retrieval_node, synthesis_auditor_node
)


def route_triage(state: AgentGraphState) -> str:
    if state.get("is_clarification_required", False):
        return "clarification_node"
    return "spatial_reasoning_node"


def build_biodiversity_graph():
    builder = StateGraph(AgentGraphState)
    builder.add_node("triage_node", triage_intake_node)
    builder.add_node("clarification_node", clarification_node)
    builder.add_node("spatial_reasoning_node", spatial_reasoning_node)
    builder.add_node("retrieval_node", retrieval_node)
    builder.add_node("synthesis_auditor_node", synthesis_auditor_node)
    builder.set_entry_point("triage_node")
    builder.add_conditional_edges("triage_node", route_triage, {
        "clarification_node": "clarification_node",
        "spatial_reasoning_node": "spatial_reasoning_node"
    })
    builder.add_edge("clarification_node", END)
    builder.add_edge("spatial_reasoning_node", "retrieval_node")
    builder.add_edge("retrieval_node", "synthesis_auditor_node")
    builder.add_edge("synthesis_auditor_node", END)
    return builder.compile()


graph = build_biodiversity_graph()
