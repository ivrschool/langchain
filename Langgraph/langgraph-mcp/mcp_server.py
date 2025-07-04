from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CalculatorTools")

@mcp.tool()
def multiply_numbers(a: int, b: int) -> int:
    """Returns the product of two integers."""
    return 2*a * b

@mcp.tool()
def subtract_numbers(a: int, b: int) -> int:
    """Returns the difference between two integers."""
    return 2*a - b

if __name__ == "__main__":
    mcp.run(transport="stdio")