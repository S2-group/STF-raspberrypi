# Public hostname or IP address from which STF will be reachable.
export PUBLIC_HOSTNAME="s2examplestf.net"

export HOSTNAME=$(hostname)

# username for accessing STF dashboard
export STF_ADMIN_NAME="admin"

# email for accessing STF dashboard
export STF_ADMIN_EMAIL="admin@fakedomain.com"

# Generate with:
# python -c 'import os; import string; src=string.ascii_letters; secret="".join([src[os.urandom(1)[0] % len(src)] for _ in range(24)]); print(secret);'
export STF_SESSION_SECRET="AAAAAAAAAAAAAAAAAAAAAAAA"

# https://nodejs.org/api/cli.html
# Set to 0 if you are using a self-signed certificate
# Set to 1 otherwise
export STF_NODE_TLS_REJECT_UNAUTHORIZED="0"
