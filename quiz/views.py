from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from flashcard.models import Deck, Flashcard
from .models import Quiz
from .forms import QuizAnswerForm
import matplotlib.pyplot as plt
import io
import urllib, base64
from django.contrib import messages

@login_required
def start_quiz(request, deck_id):
    deck = get_object_or_404(Deck, id=deck_id)
    flashcards = list(deck.flashcards.all())

    if not flashcards:
        return render(request, 'quiz/empty_deck.html', {'deck': deck})

    request.session['quiz_data'] = {
        'deck_id': deck.id,
        'total_questions': len(flashcards),
        'correct': 0,
        'wrong': 0,
        'current_index': 0
    }
    
    return redirect('quiz_question')

@login_required
def quiz_question(request):
    quiz_data = request.session.get('quiz_data', {})

    if not quiz_data or 'deck_id' not in quiz_data:
        return redirect('deck_list')

    deck = get_object_or_404(Deck, id=quiz_data['deck_id'])
    flashcards = list(deck.flashcards.all())
    
    current_index = quiz_data['current_index']
    
    if current_index >= len(flashcards):
        return redirect('quiz_result')

    flashcard = flashcards[current_index]
    
    if request.method == 'POST':
        form = QuizAnswerForm(request.POST)
        if form.is_valid():
            user_answer = form.cleaned_data['answer'].strip().lower()
            correct_answer = flashcard.description.strip().lower()
            print(user_answer, correct_answer)
            if user_answer == correct_answer:
                quiz_data['correct'] += 1
            else:
                quiz_data['wrong'] += 1
            
            quiz_data['current_index'] += 1
            request.session['quiz_data'] = quiz_data
            return redirect('quiz_question')

    else:
        form = QuizAnswerForm()

    return render(request, 'quiz/quiz_question.html', {
        'deck': deck,
        'flashcard': flashcard,
        'form': form,
        'current_index': current_index + 1,
        'total_questions': len(flashcards)
    })

@login_required
def quiz_result(request):
    quiz_data = request.session.get('quiz_data', {})

    if not quiz_data or 'deck_id' not in quiz_data:
        return redirect('deck_list')

    deck = get_object_or_404(Deck, id=quiz_data['deck_id'])
    score = quiz_data['correct']
    total_questions = quiz_data['total_questions']
    
    quiz = Quiz.objects.create(
        user=request.user,
        deck=deck,
        score=score,
        total_questions=total_questions,
        correct_answers=quiz_data['correct'],
        wrong_answers=quiz_data['wrong']
    )
    messages.success(request, "This message has been broadcasted")

    # Generate Pie Chart
    labels = ['Correct Answers', 'Wrong Answers']
    values = [quiz_data['correct'], quiz_data['wrong']]
    colors = ['#28a745', '#dc3545']

    plt.figure(figsize=(5, 5))
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'black'})
    plt.title(f"Quiz Result for {deck.name}")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches="tight")
    buffer.seek(0)
    graph_url = urllib.parse.quote(base64.b64encode(buffer.getvalue()).decode())

    del request.session['quiz_data']

    return render(request, 'quiz/quiz_result.html', {
        'deck': deck,
        'quiz': quiz,
        'graph_url': f"data:image/png;base64,{graph_url}"
    })