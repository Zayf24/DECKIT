from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DeckForm
from .models import Deck, Flashcard
from django.utils import timezone

def create_deck(request):
    if request.method == 'POST':
        deck_form = DeckForm(request.POST)
        if deck_form.is_valid():
            deck = deck_form.save(commit=False)
            deck.user = request.user

            total = int(request.POST.get('flashcard_total', 0))
            flashcards_added = 0  # Count valid flashcards

            flashcards = []
            for i in range(total):
                title = request.POST.get(f'flashcard_title_{i}', '').strip()
                description = request.POST.get(f'flashcard_description_{i}', '').strip()

                if title and description:
                    flashcards.append(Flashcard(deck=deck, title=title, description=description, order=i))
                    flashcards_added += 1
                elif title or description:  # Partial flashcard
                    messages.error(request, "Each flashcard must have both a title and a description.")
                    return render(request, 'flashcards/deck_create.html', {'deck_form': deck_form})

            if flashcards_added == 0:
                messages.error(request, "Deck can't be empty! Add at least one flashcard.")
                return render(request, 'flashcards/deck_create.html', {'deck_form': deck_form})

            deck.save()  # Save the deck only if at least one valid flashcard exists
            Flashcard.objects.bulk_create(flashcards)  # Bulk insert flashcards

            messages.success(request, 'Flashcard deck created successfully!')
            return redirect('deck_list')

        messages.error(request, 'Please correct the errors below.')

    else:
        deck_form = DeckForm()

    return render(request, 'flashcards/deck_create.html', {'deck_form': deck_form})


@login_required
def deck_list(request):
    decks = Deck.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'flashcards/deck_list.html', {'decks': decks})

@login_required
def deck_detail(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    deck.last_accessed = timezone.now()
    deck.views+=1
    deck.save()
    flashcards = list(deck.flashcards.all())
    # Get card index from GET parameter; default is 0.
    try:
        card_index = int(request.GET.get("card", 0))
    except ValueError:
        card_index = 0
    if flashcards:
        # Use modulo to allow cycling through cards.
        current_index = card_index % len(flashcards)
        current_card = flashcards[current_index]
        next_index = current_index + 1
    else:
        current_card = None
        current_index = 0
        next_index = 0
    context = {
        'deck': deck,
        'flashcards': flashcards,
        'current_card': current_card,
        'current_index': current_index,
        'next_index': next_index,
    }
    return render(request, 'flashcards/deck_detail.html', context)

def search_decks(request):
    query = request.GET.get('q', '')
    decks = Deck.objects.none()  # default to empty queryset
    if query:
        decks = Deck.objects.filter(name__icontains=query)
    context = {
        'query': query,
        'decks': decks,
    }
    return render(request, 'flashcards/search_results.html', context)