from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse  # needed for partials

from .forms import UserProfileForm


@login_required
def user_profile(request):
    """View for users to update their profile information"""
    # Handle partial requests
    partial = request.GET.get('partial')
    if partial:
        return _render_partial(request, partial)

    # Handle full page requests
    context = {}

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            if not user.display_name:
                full_name = user.get_full_name().strip()
                if full_name:
                    user.display_name = full_name
            user.save()
            messages.success(request, 'Your profile has been updated successfully.')
            return redirect('users:user_profile')
    else:
        form = UserProfileForm(instance=request.user)

    context['form'] = form
    return render(request, 'users/profile.html', context)


def _render_partial(request, partial_name):
    """Route partial requests to appropriate handlers"""
    partials = {
        'delete-account': 'users/profile.html#delete-account',
    }

    if partial_name not in partials:
        return TemplateResponse(request, 'errors/404.html', status=404)

    context = {}
    return TemplateResponse(request, partials[partial_name], context)


@login_required
def delete_account(request):
    """View to handle user account deletion
    
    Note: By adding the message before calling logout(), the message gets encoded
     into the response data. The framework serializes it properly so it survives 
     the logout and redirect.
    
    """
    if request.method == 'POST':
        user = request.user

        # Add the message to the session before logging out
        messages.success(request, 'Your account has been deleted successfully.')

        # Log out the user before deletion to avoid session issues
        from django.contrib.auth import logout
        logout(request)

        # Now delete the user
        user.delete()

        return redirect('core:home')

    # If GET request, don't allow direct access
    return redirect('users:user_profile')
