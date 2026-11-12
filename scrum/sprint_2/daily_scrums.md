# # # November 2, 2026 — Independent Work

**Format:** Individual work; no team check-in

**Progress and Updates**
- Team members continued working independently on their assigned project tasks.
- No group meeting or formal check-in took place.

**Follow-up**
- Team members would share progress and coordinate outstanding work at the next opportunity.

# # November 3, 2026 — Daily Scrum and Sprint 2 Coordination

**Format:** In-person meeting during class

**Participants:** Faye, Artemis, and Yasir

**Progress and Updates**
- The team discussed the progress of US2 (Post Listing) and US3 (Browse Listings).
- Both stories were reported as completed or nearing completion.


**Planning and Decisions**
- Faye planned to focus on some optional user stories while continuing her documentation responsibilities.
- Faye and Yasir planned to review the HTML code together.
- The team discussed coordinating remaining implementation work as Sprint 2 progressed.
- Artemis reported that she planned to finish the remaining work on US2 (Post Listing) later that evening.

**Follow-up**
- Confirm completion and testing of US2 and US3.
- Continue work on optional features.
- Review HTML implementation with Yasir.
- Continue maintaining Scrum and project documentation.

# #November 4, 2026 — Daily Scrum and Development Coordination

**Format:** Asynchronous discussion in Microsoft Teams

**Participants:** Faye, Yasir Artemis, Nikki

**Progress and Updates**
- Nikki reported that he had completed his version of US3 (Browse Listings) and planned to push it to a separate US3 branch.
- While working on US3, Nikki had difficulty locating the existing US2 implementation in `dev` and independently recreated some of its functionality.
-Artemis clarified that US2 was already in `dev`, including the `new_listing` route, Posting model, and FoodForm.
- Artemis reviewed the situation and identified useful additions in Nikki's implementation that could be incorporated into the existing code.

**Planning and Decisions**
- Faye and Artemis coordinated the integration of the missing US2 functionality into Nikki's US3 branch.
- The team planned to merge the updated branch into `dev`, replacing the overlapping implementation as needed.
- Yasir was asked to review the HTML in the US3 listings pages to ensure all required functionality was included.
- Jess was informed that US4 (Reserve Portions) would soon be available for him to work on.

**Blockers and Follow-up**
- Verify that the US3 implementation includes all required listing functionality.
- Complete integration and testing of the US2 and US3 changes before merging.
- Make sure team members pull the latest `dev` branch before starting work on existing features.
- Coordinate the next steps for US4.

**Additional Progress and Updates**
- Artemis reviewed the US3 listings page against the acceptance criteria, and Nikki tested the implementation.
- Testing revealed an issue preventing listings from being posted through the browser. The date format expected by `forms.py` did not match the format sent by the date picker.
- An additional issue was identified in `validate_pickup_end`, which attempted to compare a string with a datetime object.
- Artemis pushed updates to `forms.py` and `routes.py` to address the date-format and validation issues.

**Planning and Decisions**
- The team clarified that daily Scrum check-ins would primarily take place asynchronously through Microsoft Teams, with additional coordination during class when available.
- Faye explained that check-ins should cover completed work, remaining tasks, and overall sprint progress.
- Yasir created the Kanban board and backfilled the Sprint 1 issues. Team members were asked to create and assign their own Sprint 2 issues, apply appropriate labels, update the board as work progresses, and reference issue numbers in pull requests using `closes #_`.
- Artemis planned to take on US4 (Reserve Portions) if work had not started by Friday. Faye offered to help by developing an initial skeleton during office hours if needed.

**Follow-up**
- Retest the listing submission functionality after Artemis's changes.
- Continue monitoring progress on US4.
- Make sure Sprint 2 tasks are tracked on the Kanban board and linked to pull requests.

# # November 5, 2026 — Daily Scrum and Sprint 2 Coordination

**Format:** Asynchronous discussion in Microsoft Teams

**Participants:** Faye, Artemis, Jess, and Nikki

**Progress and Updates**
- Nikki reported that he was feeling unwell and would not attend class but offered to help with any unassigned Sprint 2 tasks.
- Jess confirmed that he was actively working on US4 (Reserve Portions) and planned to push his branch later in the day.
- Faye acknowledged Jess's update and confirmed that he was expected to take responsibility for US4.

**Planning and Decisions**
- Nikki asked whether he should begin working on US5 (Manage Listings).
- Artemis clarified that Faye and Artemis were already working on US5.
- Artemis suggested that Nikki could begin working on US6 (My Reservations).

**Follow-up**
- Jess to push his US4 branch and coordinate integration.
- Faye and Artemis to continue working on US5.
- Nikki to begin US6 if available.
- Continue updating the Kanban board and checking in through Microsoft Teams.
# # November 5, 2026 — Daily Scrum and Sprint 3 Development Coordination

**Format:** Asynchronous discussion in Microsoft Teams

**Participants:** Faye, Artemis, Jess, and Nikki

**Progress and Updates**
- Faye began working on the initial skeleton for US5 (Manage Listings).
- Faye created the vendor listings route and initial page structure.
- A link to the listings page was added to the vendor homepage.
- The initial implementation provided a starting point for displaying a vendor's listings and related information.

**Planning and Decisions**
- Faye and Artemis continued coordinating the development of US5.
- The team planned to continue building on the initial implementation and verify that it met the acceptance criteria.

**Blockers and Follow-up**
- The initial US5 implementation had not yet been fully tested.
- Docker setup was still needed to run and test the application locally.
- Continue development and review of US5.
- Coordinate integration of the completed changes into dev.

# # November 6, 2026 — Daily Scrum and Sprint 3 Development Updates

**Format:** Asynchronous discussion in Microsoft Teams

**Participants:** Faye and Artemis

**Progress and Updates**
- Artemis completed US5 (Manage Listings).
- The completed US5 implementation was merged into the dev branch.
- The README test documentation for US5 was filled out.

**Planning and Decisions**
- The team moved forward with organizing the remaining required user stories.
- Further coordination was needed to determine who would take responsibility for US6 and US7.

**Follow-up**
- Continue coordinating the remaining required user stories.
- Confirm assignments for US6 and US7.
- Continue tracking implementation and testing progress.