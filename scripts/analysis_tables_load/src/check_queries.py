"""SQL statements check the analytics tables for issues.

:authors
    JP at 19/04/20
"""
# Check for no duplicate segment IDs
check_segment_id = """
SELECT segment_id FROM analysis.dim_segments GROUP BY segment_id HAVING COUNT(*) > 1
"""

# Check for no duplicate leaderboard IDs
check_leaderboard_id = """
SELECT leaderboard_id FROM analysis.fact_leaderboard GROUP BY leaderboard_id HAVING COUNT(*) > 1
"""

check_queries = [check_segment_id, check_leaderboard_id]
