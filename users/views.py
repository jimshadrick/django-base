from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse  # needed for partials

from .forms import UserProfileForm


@login_required
def user_profile(request):
    """View for users to update their profile information"""
    context = {}
    # Render modal partial if requested
    if request.GET.get('partial') == 'delete-account':
        # Returns only the HTML inside the partialdef tag
        return TemplateResponse(request, 'users/profile.html#delete-account', context)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)

        if form.is_valid():
            user = form.save(commit=False)

            # Autopopulate display_name if it's empty
            if not user.display_name:
                full_name = user.get_full_name().strip()
                if full_name:
                    user.display_name = full_name

            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:user_profile')
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'users/profile.html', {'form': form})
