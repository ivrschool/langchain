from langgraph_sdk import Auth

VALID_TOKENS = {
    "user1-token": {"id": "user1", "name": "Alice"},
    "user2-token": {"id": "user2", "name": "Bob"},
}

auth = Auth()

@auth.authenticate
async def get_current_user(authorization: str | None) -> Auth.types.MinimalUserDict:
    assert authorization, "Missing Authorization Header"
    scheme, token = authorization.split()
    assert scheme.lower() == "bearer", "Must use Bearer token"

    if token not in VALID_TOKENS:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid token")

    return {
        "identity": VALID_TOKENS[token]["id"],
    }
