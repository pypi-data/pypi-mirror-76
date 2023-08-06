@blueprint_main.route("/<path:page_url>")
@blueprint_main.route("/<path:page_url>/page/<int:page_number>")
def render_page(page_url: str, page_number: Optional[int] = 1) -> str:

    page: Optional["PageType"] = current_app.site.get_page(page_url=page_url)

    if page is None:
        abort(404)

    """
    TODO: Add pagination.

    paginator = Paginator(page.contents, per_page=10)

    if page_number > paginator.page_count:
        abort(404)

    contents = paginator.page(page_number)
    """

    return render_template("page.html", page=page)


class PaginationMixin:

    """
    # https://github.com/pallets/flask-sqlalchemy/blob/a91b33852efec04aacf2db48213dc83bd0415632/src/flask_sqlalchemy/__init__.py#L308
    # https://github.com/pallets/flask-sqlalchemy/blob/a91b33852efec04aacf2db48213dc83bd0415632/src/flask_sqlalchemy/__init__.py#L416

    posts = Posts.query.order_by(Posts.time.desc()).paginate(
        page, per_page, error_out=False
    )
    """

    ITEMS_PER_PAGE = 6

    _contents = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]

    def paginated(self, page_number):

        import math

        item_count = len(self._contents)
        page_count = math.ceil(item_count / self.ITEMS_PER_PAGE)

        if page_number <= 0:
            print("Page too low")
            return

        if page_number > page_count:
            print("Page too high")
            return

        start = self.ITEMS_PER_PAGE * (page_number - 1)
        end = start + self.ITEMS_PER_PAGE

        return self._contents[start:end]


pm = PaginationMixin()
print(pm.paginated(page_number=0))
print(pm.paginated(page_number=1))
print(pm.paginated(page_number=2))
print(pm.paginated(page_number=3))
print(pm.paginated(page_number=4))
print(pm.paginated(page_number=5))
