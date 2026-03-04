# ============================================================================
# K1RL QUASAR v25 — Redis Configuration (HuggingFace Spaces)
# Container-only environment: Redis runs locally within the Space
# 
# ⚡ v25 ISOLATION:
#   - DB numbers 5-9 (v24 uses 0-4) — zero key collision
#   - Channel prefix "v25:" — zero pub/sub cross-talk
#   - Same password/host/port — shared Redis instance is safe
# ============================================================================

import os

# ── Environment detection ──────────────────────────────────────────────────
IS_HUGGINGFACE_SPACE = os.environ.get('SPACE_ID') is not None
IS_LOCAL_DEV = not IS_HUGGINGFACE_SPACE

# ── Version & Namespace ────────────────────────────────────────────────────
QUASAR_VERSION = "v25"
CHANNEL_PREFIX = "v25:"  # Prefixed to ALL pub/sub channel names

# ── Credentials ─────────────────────────────────────────────────────────────
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD", "k1rl_099a0c008e32300dc3c14189")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

# ── Host selection ─────────────────────────────────────────────────────────
if IS_HUGGINGFACE_SPACE:
    # HuggingFace Spaces: Redis runs inside container
    REDIS_HOST = "127.0.0.1"
elif IS_LOCAL_DEV:
    # Local development
    REDIS_HOST = os.environ.get("REDIS_HOST", "127.0.0.1")
else:
    # Production server fallback
    REDIS_HOST = os.environ.get("REDIS_HOST", "145.241.100.50")

# ── Connection URLs ────────────────────────────────────────────────────────
# v25 default DB is 5 (metrics) — shifted from v24's DB 0
REDIS_URL = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/5"

# ── Database selection (v25: DBs 5-9) ─────────────────────────────────────
# v24 uses DBs 0-4, v25 uses DBs 5-9 — complete isolation
#
#   DB │ v24 Purpose     │ v25 Purpose      │
#   ───┼─────────────────┼──────────────────│
#    0 │ Metrics         │ (reserved v24)   │
#    1 │ Visitors        │ (reserved v24)   │
#    2 │ Cache           │ (reserved v24)   │
#    3 │ Features        │ (reserved v24)   │
#    4 │ Rewards         │ (reserved v24)   │
#    5 │ —               │ Metrics      ◄── │
#    6 │ —               │ Visitors     ◄── │
#    7 │ —               │ Cache        ◄── │
#    8 │ —               │ Features     ◄── │
#    9 │ —               │ Rewards      ◄── │
#
REDIS_DB_METRICS  = 5    # Real-time metrics
REDIS_DB_VISITORS = 6    # Visitor tracking  
REDIS_DB_CACHE    = 7    # General cache
REDIS_DB_FEATURES = 8    # Feature data
REDIS_DB_REWARDS  = 9    # Reward signals

# Connection pool settings
REDIS_POOL_SETTINGS = {
    'max_connections': 20,
    'retry_on_timeout': True,
    'socket_timeout': 5,
    'socket_connect_timeout': 5,
    'health_check_interval': 30
}

# ── Channel name helper ───────────────────────────────────────────────────
def prefixed_channel(channel_name: str) -> str:
    """Add v25 prefix to a channel name.
    
    Usage:
        prefixed_channel("rewards")          → "v25:rewards"
        prefixed_channel("agent_0")          → "v25:agent_0"
        prefixed_channel("final_signals")    → "v25:final_signals"
    
    Already-prefixed channels are returned unchanged:
        prefixed_channel("v25:rewards")      → "v25:rewards"
    """
    if channel_name.startswith(CHANNEL_PREFIX):
        return channel_name
    return f"{CHANNEL_PREFIX}{channel_name}"


def strip_prefix(channel_name: str) -> str:
    """Remove v25 prefix from a channel name (for logging/callbacks).
    
    Usage:
        strip_prefix("v25:rewards")  → "rewards"
        strip_prefix("rewards")      → "rewards"
    """
    if channel_name.startswith(CHANNEL_PREFIX):
        return channel_name[len(CHANNEL_PREFIX):]
    return channel_name


# ── Debug info ─────────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("K1RL QUASAR v25 — Redis Configuration")
    print("=" * 60)
    print(f"Version:      {QUASAR_VERSION}")
    print(f"Chan Prefix:  {CHANNEL_PREFIX}")
    print(f"Environment:  {'HuggingFace Spaces' if IS_HUGGINGFACE_SPACE else 'Local/Production'}")
    print(f"Redis Host:   {REDIS_HOST}")
    print(f"Redis Port:   {REDIS_PORT}")
    print(f"Redis URL:    {REDIS_URL}")
    print(f"Databases:    metrics={REDIS_DB_METRICS}, visitors={REDIS_DB_VISITORS}, "
          f"cache={REDIS_DB_CACHE}, features={REDIS_DB_FEATURES}, rewards={REDIS_DB_REWARDS}")
    print("-" * 60)
    print("Channel examples:")
    for ch in ["rewards", "reward-batches", "agent_0", "meta_features-agent_0", 
               "final_signals", "confirmations:v250", "system-commands"]:
        print(f"  {ch:30s} → {prefixed_channel(ch)}")
    print("=" * 60)
