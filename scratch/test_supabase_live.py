import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))
from src.db.supabase_client import get_supabase_client

supabase = get_supabase_client()
print("Testing Supabase Client connection...")

for table in ['documentation', 'users', 'chat_history', 'tickets']:
    try:
        res = supabase.table(table).select('id', count='exact').limit(1).execute()
        print(f"Table [{table}]: OK (count: {res.count})")
    except Exception as e:
        print(f"Table [{table}]: ERROR - {e}")

try:
    rpc_res = supabase.rpc('match_documentation', {'query_embedding': [0.0]*768, 'match_threshold': 0.0, 'match_count': 2}).execute()
    print(f"RPC [match_documentation]: OK (returned {len(rpc_res.data)} docs)")
except Exception as e:
    print(f"RPC [match_documentation]: ERROR - {e}")
