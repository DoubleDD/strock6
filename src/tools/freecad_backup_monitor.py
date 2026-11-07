#!/usr/bin/env python3
import argparse
import os
import shutil
import time
from datetime import datetime
from pathlib import Path


def log(message):
    print(f"{datetime.now():%Y-%m-%d %H:%M:%S} {message}", flush=True)


def display_path(path, root):
    try:
        return str(path.relative_to(root))
    except ValueError:
        return str(path)


def unique_destination(destination):
    if not destination.exists():
        return destination
    index = 2
    while True:
        candidate = destination.with_name(f"{destination.name}.{index}")
        if not candidate.exists():
            return candidate
        index += 1


def document_stem(backup_name, stems):
    for stem in stems:
        if backup_name.startswith(stem + "."):
            return stem
    return None


def archive_older_backups(root, backup_root):
    moved = 0
    for current, dirnames, filenames in os.walk(str(root)):
        current_path = Path(current)
        dirnames[:] = [
            name
            for name in dirnames
            if name != ".git" and (current_path / name).resolve() != backup_root
        ]

        stems = sorted(
            (Path(name).stem for name in filenames if name.lower().endswith(".fcstd")),
            key=len,
            reverse=True,
        )
        groups = {}
        for name in filenames:
            if not name.lower().endswith(".fcbak"):
                continue
            stem = document_stem(name, stems)
            if stem is not None:
                groups.setdefault(stem, []).append(current_path / name)

        for backups in groups.values():
            if len(backups) < 2:
                continue
            try:
                backups.sort(key=lambda path: (path.stat().st_mtime_ns, path.name))
            except FileNotFoundError:
                continue
            for source in backups[:-1]:
                destination = unique_destination(
                    backup_root / source.parent.relative_to(root) / source.name
                )
                try:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(source), str(destination))
                    moved += 1
                    log(
                        f"已归档 {display_path(source, root)} -> "
                        f"{display_path(destination, root)}"
                    )
                except (FileNotFoundError, OSError) as exc:
                    log(f"无法归档 {display_path(source, root)}：{exc}",)
    return moved


def parse_args():
    project_root = Path(__file__).resolve().parents[2]
    cad_root = project_root / "cad"
    parser = argparse.ArgumentParser(
        description="每个 FCStd 仅在同目录保留最新 FCBak，其余移入 cad/backup。"
    )
    parser.add_argument("--root", type=Path, default=cad_root, help="要监控的 CAD 模型目录")
    parser.add_argument("--backup-dir", type=Path, help="归档目录，默认为 ROOT/backup")
    parser.add_argument("--interval", type=float, default=2.0, help="轮询间隔秒数，默认 2")
    parser.add_argument("--once", action="store_true", help="只整理一次，不持续监控")
    return parser.parse_args()


def main():
    args = parse_args()
    root = args.root.expanduser().resolve()
    backup_root = (
        args.backup_dir.expanduser().resolve()
        if args.backup_dir
        else root / "backup"
    )
    if not root.is_dir():
        raise SystemExit(f"监控目录不存在：{root}")
    if args.interval <= 0:
        raise SystemExit("轮询间隔必须大于 0")
    if backup_root == root:
        raise SystemExit("归档目录不能与监控目录相同")

    backup_root.mkdir(parents=True, exist_ok=True)
    if not args.once:
        log(f"开始监控 {root}")
        log(f"旧备份归档到 {backup_root}；按 Ctrl+C 停止")
    try:
        while True:
            archive_older_backups(root, backup_root)
            if args.once:
                break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        log("监控已停止")


if __name__ == "__main__":
    main()
