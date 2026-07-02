from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class AgentNode:
    name: str
    role: Optional[str] = None
    tasks: List[str] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    output: Optional[str] = None


@dataclass
class ProgramNode:
    agents: List[AgentNode] = field(default_factory=list)

    def to_dict(self):
        # Normalize single-agent programs to the example AST shape
        if len(self.agents) == 1:
            a = self.agents[0]
            return {
                "agent": a.name,
                "role": a.role,
                "task": a.tasks[0] if a.tasks else None,
                "input": a.inputs[0] if a.inputs else None,
                "constraints": a.constraints,
                "output": a.output,
            }

        return {"agents": [a.__dict__ for a in self.agents]}
