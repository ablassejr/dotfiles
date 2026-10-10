# Behavioral acceptance test anti-patterns

Tests establish the required outcome through the real affected components. Test-first execution helps expose a missing behavior, but does not by itself make an assertion meaningful.

| Anti-pattern | Better evidence |
|---|---|
| Asserting a mock exists or an internal method was called | Assert the result visible to the user or caller. |
| Mocking the worker, service, or internal collaborator under test | Exercise it; fake only a true external boundary or nondeterministic input. |
| Checking private tables when a public read interface exists | Retrieve and assert the persisted result through that interface. |
| Repeating the implementation's algorithm to calculate expectations | Use an independent example or established contract. |
| Adding one test per function, seam, or incident mechanism | Reuse or add only scenarios needed for the affected acceptance criteria. |
| Claiming E2E from a stubbed application or a passing unit test | Report the actual boundary and use an integration fallback when E2E cannot run. |
| Declaring acceptance from startup, no exception, or process completion alone | Assert the intended successful output and material in-scope failure or recovery behavior. |

When a true external provider needs a fake, model the documented responses relevant to the scenario, including meaningful failures. Do not fake an internal component simply because it is slow or hard to initialize. If the contract under test is the provider integration itself, an application test with a provider fake leaves that live integration unverified.

When setup or observation is difficult, improve the harness at the public boundary. Do not expose private state or add test-only production methods to satisfy the test. Keep cleanup in the test environment.

Minimal means removing redundant proof, not weakening assertions. A scenario may contain multiple observations when they jointly establish one outcome. Retain distinct scenarios that cover different required outcomes even if their internal execution paths overlap.
