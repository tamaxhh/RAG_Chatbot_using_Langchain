# Compatibility shim: some langchain versions expect RAW_SCHEMA_QUERY to exist in
# langchain_community.graphs.memgraph_graph. Older/newter releases may only define
# SCHEMA_QUERY, which causes ImportError when langchain imports RAW_SCHEMA_QUERY.
# This module sets the alias at runtime so we don't have to modify site-packages.

try:
    from langchain_community.graphs import memgraph_graph as _mg
except Exception:
    # If the package isn't installed yet, do nothing; import-time errors will show later.
    _mg = None

if _mg is not None and not hasattr(_mg, "RAW_SCHEMA_QUERY"):
    # Create an alias so other packages importing RAW_SCHEMA_QUERY work.
    _mg.RAW_SCHEMA_QUERY = getattr(_mg, "SCHEMA_QUERY", None)
