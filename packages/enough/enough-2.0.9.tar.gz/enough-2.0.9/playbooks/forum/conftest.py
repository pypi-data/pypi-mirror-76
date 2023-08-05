def pytest_addoption(parser):
    parser.addoption(
        "--enough-hosts",
        action="store",

        default="bind-host,postfix-host,icinga-host,forum-host",
        help="list of hosts"
    )
    parser.addoption(
        "--enough-service",
        action="store",
        default="forum",
        help="service"
    )
