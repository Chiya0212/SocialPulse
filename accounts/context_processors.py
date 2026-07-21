def theme_processor(request):
    return {'current_theme': getattr(request, 'theme', 'dark')}
