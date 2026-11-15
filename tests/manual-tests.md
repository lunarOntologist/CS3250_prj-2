| User story | Acceptance criterion | Tester | Date | Result | Notes |
| --- | --- | --- | --- | --- | --- |
| US1 | 2: duplicate email rejected | Name | 99/99/26 | passed |  |
| US5 | Deletion of a listing succeeded when there was >1 reservation on the listing | Artemis | 11/6/2026 | Failed | ... |
| US5 | Deletion of a listing succeeded when there was >1 reservation on the listing | Artemis | 11/6/2026 | Passed | I had to make it loop through reservations |
| US8 | 1: Given I am on the listings page, when I select one or more dietary tags, then only listings that have all selected tags are shown. | Faye | 11/14/2026 | Passed | Tested Vegetarian, Vegan, Halal + Gluten-free, and Vegetarian + Vegan. The empty-state message appeared when no listings matched. |
| US8 | 2: When I select a campus location, then only listings at that location are shown; filters can be combined with dietary tags. | Faye | 11/14/2026 | Passed | Tested pickup location filtering using Tivoli Cafe. Combining a location filter with dietary tags has not yet been tested. |
| US8 | 3: When I click "Clear filters", then all available listings are shown again. | Faye | 11/14/2026 | Passed | Clear Filters restored all available listings. |
| US1 | made new student acct, sent to login | Yasir | 11/14/26 | Passed | |
| US1 | same email twice | Yasir | 11/14/26 | Passed | says already registered |
| US1 | left name blank | Yasir | 11/14/26 | Passed | |
| US1 | pw stored hashed | Yasir | 11/14/26 | Passed | checked db, not plain text |
| US1 | login right pw / wrong pw | Yasir | 11/14/26 | Passed | wrong pw shows error |
| US2 | vendor posts listing w/ tags | Yasir | 11/14/26 | Passed | |
| US2 | end before start | Yasir | 11/14/26 | Passed | not saved, error shown |
| US2 | end in the past | Yasir | 11/14/26 | Passed | |
| US2 | 101 portions | Yasir | 11/14/26 | Passed | rejected |
| US2 | student opens new listing page | Yasir | 11/14/26 | Passed | blocked |
| US3 | listings show vendor, location, tags, portions, window | Yasir | 11/14/26 | Passed | |
| US3 | sorted by end time | Yasir | 11/14/26 | Passed | soonest first |
| US3 | no listings left | Yasir | 11/14/26 | Passed | shows message |
| US4 | reserved 2 portions | Yasir | 11/14/26 | Passed | got 6 char code, portions went down |
| US4 | tried 2 portions when 1 left | Yasir | 11/14/26 | Passed | error, nothing reserved |
| US4 | reserve same listing again | Yasir | 11/14/26 | Passed | says already have one |
| US4 | 2 students last portion same time | Yasir | 11/14/26 | Not tested | cant do by hand, code locks the row |
| US5 | my listings shows status + reserved/left | Yasir | 11/14/26 | Passed | |
| US5 | edited listing w/ no reservations | Yasir | 11/14/26 | Passed | |
| US5 | lower portions below reserved | Yasir | 11/14/26 | Passed | not allowed |
| US5 | cancelled listing | Yasir | 11/14/26 | Passed | gone for students, reservations cancelled |
| US5 | see who reserved | Yasir | 11/14/26 | Passed | |
| US6 | my reservations shows all fields | Yasir | 11/14/26 | Passed | |
| US6 | cancelled pizza reservation | Yasir | 11/14/26 | Passed | portions went back up |
| US6 | cancelled one has no cancel button | Yasir | 11/14/26 | Passed | |
| US7 | entered valid code | Yasir | 11/14/26 | Passed | picked up, shows student + portions |
| US7 | fake code | Yasir | 11/14/26 | Passed | no reservation msg |
| US7 | used code twice | Yasir | 11/14/26 | Passed | already used |
| US7 | code from cancelled reservation | Yasir | 11/14/26 | Passed | |
| US7 | window ended, still active | Yasir | 11/14/26 | Passed | shows no-show |
| US8 | location + tag together | Yasir | 11/14/26 | Passed | tivoli + halal only showed rice bowls |
| US9 | dashboard for today, 3 listings | Yasir | 11/15/26 | Passed | posted, portions, picked up, no-shows all right |
| US9 | no-show rate | Yasir | 11/15/26 | Passed | 1 of 3 portions = 33.3% |
| US9 | range w/ no data | Yasir | 11/15/26 | Passed | all 0, no error |
| US9 | student opens dashboard | Yasir | 11/15/26 | Passed | blocked |
| US10 | rated pickup 4 stars w/ comment | Yasir | 11/14/26 | Passed | |
| US10 | rate before pickup | Yasir | 11/14/26 | Passed | no form, blocked |
| US10 | 9 stars / 301 char comment | Yasir | 11/14/26 | Passed | rejected |
| US10 | rate same one again | Yasir | 11/14/26 | Passed | form gone after first |
| US10 | vendor sees avg + comments | Yasir | 11/14/26 | Passed | |