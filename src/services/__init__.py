import os
from supabase import create_client, Client


def get_supabase_cli():
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")

    supabase_cli: Client = create_client(url, key)

    return supabase_cli
