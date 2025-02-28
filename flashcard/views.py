from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import DeckForm
from .models import Deck, Flashcard
from django.utils import timezone
from . import pdftodeck as pdfread
import os
import tempfile

class FlashcardQueue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

    def get_all(self):
        return self.items

@login_required
def create_deck(request):
    if request.method == 'POST':
        deck_form = DeckForm(request.POST)
        if deck_form.is_valid():
            deck = deck_form.save(commit=False)
            deck.user = request.user

            total = int(request.POST.get('flashcard_total', 0))
            flashcards_added = 0  # Count valid flashcards

            # Using the FlashcardQueue data structure to store flashcards temporarily.
            # this is for data structures implementation
            flashcard_queue = FlashcardQueue()

            for i in range(total):
                title = request.POST.get(f'flashcard_title_{i}', '').strip()
                description = request.POST.get(f'flashcard_description_{i}', '').strip()

                if title and description:
                    # Enqueue a new Flashcard instance.
                    flashcard_queue.enqueue(Flashcard(deck=deck, title=title, description=description, order=i))
                    flashcards_added += 1
                elif title or description:  # Partial flashcard
                    messages.warning(request, "Each flashcard must have both a title and a description.",extra_tags="deck_create")
                    return render(request, 'flashcards/deck_create.html', {'deck_form': deck_form})

            if flashcards_added == 0:
                messages.warning(request, "Deck can't be empty! Add at least one flashcard.",extra_tags="deck_create")
                return render(request, 'flashcards/deck_create.html', {'deck_form': deck_form})

            # Save the deck only if at least one valid flashcard exists.
            deck.save()
            # Bulk insert flashcards using the items stored in our FlashcardQueue.
            Flashcard.objects.bulk_create(flashcard_queue.get_all())

            messages.success(request, 'Flashcard deck created successfully!',extra_tags="deck_create")
            return redirect('deck_list')

        messages.warning(request, 'Please correct the errors below.',extra_tags="deck_create")

    else:
        deck_form = DeckForm()

    return render(request, 'flashcards/deck_create.html', {'deck_form': deck_form})

@login_required
def create_deck_pdf(request):
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        theme = request.POST.get('theme', 'default').strip()
        pdf_file = request.FILES.get('pdf')

        if not title or not pdf_file:
            messages.warning(request, "Both a deck title and a PDF file are required.",extra_tags="deck_create_pdf")
            return render(request, 'flashcards/pdftodeck.html')

        # Save the uploaded PDF to a temporary file.
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, pdf_file.name)
        with open(temp_file_path, 'wb+') as destination:
            for chunk in pdf_file.chunks():
                destination.write(chunk)

        # Extract text from the PDF and generate flashcards using the OpenAI API.
        note_text = pdfread.extract_text_from_pdf(temp_file_path)
        flashcards_list = pdfread.generate_flashcards(note_text)

        if not flashcards_list:
            messages.warning(request, "No valid flashcards were generated from the PDF.",extra_tags="deck_create_pdf")
            return render(request, 'flashcards/pdftodeck.html')

        # Create the deck.
        deck = Deck.objects.create(user=request.user, name=title,theme=theme)

        flashcards = []
        for index, fc in enumerate(flashcards_list):
            question = fc.get('question', '').strip()
            answer = fc.get('answer', '').strip()
            if question and answer:
                flashcards.append(Flashcard(deck=deck, title=question, description=answer, order=index))

        if not flashcards:
            messages.warning(request, "No valid flashcards were generated from the PDF.",extra_tags="deck_create_pdf")
            deck.delete()
            return render(request, 'flashcards/pdftodeck.html')

        # Bulk create flashcards.
        Flashcard.objects.bulk_create(flashcards)
        messages.success(request, "Deck created successfully from PDF!",extra_tags="deck_create_pdf")
        return redirect('deck_list')

    # For GET requests, simply render the PDF upload form.
    return render(request, 'flashcards/pdftodeck.html')

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