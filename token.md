

```bash
# Option 1: Force token refresh (recommended)
azd auth login --use-device-code
```

This will:
- Re-authenticate and refresh the token cache
- Reload the subscription list with current permissions
- Not require manual cache deletion

**Alternative approaches:**

```bash
# Option 2: Just re-run azd auth login
azd auth login
```

```bash
# Option 3: If the above don't work, logout and login
azd auth logout
azd auth login
```

**Root cause**: The teammate (`babal@microsoft.com`) likely gained access to subscription `80ef7369-572a-4abd-b09a-033367f44858` after their last `azd auth login`. The cached token doesn't include this subscription in its claims, so `azd` needs to refresh.

**Quick fix**: Have your teammate run:
```bash
azd auth login --use-device-code
```

This forces a fresh authentication flow and updates the cached subscription list. The `--use-device-code` flag ensures a clean refresh through the browser.