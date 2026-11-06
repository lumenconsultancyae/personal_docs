from pages.portfolio_page import PortfolioPage


def before_all(context) -> None:
    context.page = PortfolioPage()


def after_all(context) -> None:
    if hasattr(context, "page") and context.page:
        context.page.quit()
