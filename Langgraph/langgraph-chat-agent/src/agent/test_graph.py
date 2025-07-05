from graph import graph

result = graph.invoke({"messages": [{"role": "user", "content": "Hi! I am Pankaj."}]})

print(result["messages"][-1].content)