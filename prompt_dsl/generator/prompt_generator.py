from prompt_dsl.ast.nodes import ProgramNode


ROLE_TEMPLATES = {
    "SUMMARIZER": "You are a helpful summarizer.",
}

CONSTRAINT_TEMPLATES = {
    "BRIEF": "Keep the response concise.",
}


class PromptGenerator:
    @staticmethod
    def generate(program: ProgramNode) -> str:
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
