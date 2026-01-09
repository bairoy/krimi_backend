# ===============================
# ENV
# ===============================
import os
from dotenv import load_dotenv
load_dotenv()

# ===============================
# IMPORTS (LATEST)
# ===============================
from typing_extensions import TypedDict, Annotated
from typing import Literal
import operator
from langchain_core.runnables import RunnableConfig

from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_core.messages import (
    AnyMessage,
    HumanMessage,
    AIMessage,
    ToolMessage,
    SystemMessage,
)

from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.postgres import PostgresSaver

# ===============================
# LLM
# ===============================
model = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# ===============================
# TOOLS
# ===============================
@tool
def multiply(a: int, b: int) -> int:
    """
    Docstring for multiply
    
    :param a: Description
    :type a: int
    :param b: Description
    :type b: int
    :return: Description
    :rtype: int
    """
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """
    Docstring for divide
    
    :param a: Description
    :type a: int
    :param b: Description
    :type b: int
    :return: Description
    :rtype: float
    """
    return a / b

tools = [multiply, divide]
tools_by_name = {t.name: t for t in tools}
llm_with_tools = model.bind_tools(tools)

# ===============================
# STATE
# ===============================
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]

# ===============================
# NODES
# ===============================
def llm_call(state: MessagesState):
    response = llm_with_tools.invoke(
        [SystemMessage(content="You are a helpful assistant.")]
        + state["messages"]
    )
    return {"messages": [response]}

def tool_node(state: MessagesState):
    last = state["messages"][-1]
    outputs = []

    for call in last.tool_calls:
        tool = tools_by_name[call["name"]]
        result = tool.invoke(call["args"])
        outputs.append(
            ToolMessage(
                content=str(result),
                tool_call_id=call["id"]
            )
        )
    return {"messages": outputs}

def should_continue(state: MessagesState) -> Literal["tools", END]:
    last = state["messages"][-1]
    if isinstance(last, AIMessage) and last.tool_calls:
        return "tools"
    return END

# ===============================
# GRAPH
# ===============================
builder = StateGraph(MessagesState)

builder.add_node("llm", llm_call)
builder.add_node("tools", tool_node)

builder.add_edge(START, "llm")
builder.add_conditional_edges("llm", should_continue, ["tools", END])
builder.add_edge("tools", "llm")
db_url = os.getenv("SUPABASE_DATABASE_URL")


# with PostgresSaver.from_conn_string(db_url) as checkpointer:
        
#     agent = builder.compile (checkpointer=checkpointer)
            
checkpointer_cm = PostgresSaver.from_conn_string(db_url)
checkpointer = checkpointer_cm.__enter__()
agent = builder.compile(checkpointer=checkpointer)