from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shows.models import Show, ShowTime
from bookings.models import Booking
from django.db.models import Count, Sum

class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_staff

class AdminDashboardView(LoginRequiredMixin, StaffRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get statistics for the dashboard
        context['total_shows'] = Show.objects.count()
        context['active_shows'] = Show.objects.filter(is_active=True).count()
        context['total_bookings'] = Booking.objects.count()
        context['total_revenue'] = Booking.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        # Get recent bookings
        context['recent_bookings'] = Booking.objects.all().order_by('-booking_date')[:5]
        
        # Get popular shows (by number of bookings)
        popular_shows = Show.objects.annotate(
            booking_count=Count('showtimes__bookings')
        ).order_by('-booking_count')[:5]
        context['popular_shows'] = popular_shows
        
        return context

class ShowListAdminView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Show
    template_name = 'admin_panel/show_list.html'
    context_object_name = 'shows'
    ordering = ['-created_at']

class ShowCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    template_name = 'admin_panel/show_form.html'
    
    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        duration = request.POST.get('duration')
        release_date = request.POST.get('release_date')
        is_active = request.POST.get('is_active') == 'on'
        
        # Manual validation
        if not title or not description or not category or not duration or not release_date:
            messages.error(request, 'All fields are required')
            return render(request, self.template_name, {
                'title': title,
                'description': description,
                'category': category,
                'duration': duration,
                'release_date': release_date,
                'is_active': is_active
            })
        
        # Create show
        show = Show.objects.create(
            title=title,
            description=description,
            category=category,
            duration=duration,
            release_date=release_date,
            is_active=is_active
        )
        
        # Handle image upload
        if 'image' in request.FILES:
            show.image = request.FILES['image']
            show.save()
        
        messages.success(request, 'Show created successfully')
        return redirect('admin_panel:show_list')

class ShowUpdateView(LoginRequiredMixin, StaffRequiredMixin, View):
    template_name = 'admin_panel/show_form.html'
    
    def get(self, request, pk):
        show = Show.objects.get(pk=pk)
        return render(request, self.template_name, {'show': show})
    
    def post(self, request, pk):
        show = Show.objects.get(pk=pk)
        
        show.title = request.POST.get('title')
        show.description = request.POST.get('description')
        show.category = request.POST.get('category')
        show.duration = request.POST.get('duration')
        show.release_date = request.POST.get('release_date')
        show.is_active = request.POST.get('is_active') == 'on'
        
        # Manual validation
        if not show.title or not show.description or not show.category or not show.duration or not show.release_date:
            messages.error(request, 'All fields are required')
            return render(request, self.template_name, {'show': show})
        
        # Handle image upload
        if 'image' in request.FILES:
            show.image = request.FILES['image']
        
        show.save()
        messages.success(request, 'Show updated successfully')
        return redirect('admin_panel:show_list')

class ShowDeleteView(LoginRequiredMixin, StaffRequiredMixin, View):
    def post(self, request, pk):
        show = Show.objects.get(pk=pk)
        show.delete()
        messages.success(request, 'Show deleted successfully')
        return redirect('admin_panel:show_list')

class ShowtimeCreateView(LoginRequiredMixin, StaffRequiredMixin, View):
    template_name = 'admin_panel/showtime_form.html'
    
    def get(self, request, show_id):
        show = Show.objects.get(pk=show_id)
        return render(request, self.template_name, {'show': show})
    
    def post(self, request, show_id):
        show = Show.objects.get(pk=show_id)
        
        date = request.POST.get('date')
        time = request.POST.get('time')
        price = request.POST.get('price')
        
        # Manual validation
        if not date or not time or not price:
            messages.error(request, 'All fields are required')
            return render(request, self.template_name, {
                'show': show,
                'date': date,
                'time': time,
                'price': price
            })
        
        # Create showtime
        ShowTime.objects.create(
            show=show,
            date=date,
            time=time,
            price=price
        )
        
        messages.success(request, 'Showtime added successfully')
        return redirect('admin_panel:show_detail', pk=show_id)

class ShowDetailAdminView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Show
    template_name = 'admin_panel/show_detail.html'
    context_object_name = 'show'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['showtimes'] = self.object.showtimes.all().order_by('date', 'time')
        return context

class BookingListAdminView(LoginRequiredMixin, StaffRequiredMixin, ListView):
    model = Booking
    template_name = 'admin_panel/booking_list.html'
    context_object_name = 'bookings'
    ordering = ['-booking_date']

class BookingDetailAdminView(LoginRequiredMixin, StaffRequiredMixin, DetailView):
    model = Booking
    template_name = 'admin_panel/booking_detail.html'
    context_object_name = 'booking'