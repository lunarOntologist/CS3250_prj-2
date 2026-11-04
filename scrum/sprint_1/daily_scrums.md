# October 26, 2026 — Sprint 1 Planning and Team Check-in

**Format:** Team planning discussion

**Participants:** Faye, Artemis, Jess, and Yasir

**Progress and Updates**
- The team shared initial story-point estimates for all 10 user stories.
- The team reviewed the user stories and their dependencies.
- Initial task assignments were discussed, including Yasir taking responsibility for US1, US6, and US7.

**Planning and Decisions**
- The team discussed taking a conservative approach to Sprint 1 to avoid overcommitting.
- US1 (Register/Login) was selected as the committed Sprint 1 scope, estimated at 5 story points.
- US2 (Post Listing) was identified as a possible stretch goal after US1 was completed and tested.
- The team identified the need to finalize estimates, assignments, and sprint capacity.

**Follow-up**
- Confirm story-point estimates as a team.
- Finalize task assignments and sprint scope.
- Update the sprint plan as work progresses.

# October 27, 2026 — Daily Scrum

**Format:** Discussion in Microsoft Teams

**Participants:** Faye, Artemis, Jess, Nikki and Yasir

**Progress and Updates**
- Team members checked in on their current progress and reported that they were on track.
- The team discussed outstanding work, including US5 (Manage Listings) and setting up seed accounts for testing.
- Seed account creation was identified as a priority.
- The team discussed the planned scope and organization of the three project sprints.

**Planning and Decisions**
- The team discussed planning all three sprints in advance.
- Sprint 1 was organized around US1, US2, and US3.
- The team discussed placing US4, US5, and potentially US6 in Sprint 2.
- US7 and optional stories were discussed for Sprint 3.
- The team planned to work on finalizing story-point estimates together during class.

**Blockers and Follow-up**
- Seed account setup and ownership of US5 still needed follow-up.
- The team needed to finalize estimates, priorities, and sprint assignments.
- Scrum documentation and planning materials needed to be transferred into the repository.

**Additional Notes**
- The professor confirmed that asynchronous discussions in Microsoft Teams count as formal daily Scrum meetings.

# # October 28, 2026 — Daily Scrum

**Format:** Brief check-in between Faye and Artemis

**Participants:** Faye, Artemis

**Progress and Updates**
- Faye and Artemis checked in on current progress.
- Both confirmed that work was on track.

**Blockers**
- No blockers or concerns were raised during this check-in.

**Follow-up**
- Continue working on assigned tasks and communicate any changes in progress.

# # # October 29, 2026 — Daily Scrum

**Format:** Asynchronous discussion in Microsoft Teams

**Participants:** Faye, Artemis, Nikki, Jess, and Yasir

**Progress and Updates**
- Yasir reported that US1 (Register/Login) was complete and shared his current assignments: US6, US7, and shared HTML/CSS work.
- Artemis confirmed that she was continuing with US2 (Post Listing) and US8 (Filter Listings).
- Nikki was identified as working on US3 (Browse Listings).
- Jess was working on the UML diagrams.
- Faye was coordinating Scrum documentation and README sprint planning.
- The team discussed creating the food posting form for US2 and connecting the required forms to routes.py.
- Faye updated the Sprint 1 planning documentation to incorporate corrections suggested by the professor.

**Planning and Coordination**
- Faye organized the team's current task assignments to help prevent duplicated work.
- The team identified US4 (Reserve Portions) as the biggest gap because it had not yet been confirmed by an owner.
- US4 was identified as a dependency blocking US5, US6, and US7.
- Jess was asked whether he could take US4 if Artemis was no longer available for it.
- US5 (Manage Listings) and the seed accounts (one student, one vendor, and sample listings) also remained unclaimed.
- The team discussed the need for tagged releases, Kanban boards, and Scrum meeting notes in the repository.
- Yasir clarified that the README work was being handled on the `readthatme` branch to avoid duplicate effort.

**Blockers and Follow-up**
- Confirm ownership of US4 and US5.
- Assign responsibility for creating the seed accounts and sample listings.
- Continue US2 development, including the food posting form and related routes.
- Coordinate remaining work around US4 and its dependent stories.
- Help teammates who were having trouble running the application locally.

**Technical Support**
- Yasir shared the Docker commands for cloning the repository, checking out and updating `dev`, and running `docker compose up --build`.
- The team was directed to open the application at `http://localhost:5000` after starting Docker Compose.

# # # October 30, 2026 — Daily Scrum

**Format:** Asynchronous discussion in Microsoft Teams

**Participants:** Faye, Artemis, Jess, and Yasir

**Progress and Updates**
- The team followed up on the status of the HTML food-posting form for US2.
- The form had been started but was not yet finished.
- The person working on the form communicated that they needed a few more hours to complete it.

**Planning and Decisions**
- Jess agreed to take responsibility for US4 (Reserve Portions) during the next sprint.

**Blockers and Follow-up**
- Finish the HTML food-posting form for US2.
- Continue coordinating US4 so it can be addressed in the next sprint.

# # # October 31, 2026 — Development Update and Team Coordination

**Format:** Asynchronous discussion in Microsoft Teams

**Progress and Updates**
- The team coordinated the vendor home page and the new listing functionality for US2 (Post Listing).
- The team agreed to use the `new_listing` route for the Post Food button on the vendor home page.
- Form and model updates were made, including adjustments to required fields, date/time fields, and listing identifiers.
- The `new_listing` route was connected, and the team tested the posting workflow using Docker.
- Testing revealed that listings with an end time in the past could still be saved. The team added and corrected an end-time validation check.
- The related pull requests were merged after the changes were completed and tested.
- The team confirmed that Nikki could move forward with US3 (Browse Listings).

**Planning and Decisions**
- The team confirmed that Sprint 2 would begin Monday, November 2.
- US4 (Reserve Portions) was confirmed as upcoming work for the next sprint.
- Team members offered to help address any bugs discovered in US2.

**Blockers and Follow-up**
- Continue development and testing of US3.
- Address any additional US2 bugs discovered during testing.
- Begin Sprint 2 work on Monday, November 2.

# # # November 2, 2026 — Independent Work

**Format:** Individual work; no team check-in

**Progress and Updates**
- Team members continued working independently on their assigned project tasks.
- No group meeting or formal check-in took place.

**Follow-up**
- Team members would share progress and coordinate outstanding work at the next opportunity.

# # # November 3, 2026 — Daily Scrum and Sprint 2 Coordination

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

# # # November 4, 2026 — Daily Scrum and Development Coordination

**Format:** Asynchronous discussion in Microsoft Teams

**Participants:** Everyone (some team members working independently and others collaborating)

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