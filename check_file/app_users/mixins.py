class TitleMixin:
    """Миксин для title в html странцие"""

    title = None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['title'] = self.title

        return context
