@e2e @ux
Feature: Executive Portfolio UX, Declarative Routing, Inline Validation & Responsive Accessibility
  As a visitor, recruiter, or engineering peer
  I want cohesive navigation, bookmarkable URL filters, accessible modals/toasts with Undo, inline form validation, and responsive layouts
  So that I can explore Wilson Guevara's portfolio seamlessly across Desktop, Tablet, and Mobile viewports

  Scenario: Declarative route navigation, deep-linking, and URL state persistence across page reloads
    Given I open the portfolio application on the "desktop" viewport
    When I navigate to the "Projects" route via the primary navigation bar
    And I filter projects by category "Architecture" and search query "DDD"
    Then the URL search parameters should include "category=Architecture" and "q=DDD"
    And the projects table should display "DDDCompiler"
    When I reload the current browser page
    Then the URL search parameters should include "category=Architecture" and "q=DDD"
    And the projects table should still display "DDDCompiler"

  Scenario: Accessible confirmation modal cancel and confirm flows with Undo toast notification
    Given I open the portfolio application at "/projects" on the "desktop" viewport
    When I request to delete the project "proj-ddd-compiler"
    Then the accessible confirmation dialog should be visible with summary "DDDCompiler"
    When I cancel the confirmation dialog
    Then the confirmation dialog should be closed
    And the projects table should display "DDDCompiler"
    When I request to delete the project "proj-ddd-compiler"
    And I confirm the deletion in the confirmation dialog
    Then a toast notification should appear with an Undo action
    When I click the Undo button in the toast notification
    Then the projects table should display "DDDCompiler"

  Scenario: Schema-first inline form validation, real-time error clearing, and project creation
    Given I open the portfolio application at "/projects" on the "desktop" viewport
    When I expand the progressive disclosure New Project form
    And I submit the project form with empty fields
    Then inline validation error alerts should be displayed on the project form
    When I fill in a valid project named "Edge Vector Gateway" with URL "https://github.com/wilsonr990/edge-vector" and tags "Rust, Milvus" and description "Low-latency vector similarity gateway at the edge."
    Then the project name validation error should be cleared immediately
    When I submit the valid project form
    Then a toast notification should confirm "Project created"
    And the projects table should display "Edge Vector Gateway"

  Scenario: Component-level table pagination and bounded scroll container
    Given I open the portfolio application at "/projects" on the "desktop" viewport
    Then the pagination status should report "Showing 1–10 of"
    And the projects data table should be rendered inside a bounded scroll container with sticky headers
    When I navigate to page 2 of the projects table
    Then the URL search parameters should include "page=2"
    And the pagination status should report "Showing 11–"

  Scenario: Responsive navigation drawer and zero horizontal overflow across Desktop, Tablet, and Mobile viewports
    Given I open the portfolio application on the "desktop" viewport
    Then the page should have zero horizontal overflow
    When I resize the viewport to "tablet"
    Then the page should have zero horizontal overflow
    When I open the responsive mobile navigation drawer
    Then the mobile navigation drawer should be visible
    When I select the "Career & Education" link inside the mobile navigation drawer
    Then the mobile navigation drawer should automatically close
    And the current route pathname should be "/journey"
    When I resize the viewport to "mobile"
    Then the page should have zero horizontal overflow
    And the browser console should have zero severe errors
