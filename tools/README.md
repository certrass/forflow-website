# Local Operator Tools

## Veee proxy wrapper

Use this when Veee has been restarted or switched to another node and outbound
commands such as GitHub, Netlify, npm, or curl start failing.

Print the proxy environment detected from the current Veee listener ports:

```bash
tools/with-veee-proxy.sh
```

Run one command through the current Veee ports:

```bash
tools/with-veee-proxy.sh gh auth status -h github.com
tools/with-veee-proxy.sh git ls-remote https://github.com/octocat/Hello-World.git HEAD
tools/with-veee-proxy.sh curl -I --max-time 12 https://github.com
```

Load the current Veee ports into the active shell:

```bash
eval "$(tools/veee-proxy-env.sh)"
```
