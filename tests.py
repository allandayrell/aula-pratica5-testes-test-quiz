import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_create_question_with_invalid_points():
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=-5)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=101)

def test_add_choice_with_empty_text_fails():
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')

def test_add_choice_with_text_exceeding_limit_fails():
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)

def test_add_multiple_choices_generates_sequential_ids():
    question = Question(title='q1')
    c1 = question.add_choice('Option 1')
    c2 = question.add_choice('Option 2')
    c3 = question.add_choice('Option 3')
    assert [c1.id, c2.id, c3.id] == [1, 2, 3]

def test_remove_choice_by_id():
    question = Question(title='q1')
    choice1 = question.add_choice('Option 1')
    choice2 = question.add_choice('Option 2')
    question.remove_choice_by_id(choice1.id)
    assert len(question.choices) == 1
    assert question.choices[0].id == choice2.id

def test_remove_choice_with_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('Option 1')
    with pytest.raises(Exception, match='Invalid choice id 99'):
        question.remove_choice_by_id(99)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('Option 1')
    question.add_choice('Option 2')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_set_correct_choices():
    question = Question(title='q1')
    c1 = question.add_choice('Option 1', is_correct=False)
    c2 = question.add_choice('Option 2', is_correct=False)
    question.set_correct_choices([c1.id])
    assert c1.is_correct is True
    assert c2.is_correct is False

def test_set_correct_choices_with_invalid_id_raises_exception():
    question = Question(title='q1')
    question.add_choice('Option 1')
    with pytest.raises(Exception, match='Invalid choice id 42'):
        question.set_correct_choices([42])

def test_correct_selected_choices_exceeding_max_selections_raises_exception():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('Option 1', is_correct=True)
    c2 = question.add_choice('Option 2', is_correct=False)
    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([c1.id, c2.id])
