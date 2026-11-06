from behave import given, then, when

NAV_TESTIDS = {
    "Overview": "nav-link-overview",
    "Journey": "nav-link-journey",
    "Projects": "nav-link-projects",
    "Testimonials": "nav-link-testimonials",
    "Personal": "nav-link-personal",
    "Contact": "nav-link-contact",
}

DRAWER_NAV_TESTIDS = {
    "Executive Overview": "drawer-nav-link-overview",
    "Career & Education": "drawer-nav-link-journey",
    "Projects Explorer": "drawer-nav-link-projects",
    "Testimonials & Skills": "drawer-nav-link-testimonials",
    "Personal & Gallery": "drawer-nav-link-personal",
    "Contact & Inquiries": "drawer-nav-link-contact",
}


@given('I open the portfolio application on the "{viewport}" viewport')
def step_open_home(context, viewport: str) -> None:
    context.page.reset_storage_and_open("/", viewport=viewport)


@given('I open the portfolio application at "{path}" on the "{viewport}" viewport')
def step_open_path(context, path: str, viewport: str) -> None:
    context.page.reset_storage_and_open(path, viewport=viewport)


@when('I navigate to the "{route_label}" route via the primary navigation bar')
def step_nav_primary(context, route_label: str) -> None:
    context.page.click_testid(NAV_TESTIDS[route_label])
    context.page.wait_for_route_ready()


@when('I filter projects by category "{category}" and search query "{query}"')
def step_filter_projects(context, category: str, query: str) -> None:
    context.page.select_by_testid("projects-category-select", category)
    context.page.fill_testid("projects-search-input", query)
    context.page.wait_for_url_contains(f"q={query}")


@then('the URL search parameters should include "{param1}" and "{param2}"')
def step_assert_two_url_params(context, param1: str, param2: str) -> None:
    url = context.page.current_url()
    assert param1 in url, f"Expected {param1} in {url}"
    assert param2 in url, f"Expected {param2} in {url}"


@then('the URL search parameters should include "{param}"')
def step_assert_one_url_param(context, param: str) -> None:
    context.page.wait_for_url_contains(param)
    url = context.page.current_url()
    assert param in url, f"Expected {param} in {url}"


@then('the projects table should display "{project_name}"')
@then('the projects table should still display "{project_name}"')
def step_assert_project_in_table(context, project_name: str) -> None:
    text = context.page.get_table_text("projects-table-container")
    assert project_name in text, f"Expected '{project_name}' in table, got: {text[:300]}"


@when("I reload the current browser page")
def step_reload_page(context) -> None:
    context.page.reload()


@when('I request to delete the project "{project_id}"')
def step_request_delete_project(context, project_id: str) -> None:
    context.page.click_testid(f"delete-project-{project_id}")


@then('the accessible confirmation dialog should be visible with summary "{summary_text}"')
def step_assert_confirm_dialog(context, summary_text: str) -> None:
    summary = context.page.wait_for_testid("confirm-dialog-summary")
    assert summary_text in summary, f"Expected {summary_text} in {summary}"


@when("I cancel the confirmation dialog")
def step_cancel_confirm_dialog(context) -> None:
    context.page.click_testid("confirm-dialog-cancel")


@then("the confirmation dialog should be closed")
def step_assert_dialog_closed(context) -> None:
    context.page.wait_for_testid_gone("confirm-dialog")


@when("I confirm the deletion in the confirmation dialog")
def step_confirm_delete(context) -> None:
    context.page.click_testid("confirm-dialog-confirm")


@then("a toast notification should appear with an Undo action")
def step_assert_undo_toast(context) -> None:
    text = context.page.wait_for_testid("toast-undo-button")
    assert "Undo" in text


@when("I click the Undo button in the toast notification")
def step_click_undo_toast(context) -> None:
    context.page.click_testid("toast-undo-button")


@when("I expand the progressive disclosure New Project form")
def step_open_project_form(context) -> None:
    context.page.click_testid("toggle-project-form")
    context.page.wait_for_testid("project-form-panel")


@when("I submit the project form with empty fields")
def step_submit_empty_project_form(context) -> None:
    context.page.click_testid("project-submit-button")


@then("inline validation error alerts should be displayed on the project form")
def step_assert_project_validation_errors(context) -> None:
    err_name = context.page.wait_for_testid("project-error-name")
    err_url = context.page.wait_for_testid("project-error-url")
    assert len(err_name) > 0
    assert len(err_url) > 0


@when(
    'I fill in a valid project named "{name}" with URL "{url}" and tags "{tags}" and description "{desc}"'
)
def step_fill_valid_project(
    context, name: str, url: str, tags: str, desc: str
) -> None:
    context.page.fill_testid("project-input-name", name)
    context.page.fill_testid("project-input-url", url)
    context.page.fill_testid("project-input-tags", tags)
    context.page.fill_testid("project-input-description", desc)


@then("the project name validation error should be cleared immediately")
def step_assert_name_error_cleared(context) -> None:
    context.page.wait_for_testid_gone("project-error-name")


@when("I submit the valid project form")
def step_submit_valid_project(context) -> None:
    context.page.click_testid("project-submit-button")


@then('a toast notification should confirm "{expected_title}"')
def step_assert_toast_title(context, expected_title: str) -> None:
    text = context.page.wait_for_testid("toast-item-success")
    assert expected_title in text, f"Expected '{expected_title}' in toast: {text}"


@then('the pagination status should report "{expected_prefix}"')
def step_assert_pagination_status(context, expected_prefix: str) -> None:
    status = context.page.wait_for_testid("pagination-status")
    assert expected_prefix in status, f"Expected '{expected_prefix}' in '{status}'"


@then("the projects data table should be rendered inside a bounded scroll container with sticky headers")
def step_assert_bounded_table(context) -> None:
    assert context.page.has_bounded_scroll_container("projects-table-container")


@when("I navigate to page 2 of the projects table")
def step_goto_page_2(context) -> None:
    context.page.click_testid("pagination-page-2")


@then("the page should have zero horizontal overflow")
def step_assert_no_horizontal_overflow(context) -> None:
    delta = context.page.get_horizontal_overflow_delta()
    assert delta <= 0, f"Detected horizontal overflow of {delta}px"


@when('I resize the viewport to "{viewport}"')
def step_resize_viewport(context, viewport: str) -> None:
    context.page.set_viewport(viewport)


@when("I open the responsive mobile navigation drawer")
def step_open_mobile_drawer(context) -> None:
    context.page.click_testid("mobile-menu-toggle")


@then("the mobile navigation drawer should be visible")
def step_assert_mobile_drawer_visible(context) -> None:
    context.page.wait_for_testid("mobile-navigation-drawer")


@when('I select the "{label}" link inside the mobile navigation drawer')
def step_click_drawer_link(context, label: str) -> None:
    context.page.click_testid(DRAWER_NAV_TESTIDS[label])
    context.page.wait_for_route_ready()


@then("the mobile navigation drawer should automatically close")
def step_assert_drawer_closed(context) -> None:
    context.page.wait_for_testid_gone("mobile-navigation-drawer")


@then('the current route pathname should be "{expected_path}"')
def step_assert_pathname(context, expected_path: str) -> None:
    context.page.wait_for_url_contains(expected_path)
    assert context.page.current_url().endswith(expected_path)


@then("the browser console should have zero severe errors")
def step_assert_no_severe_console_errors(context) -> None:
    errors = context.page.get_severe_console_errors()
    assert len(errors) == 0, f"Unexpected SEVERE browser console errors: {errors}"
