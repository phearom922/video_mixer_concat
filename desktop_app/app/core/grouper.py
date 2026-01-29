"""Video file grouping logic."""
from pathlib import Path
from typing import List, Tuple
from enum import Enum


class SortMode(Enum):
    """Sorting modes for video files."""
    FILENAME = "filename"
    TIME = "time"
    RANDOM = "random"


class RemainderBehavior(Enum):
    """Behavior for remaining files after grouping."""
    IGNORE = "ignore"
    EXPORT_SINGLE = "export_single"
    WARN = "warn"


def scan_video_files(directory: Path) -> List[Path]:
    """
    Scan directory for video files.

    IMPORTANT (Windows note):
    - เดิมใช้ glob ทั้งตัวพิมพ์เล็กและพิมพ์ใหญ่ (*.mp4 และ *.MP4)
    - บน Windows filesystem ไม่สนใจตัวพิมพ์เล็ก/ใหญ่ ทำให้ไฟล์เดียวกันถูกนับซ้ำ 2 ครั้ง
      เช่น 1.mp4 จะได้ path ซ้ำ → กลายเป็นกลุ่ม [1.mp4, 1.mp4]
    - ผลลัพธ์คือ Group Size = 2 แต่ได้ผลลัพธ์ 4 กลุ่ม: (1+1), (2+2), (3+3), (4+4)

    แก้ไขโดย:
    - อ่านไฟล์ทั้งหมดในโฟลเดอร์ครั้งเดียว
    - filter ตามนามสกุลแบบ lower() เพื่อตัดปัญหา case-sensitive
    - ใช้ set เพื่อกัน path ซ้ำ (เผื่อกรณีอื่น)
    """
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v', '.webm'}

    # Check if directory exists
    if not directory.exists():
        return []
    
    if not directory.is_dir():
        return []

    unique_files = set()
    try:
        for entry in directory.iterdir():
            try:
                if entry.is_file():
                    if entry.suffix.lower() in video_extensions:
                        unique_files.add(entry.resolve())
            except (PermissionError, OSError):
                # Skip files that can't be accessed
                continue
    except (PermissionError, OSError) as e:
        # Directory can't be read
        return []

    # แปลงกลับเป็น list และ sort เพื่อให้ลำดับคงที่
    return sorted(unique_files)


def sort_files(files: List[Path], mode: SortMode) -> List[Path]:
    """Sort files according to mode."""
    if mode == SortMode.FILENAME:
        return sorted(files)
    elif mode == SortMode.TIME:
        return sorted(files, key=lambda p: p.stat().st_mtime)
    elif mode == SortMode.RANDOM:
        import random
        shuffled = files.copy()
        random.shuffle(shuffled)
        return shuffled
    else:
        return files


def group_files(
    files: List[Path],
    group_size: int,
    sort_mode: SortMode = SortMode.FILENAME,
    remainder_behavior: RemainderBehavior = RemainderBehavior.IGNORE
) -> Tuple[List[List[Path]], List[Path]]:
    """
    Group video files.
    
    Returns:
        (groups, remainder)
    """
    if group_size < 2:
        raise ValueError("Group size must be at least 2")
    
    sorted_files = sort_files(files, sort_mode)
    groups = []
    remainder = []
    
    # Create groups
    for i in range(0, len(sorted_files), group_size):
        group = sorted_files[i:i + group_size]
        if len(group) >= group_size:
            groups.append(group)
        else:
            remainder = group
    
    return groups, remainder
