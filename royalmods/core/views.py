from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from mods.models import Mod, Game, Category
from .models import SiteConfiguration, PageTemplate


class HomePage(ListView):
    """Homepage showing recent approved mods"""
    model = Mod
    template_name = 'core/home.html'
    context_object_name = 'recent_mods'
    
    def get_queryset(self):
        config = SiteConfiguration.getInstance()
        return Mod.objects.filter(status='approved').select_related('game', 'main_author')[:config.featured_mods_count]
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['site_config'] = SiteConfiguration.getInstance()
        return context


class FeaturedView(ListView):
    """Featured mods page"""
    model = Mod
    template_name = 'core/featured.html'
    context_object_name = 'featured_mods'
    paginate_by = 12
    
    def get_queryset(self):
        return Mod.objects.filter(status='approved').select_related('game', 'main_author').order_by('-views_count')


class SearchView(ListView):
    """Search functionality for mods"""
    model = Mod
    template_name = 'core/search.html'
    context_object_name = 'search_results'
    paginate_by = 12
    
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        game_filter = self.request.GET.get('game', '')
        category_filter = self.request.GET.get('category', '')
        
        queryset = Mod.objects.filter(status='approved').select_related('game', 'main_author')
        
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(main_author__username__icontains=query)
            )
        
        if game_filter:
            queryset = queryset.filter(game__slug=game_filter)
            
        if category_filter:
            queryset = queryset.filter(categories__slug=category_filter)
            
        return queryset.distinct()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['games'] = Game.objects.all()
        context['categories'] = Category.objects.all()
        context['selected_game'] = self.request.GET.get('game', '')
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class PageDetailView(DetailView):
    """Display custom pages created from templates"""
    model = PageTemplate
    template_name = 'core/page_detail.html'
    context_object_name = 'page'
    
    def get_queryset(self):
        return PageTemplate.objects.filter(is_active=True)