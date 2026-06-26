from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup

DEFAULT_TIMEOUT = 10.0
DEFAULT_WORKERS = 4


@dataclass(frozen=True)
class PageResult:
    approach: str
    url: str
    title: str | None
    status: str
    elapsed_seconds: float
    record_id: int | None = None
    error: str | None = None


@dataclass(frozen=True)
class ParserSummary:
    approach: str
    workers: int
    url_count: int
    created: int
    updated: int
    failed: int
    elapsed_seconds: float


def extract_title(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if soup.title is None or soup.title.string is None:
        raise ValueError("HTML document does not contain a non-empty <title> tag")
    title = re.sub(r"\s+", " ", soup.title.string).strip()
    if not title:
        raise ValueError("HTML title is empty")
    return title


def build_parser(description: str) -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS)
    parser.add_argument("--timeout", type=float, default=DEFAULT_TIMEOUT)
    return parser


def summarize_results(
    approach: str,
    workers: int,
    results: Iterable[PageResult],
    elapsed_seconds: float,
) -> ParserSummary:
    result_list = list(results)
    return ParserSummary(
        approach=approach,
        workers=workers,
        url_count=len(result_list),
        created=sum(1 for result in result_list if result.status == "created"),
        updated=sum(1 for result in result_list if result.status == "updated"),
        failed=sum(1 for result in result_list if result.status == "failed"),
        elapsed_seconds=elapsed_seconds,
    )


def print_page_result(result: PageResult) -> None:
    print(
        f"{result.approach}: {result.url} | status={result.status} | "
        f"title={result.title!r} | record_id={result.record_id} | "
        f"elapsed={result.elapsed_seconds:.6f}s"
    )
    if result.error:
        print(f"  error: {result.error}")


def write_parser_summaries(path: Path, summaries: Iterable[ParserSummary]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "approach",
                "workers",
                "url_count",
                "created",
                "updated",
                "failed",
                "elapsed_seconds",
            ],
        )
        writer.writeheader()
        for summary in summaries:
            writer.writerow(summary.__dict__)
