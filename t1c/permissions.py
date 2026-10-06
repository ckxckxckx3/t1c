ROLE_PERMISSIONS = {
    "admin": {
        "workspace:read",
        "workspace:write",
        "workspace:delete",
        "users:read",
        "users:manage",
    },
    "member": {
        "workspace:read",
        "workspace:write",
        "users:read",
        "users:manage",
    },
    "viewer": {
        "workspace:read",
    },
}
