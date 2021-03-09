import logging

from github import Github, PaginatedList
from typing import List

from aws import comprehend

logger = logging.getLogger(__file__)

GITHUB_TOKEN = "your-github-token"
MAX_ISSUES_PROCESSED = 10


def process_user(gh_username: str):
    gh = Github(GITHUB_TOKEN)
    issue_list = gh.search_issues(query="", sort="updated", order="desc", per_page=10, page=1, user=gh_username)
    if issue_list.totalCount == 0:
        logger.info(f"No issues found for user {gh_username}")
        return []

    logger.info(f"Processing user {gh_username}")
    parsed_data = [issue_data.body for issue_data in issue_list[:2] if issue_data and issue_data.body]
    sentiment_info = comprehend.process_text(parsed_data)
    return sentiment_info


def process_repo(gh_repo_name: str):
    gh = Github(GITHUB_TOKEN)
    issue_list = gh.get_repo(gh_repo_name).get_issues(sort="updated", direction="desc")
    logger.info(f"Found {issue_list.totalCount} issues for repo {gh_repo_name}")

    if issue_list.totalCount == 0:
        logger.info(f"No issues found for repo {gh_repo_name}")
        return {}

    parsed_data = _filter_issues(issue_list)
    sentiment_info = comprehend.process_text(parsed_data)
    return sentiment_info


def _filter_issues(issue_list: PaginatedList) -> List[str]:
    cnt = 0
    results = []
    for issue_data in issue_list:
        if not issue_data.pull_request and issue_data.body:
            cnt += 1
            results.append(issue_data.body)
            results.append(issue_data.title)
            comment_list = issue_data.get_comments()
            logger.info(f"Got {comment_list.totalCount} comments for issue #{issue_data.id}")
            for comment in comment_list:
                results.append(comment.body)

        if cnt > MAX_ISSUES_PROCESSED:
            break
    return results
