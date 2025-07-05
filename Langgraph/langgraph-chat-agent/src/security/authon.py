from langgraph_sdk import Auth

# This is our toy user database. Do not use this in production.
VALID_TOKENS = {
    "user1-token": {"id": "user1", "name": "Alice"},
    "user2-token": {"id": "user2", "name": "Bob"},
}

auth = Auth()

@auth.authenticate
async def get_current_user(authorization: str | None) -> Auth.types.MinimalUserDict:
    assert authorization
    scheme, token = authorization.split()
    assert scheme.lower() == "bearer"
    
    if token not in VALID_TOKENS:
        raise Auth.exceptions.HTTPException(status_code=401, detail="Invalid token")

    user_data = VALID_TOKENS[token]
    return {
        "identity": user_data["id"]
    }

@auth.on
async def add_owner(ctx: Auth.types.AuthContext, value: dict):
    """Make resources private to their creator."""
    filters = {"owner": ctx.user.identity}
    metadata = value.setdefault("metadata", {})
    metadata.update(filters)
    return filters

@auth.on.threads.create
async def on_thread_create(ctx: Auth.types.AuthContext, value: dict):
    metadata = value.setdefault("metadata", {})
    metadata["owner"] = ctx.user.identity
    return {"owner": ctx.user.identity}

@auth.on.threads.read
async def on_thread_read(ctx: Auth.types.AuthContext, value: dict):
    return {"owner": ctx.user.identity}

@auth.on.assistants
async def on_assistants(ctx: Auth.types.AuthContext, value: dict):
  if ctx.user.identity == "user2":
    raise Auth.exceptions.HTTPException(
        status_code=403,
        detail="User lacks the required permissions."
    )
  else:
    return {
        "identity": ctx.user.identity,
        "is_authenticated": True
    }