# Dependencies

Status: CURRENT

QUESTION_MODEL -> PAGE_1, PAGE_2, PAGE_3, PAGE_4.
SOURCE_LOCK -> PAGE_2, PAGE_3.
PAGE_1 -> PAGE_2 -> PAGE_3 -> PAGE_4.
FOUR_PAGE_ARCHITECTURE -> EXACT_COPY.
EXACT_COPY + VISUAL_MASTER -> ARTIFACT_SPEC -> PDF_RENDER.
PDF_RENDER -> RENDER_QA -> RELEASE_CANDIDATE.

Any change to the core student coordinates reopens all four pages.
Any source-content change reopens only affected source applications plus descendants.
