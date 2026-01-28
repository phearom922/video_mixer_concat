"""Semantic version comparison utilities."""


def compare_versions(v1: str, v2: str) -> int:
    """
    Compare two semantic version strings.
    
    Returns:
        1 if v1 > v2
        -1 if v1 < v2
        0 if v1 == v2
    """
    def parse_version(v: str) -> list:
        parts = v.split(".")
        return [int(x) for x in parts]
    
    try:
        v1_parts = parse_version(v1)
        v2_parts = parse_version(v2)
        
        max_len = max(len(v1_parts), len(v2_parts))
        v1_parts.extend([0] * (max_len - len(v1_parts)))
        v2_parts.extend([0] * (max_len - len(v2_parts)))
        
        for i in range(max_len):
            if v1_parts[i] > v2_parts[i]:
                return 1
            elif v1_parts[i] < v2_parts[i]:
                return -1
        return 0
    except (ValueError, AttributeError):
        # If parsing fails, do string comparison
        if v1 > v2:
            return 1
        elif v1 < v2:
            return -1
        return 0


def is_newer_version(latest: str, current: str) -> bool:
    """Check if latest version is newer than current."""
    return compare_versions(latest, current) > 0
