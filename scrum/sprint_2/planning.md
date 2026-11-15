
# Sprint 2 Planning

**Date:** November 4, 2026

**Planning contributors:** Faye, Yasir, Artemis, and Nikki

**Status:** Draft plan based on estimates and assignments shared by the team

## Goal Statement

Continue developing the core CampusEats functionality by integrating and testing US2 (Post Listing) and US3 (Browse Listings). The team will also prepare to begin US5 (Manage Listings). Prioritize making sure existing features work together, resolving issues discovered during testing, and coordinating development through Microsoft Teams and the Kanban board.

## Product Backlog Estimates

The following estimates were carried forward from Sprint 1. Estimates have not yet been finalized together.

| User Story | Description | Faye | Yasir | Jess | Artemis | Conservative Planning Estimate |
|---|---|---:|---:|---:|---:|---:|
| US1 | Register/login | 5 | 3 | 3 | 3 | 5 |
| US2 | Post listing | 4 | 4 | 3 | 3 | 4 |
| US3 | Browse listings | 3 | 3 | 3 | 3 | 3 |
| US4 | Reserve portions | 5 | 5 | 3 | 3 | 5 |
| US5 | Manage listings | 4 | 4 | 2 | 2 | 4 |
| US6 | My reservations | 3 | 3 | 2 | 2 | 3 |
| US7 | Confirm pickup | 4 | 3 | 3 | 3 | 4 |
| US8 | Filter listings | 3 | 2 | 2 | 2 | 3 |
| US9 | Impact dashboard | 4 | 3 | 1 | 1 | 4 |
| US10 | Rate pickup | 2 | 2 | 1 | 1 | 2 |

**Estimation approach:** The conservative estimates from Sprint 1 were retained because no updated team-agreed estimates were documented. These values remain provisional.

## Proposed Sprint 2 Backlog

| User Story | Work | Estimate | Assignment | Priority |
|---|---|---:|---|---|
| US2 | Post listing and integration | 4 points | Artemis | Planned |
| US3 | Browse listings | 3 points | Nikki | Planned |
| US5 | Manage listings | 4 points | Artemis, if development had not started by Friday | Next priority |

**Planned scope:** Continue integrating and testing US2 and US3, while preparing to begin US5.

**Additional work:** Artemis planned to take on US5 (Manage Listings) if development had not started by Friday. Faye offered to help create an initial skeleton if needed.

## Proposed Assignment and Dependency Notes

- **Nikki:** Continue work on US3 and coordinate integration with the existing US2 implementation.
- **Artemis:** Coordinate US2 and US3 integration, review the listings page against acceptance criteria, address testing issues, and potentially begin US5.
- **Yasir:** Review the HTML in the US3 listings pages.
- **Faye:** Coordinate integration and offer assistance with an initial US5 skeleton if needed.
- **Jess:** Was informed that US4 (Reserve Portions) would soon be available for him to work on.
- US3 relies on the existing US2 listing functionality.
- Team members should pull the latest `dev` branch before working on existing features.
- Sprint 2 tasks should be tracked on the Kanban board and linked to pull requests using `closes #issue-number`.
- The plan should be updated if the team agrees on different estimates, assignments, or scope.

## Definition of Done

A story is considered done when:

- Its acceptance criteria are met.
- Relevant tests pass, including appropriate failure cases.
- The changes are committed on a task branch and submitted through a pull request.
- A teammate other than the author reviews the pull request.
- The application continues to use PostgreSQL and the required Docker Compose setup.
- The completed work is merged into the appropriate development branch according to the project workflow.

## Open Decisions

- Confirm the final story-point estimates as a team.
- Confirm the final assignments and timing for US5.
- Verify that US2 and US3 work together correctly before merging.
- Confirm remaining task assignments and sprint capacity.
- Review the plan as implementation progresses and adjust scope when necessary.
