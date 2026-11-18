"""Contracts for owning-stack refusal and zero-redirect HTTP route handling."""

from collections import deque
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from proxmox_sdk.proxmox_codegen.crawler import (
    _close_browser,
    _drain_web_socket_refusals,
    _fulfill_without_redirect,
    _guard_request,
    _guard_web_socket,
)


def test_cross_origin_http_request_is_refused_before_any_fetch_or_fulfillment() -> None:
    route = Mock()
    request = SimpleNamespace(redirected_from=None, url="https://other.example/private")
    errors = []
    _guard_request(route, request, ("https", "source.example", 443), errors)
    route.abort.assert_called_once_with("blockedbyclient")
    route.fetch.assert_not_called()
    route.fulfill.assert_not_called()
    assert errors == []


def test_web_socket_dispatch_callback_never_calls_a_synchronous_route_action() -> None:
    pending = deque()
    route = Mock(url="wss://same-origin.example/socket")
    _guard_web_socket(route, pending)
    route.close.assert_not_called()
    route.connect_to_server.assert_not_called()
    assert list(pending) == [route]
    _drain_web_socket_refusals(pending)
    route.close.assert_called_once_with(code=1008, reason="WebSockets are refused")
    assert not pending


def test_failed_close_does_not_leave_other_queued_refusals_undrained() -> None:
    failure = RuntimeError("synthetic route close failure")
    first = Mock()
    first.close.side_effect = failure
    second = Mock()
    pending = deque([first, second])
    with pytest.raises(RuntimeError) as error:
        _drain_web_socket_refusals(pending)
    assert error.value is failure
    second.close.assert_called_once_with(code=1008, reason="WebSockets are refused")
    assert not pending


def test_reentrant_close_is_bounded_and_browser_disposes_late_refusals() -> None:
    pending = deque()
    first, reopened = Mock(), Mock()
    first.close.side_effect = lambda **kwargs: pending.append(reopened)
    pending.append(first)
    _drain_web_socket_refusals(pending)
    first.close.assert_called_once_with(code=1008, reason="WebSockets are refused")
    reopened.close.assert_not_called()
    assert list(pending) == [reopened]
    browser = Mock()
    browser.close.side_effect = lambda: pending.append(Mock())
    _close_browser(browser, pending)
    browser.close.assert_called_once_with()
    assert not pending


def test_browser_cleanup_runs_even_when_refusal_fails_and_retains_no_late_handle() -> None:
    pending = deque()
    route = Mock()
    route.close.side_effect = RuntimeError("synthetic route close failure")
    pending.append(route)
    browser = Mock()
    browser.close.side_effect = lambda: pending.append(Mock())
    with pytest.raises(RuntimeError, match="synthetic route close failure"):
        _close_browser(browser, pending)
    browser.close.assert_called_once_with()
    assert not pending


@pytest.mark.parametrize("status", [301, 302, 303, 307, 308])
def test_redirect_response_is_aborted_without_fulfillment_or_followed_hop(status: int) -> None:
    response = SimpleNamespace(
        status=status,
        headers={"location": "http://169.254.169.254/never-follow"},
        dispose=Mock(),
    )
    route = Mock()
    route.fetch.return_value = response
    errors = []
    _fulfill_without_redirect(route, errors)
    route.fetch.assert_called_once_with(max_redirects=0, max_retries=0, timeout=30000)
    route.abort.assert_called_once_with("blockedbyclient")
    route.fulfill.assert_not_called()
    response.dispose.assert_called_once_with()
    assert errors[0].status == status
    assert errors[0].location_host == "169.254.169.254"


@pytest.mark.parametrize("status", [200, 404])
def test_same_origin_nonredirect_response_is_fulfilled_unchanged(status: int) -> None:
    response = SimpleNamespace(status=status, dispose=Mock())
    route = Mock()
    route.fetch.return_value = response
    errors = []
    _fulfill_without_redirect(route, errors)
    route.fulfill.assert_called_once_with(response=response)
    route.abort.assert_not_called()
    response.dispose.assert_called_once_with()
    assert errors == []


def test_http_route_failure_still_disposes_its_fetched_response() -> None:
    response = SimpleNamespace(status=200, dispose=Mock())
    route = Mock()
    route.fetch.return_value = response
    route.fulfill.side_effect = RuntimeError("synthetic fulfillment failure")
    with pytest.raises(RuntimeError, match="synthetic fulfillment failure"):
        _fulfill_without_redirect(route, [])
    response.dispose.assert_called_once_with()
