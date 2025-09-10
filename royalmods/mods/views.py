from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from .models import Mod, ModImage, Game, Category
from .forms import ModUploadForm


class ModListView(ListView):
    """List all approved mods"""
    model = Mod
    template_name = 'mods/list.html'
    context_object_name = 'mods'
    paginate_by = 12
    
    def get_queryset(self):
        return Mod.objects.filter(status='approved').select_related('game', 'main_author').prefetch_related('categories')


class ModDetailView(DetailView):
    """Individual mod page with all details"""
    model = Mod
    template_name = 'mods/detail.html'
    context_object_name = 'mod'
    
    def get_queryset(self):
        return Mod.objects.filter(status='approved').select_related('game', 'main_author').prefetch_related('categories', 'other_authors', 'images', 'required_mods')
    
    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj


class GameModsView(ListView):
    """Mods filtered by game"""
    model = Mod
    template_name = 'mods/by_game.html'
    context_object_name = 'mods'
    paginate_by = 12
    
    def get_queryset(self):
        gameSlug = self.kwargs['game_slug']
        return Mod.objects.filter(status='approved', game__slug=gameSlug).select_related('game', 'main_author').prefetch_related('categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['game'] = get_object_or_404(Game, slug=self.kwargs['game_slug'])
        return context


class CategoryModsView(ListView):
    """Mods filtered by category"""
    model = Mod
    template_name = 'mods/by_category.html'
    context_object_name = 'mods'
    paginate_by = 12
    
    def get_queryset(self):
        categorySlug = self.kwargs['category_slug']
        return Mod.objects.filter(status='approved', categories__slug=categorySlug).select_related('game', 'main_author').prefetch_related('categories')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, slug=self.kwargs['category_slug'])
        return context


class ModUploadView(LoginRequiredMixin, CreateView):
    """Upload new mod form"""
    model = Mod
    form_class = ModUploadForm
    template_name = 'mods/upload.html'
    success_url = reverse_lazy('accounts:creator_studio')
    
    def form_valid(self, form):
        form.instance.main_author = self.request.user
        response = super().form_valid(form)
        
        # Handle multiple image uploads
        images = self.request.FILES.getlist('images')
        for i, image_file in enumerate(images[:6]):
            ModImage.objects.create(
                mod=form.instance,
                image=image_file,
                order=i
            )
        
        messages.success(self.request, 'Mod uploaded successfully! It will be reviewed by admins before going public.')
        return response


class ModDownloadView(View):
    """Handle mod download and increment counter"""
    def get(self, request, slug):
        mod = get_object_or_404(Mod, slug=slug, status='approved')
        mod.increment_downloads()
        return redirect(mod.download_link)