from prompt_dsl.ast.nodes import ProgramNode


ROLE_TEMPLATES = {
    "TEACHER": "You are an experienced teacher.",
    "ENVIRONMENTALEXPERT": "You are an Environmental Expert.",
    "DATA_SCIENTIST": "You are an experienced data scientist.",
}

CONSTRAINT_TEMPLATES = {
    "STEPBYSTEP": "Provide step-by-step reasoning.",
    "BRIEF": "Keep the response concise.",
}


class PromptGenerator:
    @staticmethod
    def generate(program: ProgramNode) -> str:
        # For now take the first agent
        agent = program.agents[0]

        parts = []

        # Role
        role = agent.role or ""
        role_key = role.replace(" ", "").upper() if role else ""
        parts.append(ROLE_TEMPLATES.get(role_key, f"You are an {role}.") if role else "")

        # Task
        if agent.tasks:
            parts.append("Task:")
            parts.append(agent.tasks[0])

        # Input
        if agent.inputs:
            parts.append("")
            parts.append(f"Input: {agent.inputs[0]}")

        # Constraints
        if agent.constraints:
            parts.append("Instructions:")
            for c in agent.constraints:
                key = c.replace(" ", "").upper()
                parts.append(f"- {CONSTRAINT_TEMPLATES.get(key, c)}")

        # Memory
        if agent.memory:
            parts.append("Maintain context from previous interactions.")

        # Tools
        if agent.tools:
            tools_str = ", ".join(t.lower() for t in agent.tools)
            parts.append(f"You may use {tools_str} tools when needed.")

        # RAG
        if agent.rag:
            parts.append("Use retrieval augmented generation (RAG) when appropriate.")

        # Output
        if agent.output:
            out = agent.output.upper()
            if out == "JSON":
                parts.append("Return response as JSON.")
            elif out == "MARKDOWN":
                parts.append("Return response formatted in Markdown.")
            elif out == "XML":
                parts.append("Return response formatted as XML.")
            else:
                parts.append(f"Return response as {agent.output}.")

        # Join parts into final prompt
        prompt = "\n\n".join(p for p in parts if p)
        return prompt
